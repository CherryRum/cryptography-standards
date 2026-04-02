#!/usr/bin/env python3
"""
构建脚本：扫描 PDF → 增量转 WebP → 生成 manifest.json + search-index.json

用法:
    python build_assets.py              # 增量构建
    python build_assets.py --full       # 全量重建
"""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import os
import re
import shutil
import sys
import time
import unicodedata

import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter
import io

from config import (
    REPO_ROOT, CATEGORY_MAP,
    IMAGE_PAGE_WIDTH, IMAGE_COVER_WIDTH, IMAGE_FORMAT,
    IMAGE_PAGE_QUALITY, IMAGE_COVER_QUALITY,
    IMAGE_SHARPEN_RADIUS, IMAGE_SHARPEN_PERCENT, IMAGE_SHARPEN_THRESHOLD,
    IMAGE_CONTRAST,
    OUTPUT_DIR, DOCS_OUTPUT_DIR, DATA_OUTPUT_DIR,
    ASSET_MANIFEST_PATH, DOC_HASH_LENGTH, RENDER_SIGNATURE, BUILD_MAX_WORKERS,
)
from metadata_utils import (
    build_remote_indexes,
    extract_standard_code,
    extract_year,
    load_remote_metadata,
    normalize_standard_code,
    normalize_title,
)

# 压制 MuPDF 对损坏/脏 PDF 的控制台噪音输出，真正失败仍由异常处理。
fitz.TOOLS.mupdf_display_errors(False)
fitz.TOOLS.mupdf_display_warnings(False)

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def sha256_file(path: str) -> str:
    """计算文件 sha256"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    """计算字符串 sha256。"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slugify(text: str) -> str:
    """将中文/特殊字符路径转为 URL 安全的 slug"""
    # 先做 NFKC 规范化
    text = unicodedata.normalize("NFKC", text)
    # 替换路径分隔符和常见特殊字符
    text = text.replace("\\", "/").replace("/", "_")
    # 保留中文、字母、数字、连字符、下划线、点
    text = re.sub(r"[^\w\u4e00-\u9fff.\-]", "_", text)
    # 压缩连续下划线
    text = re.sub(r"_+", "_", text).strip("_")
    return text


_STANDARD_CODE_RE = re.compile(
    r"(?:\(.*?\)\s*)?"
    r"((?:GBT|GMT|GB\/T|GM\/T|GBZ|GMZ|GB\/Z|GM\/Z|GBY|GMY)[\s_]*[\d]+(?:\.[\d]+)?(?:-[\d]{4})?)",
    re.IGNORECASE,
)


def parse_filename(filename: str, category_slug: str):
    """
    从文件名解析标准编号、标题、年份。

    返回 (standardCode, title, year)
    """
    stem = os.path.splitext(filename)[0].strip()
    m = _STANDARD_CODE_RE.search(stem)
    if m:
        raw_code = m.group(1).strip()
        title = stem[m.end():].strip().lstrip("_-:： ").strip() or stem
        code = normalize_standard_code(raw_code) or extract_standard_code(stem)
        year = extract_year(code)
        return code, title, year

    # 英文标准或无法解析的文件名
    title = stem
    return "", title, ""


def apply_remote_metadata(info: dict, remote_record: dict, match_confidence: str, match_key: str):
    info["standardCode"] = remote_record.get("standardCode") or info["standardCode"]
    info["title"] = remote_record.get("title") or info["title"]
    info["year"] = remote_record.get("year") or info["year"]
    info["titleEn"] = remote_record.get("titleEn", "")
    info["publishDate"] = remote_record.get("publishDate", "")
    info["implementDate"] = remote_record.get("implementDate", "")
    info["status"] = remote_record.get("status", "")
    info["statusLabel"] = remote_record.get("statusLabel", "")
    info["standardType"] = remote_record.get("standardType", "")
    info["standardTypeLabel"] = remote_record.get("standardTypeLabel", "")
    info["workingGroup"] = remote_record.get("workingGroup", "")
    info["workingGroupLabel"] = remote_record.get("workingGroupLabel", "")
    info["draftingOrg"] = remote_record.get("draftingOrg", "")
    info["responsibleOrg"] = remote_record.get("responsibleOrg", "")
    info["adoptionType"] = remote_record.get("adoptionType", "")
    info["adoptionTypeLabel"] = remote_record.get("adoptionTypeLabel", "")
    info["upgradedToNationalFlag"] = remote_record.get("upgradedToNationalFlag", "")
    info["remotePdfPath"] = remote_record.get("remotePdfPath", "")
    info["metadataSource"] = remote_record.get("remoteSource", "gmbz.org.cn")
    info["matchConfidence"] = match_confidence
    info["matchKey"] = match_key


