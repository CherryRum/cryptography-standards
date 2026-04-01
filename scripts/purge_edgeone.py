#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EdgeOne CDN Cache Purge Script
腾讯云 EdgeOne CDN 缓存刷新脚本

Supports both domestic (China) and international EdgeOne deployments
支持国内站和国际站的 EdgeOne 部署

Based on Tencent Cloud API v3 signature implementation
基于腾讯云 API 签名 v3 实现
Reference: https://cloud.tencent.com/document/product/213/30654
"""

import hashlib
import hmac
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime

if sys.version_info[0] <= 2:
    from httplib import HTTPSConnection
else:
    from http.client import HTTPSConnection


def check_rate_limit_github():
    """
    Check if enough time has passed since last successful workflow run using GitHub API
    使用 GitHub API 检查距离上次成功的工作流运行是否超过配置的间隔时间
    
    Returns:
        True if can proceed, False if rate limited
    """
    github_token = os.getenv("GITHUB_TOKEN")
    min_interval_hours = float(os.getenv("MIN_INTERVAL_HOURS", "1"))
    github_repository = os.getenv("GITHUB_REPOSITORY")  # e.g., "owner/repo"
    github_workflow = os.getenv("GITHUB_WORKFLOW")  # e.g., "Deploy VuePress Site"
    github_run_id = os.getenv("GITHUB_RUN_ID")  # Current run ID to exclude
    
    if not github_token or not github_repository:
        print("⚠️  Warning: GitHub API credentials not available, skipping rate limit check")
        return True
    
    try:
        # Query GitHub API for recent workflow runs
        # 查询 GitHub API 获取最近的工作流运行记录
        api_url = "https://api.github.com/repos/%s/actions/runs?status=completed&per_page=10" % github_repository
        
        req = urllib.request.Request(api_url)
        req.add_header("Authorization", "Bearer %s" % github_token)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            for run in data.get("workflow_runs", []):
                # Skip current run and non-matching workflows
                # 跳过当前运行和不匹配的工作流
                if str(run["id"]) == github_run_id:
                    continue
                if github_workflow and run["name"] != github_workflow:
                    continue
                if run["conclusion"] != "success":
                    continue
                
                # Check the completion time of last successful run
                # 检查上次成功运行的完成时间
                completed_at = run.get("updated_at") or run.get("created_at")
                if completed_at:
                    # Parse ISO 8601 timestamp
                    # 解析 ISO 8601 时间戳
                    completed_time = datetime.strptime(completed_at.replace("Z", "+00:00").split("+")[0], "%Y-%m-%dT%H:%M:%S")
                    current_time = datetime.utcnow()
                    time_elapsed = (current_time - completed_time).total_seconds()
                    min_interval_seconds = min_interval_hours * 3600
                    
                    if time_elapsed < min_interval_seconds:
                        time_remaining = min_interval_seconds - time_elapsed
                        print("⚠️  Rate limit: Last successful run was %.1f minutes ago" % (time_elapsed / 60))
                        print("   Minimum interval: %.1f hour(s)" % min_interval_hours)
                        print("   Please wait %.1f more minutes before next purge" % (time_remaining / 60))
                        print("   (Last run: %s)" % completed_at)
                        return False
                
                # Only check the most recent successful run
                # 只检查最近一次成功的运行
                break
        
        return True
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print("⚠️  Warning: Could not check GitHub API for rate limiting: HTTP %d" % e.code, file=sys.stderr)
        print("   %s" % error_body, file=sys.stderr)
        return True  # Allow purge if API check fails
    except Exception as e:
        print("⚠️  Warning: Could not check GitHub API for rate limiting: %s" % str(e), file=sys.stderr)
        return True  # Allow purge if API check fails


def sign(key, msg):
    """
    HMAC-SHA256 signing function
    HMAC-SHA256 签名函数
    """
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def purge_edgeone_cache(secret_id, secret_key, zone_id, targets, purge_type="purge_host", site_type="cn"):
    """
    Purge EdgeOne CDN cache
    刷新 EdgeOne CDN 缓存
    
    Args:
        secret_id: Tencent Cloud Secret ID (腾讯云密钥 ID)
        secret_key: Tencent Cloud Secret Key (腾讯云密钥 Key)
        zone_id: EdgeOne Zone ID (站点 ID)
        targets: List of targets to purge (刷新目标列表)
        purge_type: Type of purge operation (刷新类型: purge_host, purge_url, purge_prefix)
        site_type: Site type - "cn" for domestic, "intl" for international
                   (站点类型 - "cn" 表示国内站，"intl" 表示国际站)
    """
    # Configure variables based on site type
    # 根据站点类型配置变量
    if site_type == "intl":
        # International site configuration (国际站配置)
        host = "teo.intl.tencentcloudapi.com"
    else:
        # Domestic site configuration (国内站配置)
        host = "teo.tencentcloudapi.com"
    
    # Common API parameters (通用 API 参数)
    service = "teo"
    action = "CreatePurgeTask"
    version = "2022-09-01"
    algorithm = "TC3-HMAC-SHA256"
    
    # Build request payload (构建请求载荷)
    payload = json.dumps({
        "ZoneId": zone_id,
        "Type": purge_type,
        "Targets": targets
    })
    
    # Print request payload for debugging (打印请求载荷用于调试)
    print("\n📤 Request Payload:")
    print("   %s" % payload)
    print("")
    
    # Get timestamp and date (获取时间戳和日期)
    timestamp = int(time.time())
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    
    # ************* Step 1: Build canonical request (步骤 1：拼接规范请求串) *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (ct, host, action.lower())
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                        canonical_uri + "\n" +
                        canonical_querystring + "\n" +
                        canonical_headers + "\n" +
                        signed_headers + "\n" +
                        hashed_request_payload)
    
    # ************* Step 2: Build string to sign (步骤 2：拼接待签名字符串) *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                     str(timestamp) + "\n" +
                     credential_scope + "\n" +
                     hashed_canonical_request)
    
    # ************* Step 3: Calculate signature (步骤 3：计算签名) *************
    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    
    # ************* Step 4: Build Authorization header (步骤 4：拼接 Authorization) *************
    authorization = (algorithm + " " +
                    "Credential=" + secret_id + "/" + credential_scope + ", " +
                    "SignedHeaders=" + signed_headers + ", " +
                    "Signature=" + signature)
    
    # ************* Step 5: Construct and send request (步骤 5：构造并发起请求) *************
    # Note: X-TC-Region header is not required for EdgeOne API
    # 注意：EdgeOne API 不需要 X-TC-Region 头
    headers = {
        "Authorization": authorization,
        "Content-Type": ct,
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": version
    }
    
    try:
        conn = HTTPSConnection(host)
        conn.request("POST", "/", headers=headers, body=payload.encode("utf-8"))
        response = conn.getresponse()
        response_data = response.read().decode("utf-8")
        result = json.loads(response_data)
        
        # Print response for debugging (打印响应用于调试)
        print("\n📥 Response JSON:")
        print("   %s" % json.dumps(result, indent=2, ensure_ascii=False))
        print("")
        
        if "Response" in result:
            if "Error" in result["Response"]:
                error = result["Response"]["Error"]
                print("❌ API Error: [%s] %s" % (error["Code"], error["Message"]), file=sys.stderr)
                return False
            else:
                print("✅ Cache purge successful!")
                print("   JobId: %s" % result["Response"].get("JobId", "N/A"))
                print("   RequestId: %s" % result["Response"].get("RequestId", "N/A"))
                
                if result["Response"].get("FailedList"):
                    print("⚠️  Failed targets: %s" % result["Response"]["FailedList"], file=sys.stderr)
                
                return True
        else:
            print("❌ Unexpected response format: %s" % result, file=sys.stderr)
            return False
            
    except Exception as err:
        print("❌ Error: %s" % str(err), file=sys.stderr)
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def main():
    """Main entry point (主入口)"""
    if len(sys.argv) < 5:
        print("Usage: python purge_edgeone.py <secret_id> <secret_key> <zone_id> <targets> [--site-type=cn|intl]")
        print("")
        print("Arguments:")
        print("  secret_id   : Tencent Cloud Secret ID")
        print("  secret_key  : Tencent Cloud Secret Key")
        print("  zone_id     : EdgeOne Zone ID")
        print("  targets     : Comma-separated list of targets (e.g., 'gmkit.cn,www.gmkit.cn')")
        print("  --site-type : Site type - 'cn' for domestic (default), 'intl' for international")
        print("")
        print("Examples:")
        print("  Domestic (CN):      python purge_edgeone.py <id> <key> zone-xxx 'gmkit.cn'")
        print("  Domestic (CN):      python purge_edgeone.py <id> <key> zone-xxx 'gmkit.cn,www.gmkit.cn' --site-type=cn")
        print("  International:      python purge_edgeone.py <id> <key> zone-yyy 'gmkit.com' --site-type=intl")
        print("  International:      python purge_edgeone.py <id> <key> zone-yyy 'gmkit.com,www.gmkit.com' --site-type=intl")
        sys.exit(1)
    
    secret_id = sys.argv[1]
    secret_key = sys.argv[2]
    zone_id = sys.argv[3]
    targets_str = sys.argv[4]
    
    # Parse site type from arguments (从参数解析站点类型)
    site_type = "cn"  # Default to domestic (默认国内站)
    for arg in sys.argv[5:]:
        if arg.startswith("--site-type="):
            site_type = arg.split("=")[1]
    
    # Validate site type (验证站点类型)
    if site_type not in ["cn", "intl"]:
        print("❌ Error: Invalid site type '%s'. Must be 'cn' or 'intl'" % site_type, file=sys.stderr)
        sys.exit(1)
    
    # Parse targets - support comma-separated list (解析目标 - 支持逗号分隔列表)
    targets = [t.strip() for t in targets_str.split(",") if t.strip()]
    
    if not targets:
        print("❌ Error: No valid targets specified", file=sys.stderr)
        sys.exit(1)
    
    site_name = "International (国际站)" if site_type == "intl" else "Domestic (国内站)"
    print("🚀 Purging EdgeOne CDN cache for %s..." % site_name)
    print("   Zone ID: %s" % zone_id)
    print("   Targets: %s" % ", ".join(targets))
    print("   Site Type: %s" % site_type)
    
    # Check rate limit using GitHub API (检查速率限制，使用 GitHub API)
    if not check_rate_limit_github():
        print("\n❌ Purge skipped due to rate limit")
        print("   Tip: You can adjust MIN_INTERVAL_HOURS environment variable in workflow")
        sys.exit(0)  # Exit with success to not fail the workflow
    
    success = purge_edgeone_cache(
        secret_id=secret_id,
        secret_key=secret_key,
        zone_id=zone_id,
        targets=targets,
        purge_type="purge_host",
        site_type=site_type
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
