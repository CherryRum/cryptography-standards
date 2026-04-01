"""构建配置常量"""
import os

# 仓库根目录（脚本在 scripts/ 下，向上一级）
REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

# PDF 分类目录映射：目录名 → (categorySlug, categoryLabel)
CATEGORY_MAP = {
    "GBT 密码国家标准":       ("gbt",            "国家标准"),
    "GMT 密码行业标准（现行）": ("gmt",            "行业标准（现行）"),
    "GMT 密码行业标准（废止）": ("gmt-deprecated", "行业标准（废止）"),
    "公开文档":               ("public",          "公开文档"),
    "英文标准":               ("english",         "英文标准"),
}

# 图像渲染参数
IMAGE_PAGE_WIDTH = 1664      # 阅读图宽度 px
IMAGE_COVER_WIDTH = 640      # 封面宽度 px
IMAGE_FORMAT = "webp"
IMAGE_PAGE_QUALITY = 82
IMAGE_COVER_QUALITY = 78
IMAGE_SHARPEN_RADIUS = 0.8
IMAGE_SHARPEN_PERCENT = 115
IMAGE_SHARPEN_THRESHOLD = 2
IMAGE_CONTRAST = 1.05
RENDER_SIGNATURE = (
    f"w{IMAGE_PAGE_WIDTH}-cw{IMAGE_COVER_WIDTH}-"
    f"q{IMAGE_PAGE_QUALITY}-{IMAGE_COVER_QUALITY}-"
    f"usm{IMAGE_SHARPEN_RADIUS}-{IMAGE_SHARPEN_PERCENT}-{IMAGE_SHARPEN_THRESHOLD}-"
    f"ct{IMAGE_CONTRAST}"
)

# 输出目录（相对于 REPO_ROOT）
OUTPUT_DIR = os.path.join(REPO_ROOT, "dist")
DOCS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "docs")
DATA_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "data")

# 增量构建 manifest 文件路径
ASSET_MANIFEST_PATH = os.path.join(REPO_ROOT, "scripts", "asset-manifest.json")
REMOTE_METADATA_DIR = os.path.join(REPO_ROOT, "scripts", "remote-metadata")
REMOTE_METADATA_RAW_PATH = os.path.join(REMOTE_METADATA_DIR, "gmbz-normsearch-raw.json")
REMOTE_METADATA_NORMALIZED_PATH = os.path.join(REMOTE_METADATA_DIR, "gmbz-normsearch-normalized.json")

# docHash 长度（sha256 截取前 N 位）
DOC_HASH_LENGTH = 8