def enrich_with_remote_metadata(pdfs: list[dict]):
    payload = load_remote_metadata()
    if not payload:
        for info in pdfs:
            info.update({
                "titleEn": "",
                "publishDate": "",
                "implementDate": "",
                "status": "",
                "statusLabel": "",
                "standardType": "",
                "standardTypeLabel": "",
                "workingGroup": "",
                "workingGroupLabel": "",
                "draftingOrg": "",
                "responsibleOrg": "",
                "adoptionType": "",
                "adoptionTypeLabel": "",
                "upgradedToNationalFlag": "",
                "remotePdfPath": "",
                "metadataSource": "local",
                "matchConfidence": "none",
                "matchKey": "",
            })
        return {
            "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "remoteAvailable": False,
            "remoteSource": "gmbz.org.cn",
            "summary": {
                "totalDocs": len(pdfs),
                "remoteRecords": 0,
                "matched": 0,
                "matchedByCode": 0,
                "matchedByTitle": 0,
                "ambiguousByCode": 0,
                "ambiguousByTitle": 0,
                "unmatched": len(pdfs),
            },
            "unmatched": [
                {
                    "id": info["id"],
                    "relPath": info["rel_path"],
                    "category": info["category"],
                    "standardCode": info["standardCode"],
                    "title": info["title"],
                }
                for info in pdfs
            ],
            "ambiguous": [],
        }

    records = payload.get("records", [])
    code_index, title_index = build_remote_indexes(records)
    matched_by_code = 0
    matched_by_title = 0
    ambiguous_by_code = 0
    ambiguous_by_title = 0
    unmatched = []
    ambiguous = []

    for info in pdfs:
        info.update({
            "titleEn": "",
            "publishDate": "",
            "implementDate": "",
            "status": "",
            "statusLabel": "",
            "standardType": "",
            "standardTypeLabel": "",
            "workingGroup": "",
            "workingGroupLabel": "",
            "draftingOrg": "",
            "responsibleOrg": "",
            "adoptionType": "",
            "adoptionTypeLabel": "",
            "upgradedToNationalFlag": "",
            "remotePdfPath": "",
            "metadataSource": "local",
            "matchConfidence": "none",
            "matchKey": "",
        })

        normalized_code = normalize_standard_code(info.get("standardCode"))
        normalized_title = normalize_title(info.get("title"))

        if normalized_code and normalized_code in code_index:
            matches = code_index[normalized_code]
            if len(matches) == 1:
                apply_remote_metadata(info, matches[0], "code", normalized_code)
                matched_by_code += 1
                continue

            ambiguous_by_code += 1
            ambiguous.append({
                "id": info["id"],
                "relPath": info["rel_path"],
                "category": info["category"],
                "matchConfidence": "ambiguous-code",
                "matchKey": normalized_code,
                "candidates": [
                    {
                        "standardCode": candidate.get("standardCode", ""),
                        "title": candidate.get("title", ""),
                        "statusLabel": candidate.get("statusLabel", ""),
                    }
                    for candidate in matches
                ],
            })
            continue

        if (not normalized_code) and normalized_title and normalized_title in title_index:
            matches = title_index[normalized_title]
            if len(matches) == 1:
                apply_remote_metadata(info, matches[0], "title", normalized_title)
                matched_by_title += 1
                continue

            ambiguous_by_title += 1
            ambiguous.append({
                "id": info["id"],
                "relPath": info["rel_path"],
                "category": info["category"],
                "matchConfidence": "ambiguous-title",
                "matchKey": normalized_title,
                "candidates": [
                    {
                        "standardCode": candidate.get("standardCode", ""),
                        "title": candidate.get("title", ""),
                        "statusLabel": candidate.get("statusLabel", ""),
                    }
                    for candidate in matches
                ],
            })
            continue

        unmatched.append({
            "id": info["id"],
            "relPath": info["rel_path"],
            "category": info["category"],
            "standardCode": info["standardCode"],
            "title": info["title"],
        })

    return {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "remoteAvailable": True,
        "remoteSource": payload.get("source", "gmbz.org.cn"),
        "remoteFetchedAt": payload.get("fetchedAt", ""),
        "summary": {
            "totalDocs": len(pdfs),
            "remoteRecords": len(records),
            "matched": matched_by_code + matched_by_title,
            "matchedByCode": matched_by_code,
            "matchedByTitle": matched_by_title,
            "ambiguousByCode": ambiguous_by_code,
            "ambiguousByTitle": ambiguous_by_title,
            "unmatched": len(unmatched),
        },
        "unmatched": unmatched,
        "ambiguous": ambiguous,
    }


