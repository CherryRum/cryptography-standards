#!/usr/bin/env python3
"""
构建脚本：扫描 PDF → 增量转 WebP → 生成 manifest.json + search-index.json

用法:
    python build_assets.py              # 增量构建
    python build_assets.py --full       # 全量重建
"""
import argparse
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
    ASSET_MANIFEST_PATH, DOC_HASH_LENGTH,
)

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
    r"^(?:\(.*?\))?\s*"                         # 可能的前缀如 "(瘦身前)"
    r"((?:GBT|GMT|GB\/T|GM\/T)\s*[\d]+(?:\.[\d]+)?(?:-[\d]{4})?)"  # 标准编号
    r"\s*"
    r"(.+?)\.pdf$",                             # 标题
    re.IGNORECASE,
)

_YEAR_RE = re.compile(r"-(\d{4})")


def parse_filename(filename: str, category_slug: str):
    """
    从文件名解析标准编号、标题、年份。

    返回 (standardCode, title, year)
    """
    m = _STANDARD_CODE_RE.match(filename)
    if m:
        raw_code = m.group(1).strip()
        title = m.group(2).strip().lstrip("_-:： ").strip()
        # 规范化标准编号格式：GBT → GB/T, GMT → GM/T
        code = raw_code
        if code.upper().startswith("GBT") and "/" not in code[:4]:
            code = "GB/T " + code[3:].lstrip()
        elif code.upper().startswith("GMT") and "/" not in code[:4]:
            code = "GM/T " + code[3:].lstrip()
        year_m = _YEAR_RE.search(code)
        year = year_m.group(1) if year_m else ""
        return code, title, year

    # 英文标准或无法解析的文件名
    title = filename.rsplit(".pdf", 1)[0].strip()
    return "", title, ""


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
            return json.load(f)
    return {}


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

    # 2. 计算哈希
    print("\n计算文件哈希...")
    current_hashes = {}
    for info in pdfs:
        h = sha256_file(info["abs_path"])
        current_hashes[info["id"]] = h
        info["sha256"] = h
        info["doc_hash"] = h[:DOC_HASH_LENGTH]

    # 3. 加载旧 manifest
    old_manifest = {} if full_rebuild else load_asset_manifest()

    # 4. 确定变更
    new_ids = set()
    changed_ids = set()
    deleted_ids = set()
    unchanged_ids = set()

    current_id_set = {info["id"] for info in pdfs}
    old_id_set = set(old_manifest.keys())

    for info in pdfs:
        doc_id = info["id"]
        if doc_id not in old_manifest:
            new_ids.add(doc_id)
        elif old_manifest[doc_id] != info["sha256"]:
            changed_ids.add(doc_id)
        else:
            unchanged_ids.add(doc_id)

    deleted_ids = old_id_set - current_id_set

    to_process = new_ids | changed_ids
    print(f"\n新增: {len(new_ids)}, 变更: {len(changed_ids)}, "
          f"删除: {len(deleted_ids)}, 未变: {len(unchanged_ids)}")
    print(f"需处理: {len(to_process)} 个 PDF")

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
        if info["id"] in changed_ids:
            doc_base = os.path.join(DOCS_OUTPUT_DIR, info["id"])
            if os.path.exists(doc_base):
                shutil.rmtree(doc_base)

    # 8. 处理新增/变更 PDF
    manifest_entries = []
    search_docs = []
    processed = 0
    skipped_render = 0
    errors = []

    for info in pdfs:
        doc_id = info["id"]
        doc_hash = info["doc_hash"]

        try:
            page_count, full_text, excerpt = extract_pdf_text(info["abs_path"])

            if doc_id in to_process:
                if is_render_complete(doc_id, doc_hash, page_count):
                    skipped_render += 1
                    print(f"\n[SKIP] {info['filename']} 已存在完整渲染结果")
                else:
                    current_dir = os.path.join(DOCS_OUTPUT_DIR, doc_id, doc_hash)
                    if os.path.exists(current_dir):
                        shutil.rmtree(current_dir)

                    processed += 1
                    print(f"\n[{processed}/{len(to_process)}] {info['filename']}")
                    t0 = time.time()
                    page_count, full_text, excerpt = process_pdf(info, doc_hash)
                    elapsed = time.time() - t0
                    print(f"  → {page_count} 页, 耗时 {elapsed:.1f}s")
        except Exception as exc:
            errors.append({
                "id": doc_id,
                "path": info["rel_path"],
                "error": str(exc),
            })
            print(f"\n[ERROR] {info['rel_path']}: {exc}")
            continue

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

    # 11. 保存 asset-manifest（sha256 映射）
    new_asset_manifest = {info["id"]: info["sha256"] for info in pdfs}
    save_asset_manifest(new_asset_manifest)
    print(f"[OK] asset-manifest.json 已保存")
    if skipped_render:
        print(f"[OK] 复用已有渲染结果: {skipped_render} 个")
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
