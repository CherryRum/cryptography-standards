#!/usr/bin/env python3
"""
抓取 gmbz.org.cn 标准检索元数据，并保存原始快照与标准化快照。

用法:
    python fetch_remote_metadata.py
"""
import argparse
import json
import os
import time
import urllib.parse
import urllib.request

from config import REMOTE_METADATA_DIR, REMOTE_METADATA_NORMALIZED_PATH, REMOTE_METADATA_RAW_PATH
from metadata_utils import normalize_remote_record

ENDPOINT = "http://www.gmbz.org.cn/main/normsearch.json"
REFERER = "http://www.gmbz.org.cn/main/bzlb.html"
DEFAULT_PAGE_SIZE = 200
_COLUMNS = [
    ("NORM_ISO_ID", "NORM_ISO_ID"),
    ("NORM_NAME_C", "NORM_NAME_C"),
    ("NORM_ZT_NAME", "NORM_ZT"),
    ("NORM_FLAG_NAME", "NORM_FLAG_NAME"),
    ("NORM_NAME_E", "NORM_NAME_E"),
    ("NORM_CO_NAME", "NORM_CO_NAME"),
    ("NORM_CA_NAME", "NORM_CA_NAME"),
    ("NORM_PUB_DATE", "NORM_PUB_DATE"),
    ("NORM_IMP_DATE", "NORM_IMP_DATE"),
    ("UP_GB_FLAG", "UP_GB_FLAG"),
    ("10", ""),
]


def build_form(draw: int, start: int, length: int) -> bytes:
    form = {
        "draw": str(draw),
        "start": str(start),
        "length": str(length),
        "search[value]": "",
        "search[regex]": "false",
        "norm_iso_id": "",
        "norm_flag": "",
        "norm_name_c": "",
        "norm_name_e": "",
        "norm_co_name": "",
        "norm_zt": "",
        "norm_pub_date_begin": "",
        "norm_pub_date_end": "",
        "norm_imp_date_begin": "",
        "norm_imp_date_end": "",
        "order[0][column]": "0",
        "order[0][dir]": "asc",
    }
    for index, (data_field, name_field) in enumerate(_COLUMNS):
        form[f"columns[{index}][data]"] = data_field
        form[f"columns[{index}][name]"] = name_field
        form[f"columns[{index}][searchable]"] = "true"
        form[f"columns[{index}][orderable]"] = "true"
        form[f"columns[{index}][search][value]"] = ""
        form[f"columns[{index}][search][regex]"] = "false"
    return urllib.parse.urlencode(form).encode("utf-8")


def fetch_page(draw: int, start: int, length: int) -> dict:
    request = urllib.request.Request(
        ENDPOINT,
        data=build_form(draw, start, length),
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": REFERER,
            "Origin": "http://www.gmbz.org.cn",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload


def fetch_all(page_size: int) -> tuple[list[dict], int, int]:
    start = 0
    draw = 1
    rows = []
    records_total = 0
    records_filtered = 0

    while True:
        payload = fetch_page(draw=draw, start=start, length=page_size)
        chunk = payload.get("data") or []
        if not isinstance(chunk, list):
            raise RuntimeError(f"远端返回异常: {payload}")

        rows.extend(chunk)
        records_total = int(payload.get("recordsTotal") or records_total or 0)
        records_filtered = int(payload.get("recordsFiltered") or records_filtered or len(rows))
        print(f"[FETCH] start={start} length={page_size} -> {len(chunk)} 条")

        if len(chunk) < page_size or len(rows) >= records_filtered:
            break
        start += page_size
        draw += 1

    return rows, records_total, records_filtered


def main():
    parser = argparse.ArgumentParser(description="抓取 gmbz.org.cn 标准元数据")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE, help="分页抓取大小")
    args = parser.parse_args()

    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rows, records_total, records_filtered = fetch_all(page_size=args.page_size)
    normalized_records = [normalize_remote_record(row, fetched_at) for row in rows]

    os.makedirs(REMOTE_METADATA_DIR, exist_ok=True)

    raw_payload = {
        "fetchedAt": fetched_at,
        "endpoint": ENDPOINT,
        "referer": REFERER,
        "pageSize": args.page_size,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "records": rows,
    }
    with open(REMOTE_METADATA_RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(raw_payload, f, ensure_ascii=False, indent=2)

    normalized_payload = {
        "fetchedAt": fetched_at,
        "source": "gmbz.org.cn",
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "records": normalized_records,
    }
    with open(REMOTE_METADATA_NORMALIZED_PATH, "w", encoding="utf-8") as f:
        json.dump(normalized_payload, f, ensure_ascii=False, indent=2)

    print(f"[OK] 原始快照: {REMOTE_METADATA_RAW_PATH}")
    print(f"[OK] 标准化快照: {REMOTE_METADATA_NORMALIZED_PATH}")
    print(f"[OK] 共保存 {len(normalized_records)} 条记录")


if __name__ == "__main__":
    main()