def render_page_to_webp(page: fitz.Page, width: int, quality: int) -> bytes:
    """将 PDF 页面渲染为 WebP 字节"""
    # 计算缩放比例
    page_rect = page.rect
    zoom = width / page_rect.width
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    # 通过 Pillow 转为 webp
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img = img.filter(
        ImageFilter.UnsharpMask(
            radius=IMAGE_SHARPEN_RADIUS,
            percent=IMAGE_SHARPEN_PERCENT,
            threshold=IMAGE_SHARPEN_THRESHOLD,
        )
    )
    img = ImageEnhance.Contrast(img).enhance(IMAGE_CONTRAST)
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=quality, method=4)
    return buf.getvalue()


def extract_pdf_text(path: str):
    """提取 PDF 页数、全文文本和摘要。"""
    doc = fitz.open(path)
    try:
        page_count = len(doc)
        text_parts = []
        for page in doc:
            text = page.get_text().strip()
            if text:
                text_parts.append(text)
    finally:
        doc.close()

    full_text = "\n".join(text_parts)
    excerpt = full_text[:500].replace("\n", " ").strip() if full_text else ""
    return page_count, full_text, excerpt


def get_pdf_page_count(path: str) -> int:
    """仅获取页数，用于快速判断渲染目录是否完整。"""
    doc = fitz.open(path)
    try:
        return len(doc)
    finally:
        doc.close()


def is_render_complete(doc_id: str, doc_hash: str, page_count: int) -> bool:
    """检查当前 hash 对应的渲染目录是否完整，可用于断点恢复。"""
    doc_dir = os.path.join(DOCS_OUTPUT_DIR, doc_id, doc_hash)
    pages_dir = os.path.join(doc_dir, "pages")
    cover_path = os.path.join(doc_dir, "cover.webp")
    if not os.path.exists(cover_path) or not os.path.isdir(pages_dir):
        return False

    page_files = [
        name for name in os.listdir(pages_dir)
        if name.lower().endswith(".webp")
    ]
    return len(page_files) == page_count


# ---------------------------------------------------------------------------
# 扫描 PDF
# ---------------------------------------------------------------------------

def scan_pdfs():
    """扫描所有分类目录，返回 PDF 信息列表"""
    results = []
    for dir_name, (cat_slug, cat_label) in CATEGORY_MAP.items():
        dir_path = os.path.join(REPO_ROOT, dir_name)
        if not os.path.isdir(dir_path):
            print(f"[WARN] 目录不存在，跳过: {dir_name}")
            continue
        for fname in sorted(os.listdir(dir_path)):
            if not fname.lower().endswith(".pdf"):
                continue
            fpath = os.path.join(dir_path, fname)
            if not os.path.isfile(fpath):
                continue
            rel_path = os.path.join(dir_name, fname)
            doc_id = slugify(os.path.splitext(rel_path)[0])
            standard_code, title, year = parse_filename(fname, cat_slug)
            results.append({
                "id": doc_id,
                "filename": fname,
                "rel_path": rel_path,
                "abs_path": fpath,
                "category": cat_slug,
                "categoryLabel": cat_label,
                "standardCode": standard_code,
                "title": title,
                "year": year,
            })
    return results


# ---------------------------------------------------------------------------
# 增量判断
# ---------------------------------------------------------------------------

def load_asset_manifest():
    """加载上一次的 asset-manifest.json"""
    if os.path.exists(ASSET_MANIFEST_PATH):
        with open(ASSET_MANIFEST_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, dict) and "docs" in raw:
            return raw
        if isinstance(raw, dict):
            return {
                "_meta": {"render_signature": ""},
                "docs": raw,
            }
    return {"_meta": {"render_signature": ""}, "docs": {}}


