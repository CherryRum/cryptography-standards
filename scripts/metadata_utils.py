import html
import json
import os
import re
import unicodedata

from config import REMOTE_METADATA_NORMALIZED_PATH

_DATE_RE = re.compile(r"^\d{8}$")
_YEAR_RE = re.compile(r"-(\d{4})")
_STANDARD_CODE_SEARCH_RE = re.compile(
    r"(GB\/T|GM\/T|GB\/Z|GM\/Z|GBT|GMT|GBZ|GMZ|GBY|GMY)[\s_]*([\d]+(?:\.[\d]+)?(?:-[\d]{4})?)",
    re.IGNORECASE,
)
_PREFIX_MAP = {
    "GBT": "GB/T",
    "GMT": "GM/T",
    "GBZ": "GB/Z",
    "GMZ": "GM/Z",
    "GBY": "GB/Y",
    "GMY": "GM/Y",
}


def clean_text(value) -> str:
    if value is None:
        return ""
    text = html.unescape(str(value))
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return "" if text == "" else text


def clean_date(value) -> str:
    text = clean_text(value)
    if not text:
        return ""
    digits = re.sub(r"[^\d]", "", text)
    if _DATE_RE.match(digits):
        return f"{digits[:4]}-{digits[4:6]}-{digits[6:8]}"
    return text


def extract_year(value) -> str:
    text = clean_text(value)
    if not text:
        return ""
    digits = re.sub(r"[^\d]", "", text)
    if len(digits) >= 4:
        return digits[:4]
    match = _YEAR_RE.search(text)
    return match.group(1) if match else ""


def normalize_standard_code(value) -> str:
    text = clean_text(value).upper()
    if not text:
        return ""
    text = text.replace("／", "/")
    match = _STANDARD_CODE_SEARCH_RE.search(text)
    if not match:
        return ""
    prefix = match.group(1).upper()
    suffix = match.group(2)
    prefix = _PREFIX_MAP.get(prefix, prefix)
    return f"{prefix} {suffix}"


def extract_standard_code(value) -> str:
    return normalize_standard_code(value)


def normalize_title(value) -> str:
    text = clean_text(value).lower()
    if not text:
        return ""
    text = re.sub(r"[^\w\u4e00-\u9fff]+", "", text)
    return text.replace("_", "")


def normalize_remote_record(record: dict, fetched_at: str) -> dict:
    standard_code = normalize_standard_code(
        record.get("NORM_ISO_ID") or record.get("NORM_ID") or record.get("USE_ISO_ID")
    )
    title = clean_text(record.get("NORM_NAME_C"))
    publish_date = clean_date(record.get("NORM_PUB_DATE"))
    implement_date = clean_date(record.get("NORM_IMP_DATE"))
    year = extract_year(publish_date) or extract_year(standard_code)
    return {
        "normId": clean_text(record.get("NORM_ID")),
        "normIsoId": clean_text(record.get("NORM_ISO_ID")),
        "standardCode": standard_code,
        "normalizedCode": normalize_standard_code(standard_code),
        "title": title,
        "normalizedTitle": normalize_title(title),
        "titleEn": clean_text(record.get("NORM_NAME_E")),
        "year": year,
        "publishDate": publish_date,
        "implementDate": clean_date(record.get("NORM_IMP_DATE")),
        "status": clean_text(record.get("NORM_ZT")),
        "statusLabel": clean_text(record.get("NORM_ZT_NAME")),
        "standardType": clean_text(record.get("NORM_FLAG")),
        "standardTypeLabel": clean_text(record.get("NORM_FLAG_NAME")),
        "workingGroup": clean_text(record.get("NORM_WG")),
        "workingGroupLabel": clean_text(record.get("NORM_WG_NAME")),
        "draftingOrg": clean_text(record.get("NORM_CO_NAME")),
        "responsibleOrg": clean_text(record.get("NORM_CA_NAME")),
        "adoptionType": clean_text(record.get("USE_ISO_TYPE")),
        "adoptionTypeLabel": clean_text(record.get("USE_ISO_TYPE_NAME")),
        "upgradedToNationalFlag": clean_text(record.get("UP_GB_FLAG")),
        "remotePdfPath": clean_text(record.get("NORM_APP_ADDR")),
        "remoteSource": "gmbz.org.cn",
        "remoteFetchedAt": fetched_at,
    }


def load_remote_metadata(path: str = REMOTE_METADATA_NORMALIZED_PATH):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, dict):
        return payload
    return {
        "fetchedAt": "",
        "source": "gmbz.org.cn",
        "records": payload,
    }


def build_remote_indexes(records):
    code_index = {}
    title_index = {}
    for record in records:
        code = record.get("normalizedCode") or normalize_standard_code(record.get("standardCode"))
        title = record.get("normalizedTitle") or normalize_title(record.get("title"))
        if code:
            code_index.setdefault(code, []).append(record)
        if title:
            title_index.setdefault(title, []).append(record)
    return code_index, title_index