def save_asset_manifest(manifest: dict):
    """保存 asset-manifest.json"""
    os.makedirs(os.path.dirname(ASSET_MANIFEST_PATH), exist_ok=True)
    with open(ASSET_MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# 核心：处理单个 PDF
# ---------------------------------------------------------------------------

def process_pdf(info: dict, doc_hash: str):
    """处理单个 PDF：渲染页图 + 封面 + 提取文本"""
    doc_dir = os.path.join(DOCS_OUTPUT_DIR, info["id"], doc_hash)
    pages_dir = os.path.join(doc_dir, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    doc = fitz.open(info["abs_path"])
    try:
        page_count = len(doc)
        text_parts = []

        for i, page in enumerate(doc):
            # 渲染阅读图
            webp_data = render_page_to_webp(page, IMAGE_PAGE_WIDTH, IMAGE_PAGE_QUALITY)
            page_path = os.path.join(pages_dir, f"{i + 1:04d}.webp")
            with open(page_path, "wb") as f:
                f.write(webp_data)

            # 封面（第一页，较小尺寸）
            if i == 0:
                cover_data = render_page_to_webp(page, IMAGE_COVER_WIDTH, IMAGE_COVER_QUALITY)
                cover_path = os.path.join(doc_dir, "cover.webp")
                with open(cover_path, "wb") as f:
                    f.write(cover_data)

            # 提取文本
            text = page.get_text().strip()
            if text:
                text_parts.append(text)
    finally:
        doc.close()

    full_text = "\n".join(text_parts)
    # 截取摘要（前 500 字符）
    excerpt = full_text[:500].replace("\n", " ").strip() if full_text else ""

    return page_count, full_text, excerpt


def process_pdf_job(info: dict, doc_hash: str, needs_render: bool, recover_render: bool):
    """子进程任务：提取文本，并在需要时渲染页面。"""
    t0 = time.time()
    page_count, full_text, excerpt = extract_pdf_text(info["abs_path"])
    render_complete = is_render_complete(info["id"], doc_hash, page_count)

    if needs_render and not render_complete:
        current_dir = os.path.join(DOCS_OUTPUT_DIR, info["id"], doc_hash)
        if os.path.exists(current_dir):
            shutil.rmtree(current_dir)
        page_count, full_text, excerpt = process_pdf(info, doc_hash)
        render_complete = True

    return {
        "id": info["id"],
        "pageCount": page_count,
        "fullText": full_text,
        "excerpt": excerpt,
        "rendered": needs_render and render_complete,
        "recovered": recover_render and render_complete,
        "elapsed": time.time() - t0,
    }


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def build(full_rebuild: bool = False):
    print("=" * 60)
    print("密码标准文档站 - 资源构建")
    print("=" * 60)

    # 1. 扫描 PDF
    pdfs = scan_pdfs()
    print(f"\n扫描到 {len(pdfs)} 个 PDF 文件")

    metadata_match_report = enrich_with_remote_metadata(pdfs)
    metadata_summary = metadata_match_report["summary"]
    if metadata_match_report.get("remoteAvailable"):
        print(
            "\n远端元数据匹配: "
            f"成功 {metadata_summary['matched']} "
            f"(编号 {metadata_summary['matchedByCode']}, 标题 {metadata_summary['matchedByTitle']}), "
            f"冲突 {metadata_summary['ambiguousByCode'] + metadata_summary['ambiguousByTitle']}, "
            f"未匹配 {metadata_summary['unmatched']}"
        )
    else:
        print("\n[WARN] 未找到远端元数据缓存，将仅使用本地文件名元数据")

    # 2. 计算哈希
    print("\n计算文件哈希...")
    current_hashes = {}
    for info in pdfs:
        h = sha256_file(info["abs_path"])
        current_hashes[info["id"]] = h
        info["sha256"] = h
        info["doc_hash"] = sha256_text(f"{h}:{RENDER_SIGNATURE}")[:DOC_HASH_LENGTH]

    # 3. 加载旧 manifest
    loaded_manifest = load_asset_manifest()
    previous_render_signature = loaded_manifest.get("_meta", {}).get("render_signature", "")
    render_signature_changed = previous_render_signature != RENDER_SIGNATURE
    old_manifest = {"_meta": {"render_signature": RENDER_SIGNATURE}, "docs": {}}
    if not full_rebuild and not render_signature_changed:
        old_manifest = loaded_manifest

    # 4. 确定变更
    new_ids = set()
    changed_ids = set()
    deleted_ids = set()
    unchanged_ids = set()

    current_id_set = {info["id"] for info in pdfs}
    old_docs = old_manifest.get("docs", {})
    old_id_set = set(old_docs.keys())

    for info in pdfs:
        doc_id = info["id"]
        if doc_id not in old_docs:
            new_ids.add(doc_id)
        elif old_docs[doc_id] != info["sha256"]:
            changed_ids.add(doc_id)
        else:
            unchanged_ids.add(doc_id)

    deleted_ids = old_id_set - current_id_set

    to_process = new_ids | changed_ids
    print(f"\n新增: {len(new_ids)}, 变更: {len(changed_ids)}, "
          f"删除: {len(deleted_ids)}, 未变: {len(unchanged_ids)}")
    print(f"需处理: {len(to_process)} 个 PDF")
    if full_rebuild:
        print("模式: 全量重建（强制重新渲染）")
    elif render_signature_changed:
        print("检测到渲染参数变化，将重新渲染全部文档")

    # 5. 确保输出目录存在
    os.makedirs(DOCS_OUTPUT_DIR, exist_ok=True)
    os.makedirs(DATA_OUTPUT_DIR, exist_ok=True)

    # 6. 删除旧资源
    for doc_id in deleted_ids:
        old_dir = os.path.join(DOCS_OUTPUT_DIR, doc_id)
        if os.path.exists(old_dir):
            shutil.rmtree(old_dir)
            print(f"  [DEL] {doc_id}")

    # 7. 对于变更的文档，清理旧 hash 目录
    for info in pdfs:
        if full_rebuild or render_signature_changed or info["id"] in changed_ids:
            doc_base = os.path.join(DOCS_OUTPUT_DIR, info["id"])
            if os.path.exists(doc_base):
                shutil.rmtree(doc_base)

    # 8. 处理新增/变更 PDF
    manifest_entries = []
    search_docs = []
    rendered_docs = 0
    skipped_render = 0
    recovered_render = 0
    errors = []
    worker_count = max(1, BUILD_MAX_WORKERS)
    print(f"并行构建进程数: {worker_count}")

    jobs = []
    for index, info in enumerate(pdfs):
        doc_id = info["id"]
        doc_hash = info["doc_hash"]
        preview_page_count = get_pdf_page_count(info["abs_path"])
        render_complete_hint = is_render_complete(doc_id, doc_hash, preview_page_count)
        needs_render = full_rebuild or (doc_id in to_process) or (not render_complete_hint)
        recover_render = (not full_rebuild) and (doc_id not in to_process) and (not render_complete_hint)

        if (not full_rebuild) and (doc_id in to_process) and render_complete_hint:
            skipped_render += 1
            print(f"\n[SKIP] {info['filename']} 已存在完整渲染结果")
            needs_render = False

        jobs.append((index, info, doc_hash, needs_render, recover_render))

    results_by_index = {}

    if worker_count == 1:
        for index, info, doc_hash, needs_render, recover_render in jobs:
            try:
                result = process_pdf_job(info, doc_hash, needs_render, recover_render)
                results_by_index[index] = result
                if result["rendered"]:
                    rendered_docs += 1
                    if result["recovered"]:
                        recovered_render += 1
                        print(f"\n[RECOVER {recovered_render}] {info['filename']}")
                    else:
                        print(f"\n[{rendered_docs}] {info['filename']}")
                    print(f"  → {result['pageCount']} 页, 耗时 {result['elapsed']:.1f}s")
            except Exception as exc:
                errors.append({
                    "id": info["id"],
                    "path": info["rel_path"],
                    "error": str(exc),
                })
                print(f"\n[ERROR] {info['rel_path']}: {exc}")
    else:
        with ProcessPoolExecutor(max_workers=worker_count) as executor:
            future_map = {
                executor.submit(process_pdf_job, info, doc_hash, needs_render, recover_render): (index, info)
                for index, info, doc_hash, needs_render, recover_render in jobs
            }

            for future in as_completed(future_map):
                index, info = future_map[future]
                try:
                    result = future.result()
                    results_by_index[index] = result
                    if result["rendered"]:
                        rendered_docs += 1
                        if result["recovered"]:
                            recovered_render += 1
                            print(f"\n[RECOVER {recovered_render}] {info['filename']}")
                        else:
                            print(f"\n[{rendered_docs}] {info['filename']}")
                        print(f"  → {result['pageCount']} 页, 耗时 {result['elapsed']:.1f}s")
                except Exception as exc:
                    errors.append({
                        "id": info["id"],
                        "path": info["rel_path"],
                        "error": str(exc),
                    })
                    print(f"\n[ERROR] {info['rel_path']}: {exc}")

    for index, info in enumerate(pdfs):
        result = results_by_index.get(index)
        if result is None:
            continue

        doc_id = info["id"]
        doc_hash = info["doc_hash"]
        page_count = result["pageCount"]
        full_text = result["fullText"]
        excerpt = result["excerpt"]

        # manifest 条目
        cover_url = f"/docs/{doc_id}/{doc_hash}/cover.webp"
        pages_base = f"/docs/{doc_id}/{doc_hash}/pages"

        entry = {
            "id": doc_id,
            "title": info["title"],
            "standardCode": info["standardCode"],
            "category": info["category"],
            "categoryLabel": info["categoryLabel"],
            "year": info["year"],
            "titleEn": info.get("titleEn", ""),
            "publishDate": info.get("publishDate", ""),
            "implementDate": info.get("implementDate", ""),
            "status": info.get("status", ""),
            "statusLabel": info.get("statusLabel", ""),
            "standardType": info.get("standardType", ""),
            "standardTypeLabel": info.get("standardTypeLabel", ""),
            "workingGroup": info.get("workingGroup", ""),
            "workingGroupLabel": info.get("workingGroupLabel", ""),
            "draftingOrg": info.get("draftingOrg", ""),
            "responsibleOrg": info.get("responsibleOrg", ""),
            "adoptionType": info.get("adoptionType", ""),
            "adoptionTypeLabel": info.get("adoptionTypeLabel", ""),
            "upgradedToNationalFlag": info.get("upgradedToNationalFlag", ""),
            "remotePdfPath": info.get("remotePdfPath", ""),
            "metadataSource": info.get("metadataSource", "local"),
            "matchConfidence": info.get("matchConfidence", "none"),
            "matchKey": info.get("matchKey", ""),
            "pageCount": page_count,
            "coverUrl": cover_url,
            "pagesBaseUrl": pages_base,
            "updatedAt": time.strftime("%Y-%m-%d"),
        }
        manifest_entries.append(entry)

        # 搜索索引条目
        search_doc = {
            "id": doc_id,
            "standardCode": info["standardCode"],
            "title": info["title"],
            "category": info["category"],
            "categoryLabel": info["categoryLabel"],
            "year": info["year"],
            "titleEn": info.get("titleEn", ""),
            "publishDate": info.get("publishDate", ""),
            "implementDate": info.get("implementDate", ""),
            "statusLabel": info.get("statusLabel", ""),
            "standardTypeLabel": info.get("standardTypeLabel", ""),
            "workingGroupLabel": info.get("workingGroupLabel", ""),
            "draftingOrg": info.get("draftingOrg", ""),
            "responsibleOrg": info.get("responsibleOrg", ""),
            "textExcerpt": excerpt,
            "fulltext": full_text[:5000] if full_text else "",
        }
        search_docs.append(search_doc)

    # 9. 写入 manifest.json
    manifest_path = os.path.join(DATA_OUTPUT_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] manifest.json: {len(manifest_entries)} 条记录")

    # 10. 写入 search-index.json（前端 MiniSearch 直接消费的文档列表）
    search_path = os.path.join(DATA_OUTPUT_DIR, "search-index.json")
    with open(search_path, "w", encoding="utf-8") as f:
        json.dump(search_docs, f, ensure_ascii=False)
    print(f"[OK] search-index.json: {len(search_docs)} 条记录")

    match_report_path = os.path.join(DATA_OUTPUT_DIR, "metadata-match-report.json")
    with open(match_report_path, "w", encoding="utf-8") as f:
        json.dump(metadata_match_report, f, ensure_ascii=False, indent=2)
    print(f"[OK] metadata-match-report.json 已保存")

    # 11. 保存 asset-manifest（sha256 映射）
    new_asset_manifest = {
        "_meta": {"render_signature": RENDER_SIGNATURE},
        "docs": {info["id"]: info["sha256"] for info in pdfs},
    }
    save_asset_manifest(new_asset_manifest)
    print(f"[OK] asset-manifest.json 已保存")
    if skipped_render:
        print(f"[OK] 复用已有渲染结果: {skipped_render} 个")
    if recovered_render:
        print(f"[OK] 恢复缺失渲染结果: {recovered_render} 个")
    if errors:
        errors_path = os.path.join(DATA_OUTPUT_DIR, "build-errors.json")
        with open(errors_path, "w", encoding="utf-8") as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)
        print(f"[WARN] 构建中有 {len(errors)} 个文档失败，详见: {errors_path}")

    print(f"\n{'=' * 60}")
    print(f"构建完成！产物目录: {OUTPUT_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="密码标准文档站 - 资源构建脚本")
    parser.add_argument("--full", action="store_true", help="全量重建（忽略增量缓存）")
    args = parser.parse_args()
    build(full_rebuild=args.full)
