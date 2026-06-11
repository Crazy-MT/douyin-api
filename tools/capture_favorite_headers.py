# -*- coding: utf-8 -*-
"""抓取浏览器里 favorite 请求的真实 headers（用于对比）"""
import sys, json, time
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from lib.reverse.cdp2 import CDP, get_ws

cdp = CDP(get_ws())
cdp.cmd("Network.enable")

print("等待抓取 favorite 请求...")
print("请在浏览器里打开【我的喜欢】页面，或刷新...")

for _ in range(60):
    ev = cdp.wait_event("Network.requestWillBeSent", timeout=2)
    if not ev:
        continue
    req = ev.get("params", {}).get("request", {})
    url = req.get("url", "")
    if "favorite" in url:
        print("\n✅ 抓到 favorite 请求")
        print("URL:", url[:100])
        print("\n=== Request Headers ===")
        for k, v in req.get("headers", {}).items():
            print(f"{k}: {v[:80] if len(v) > 80 else v}")
        cdp.close()
        sys.exit(0)

print("未抓到，请确认浏览器已打开 CDP 调试端口 9222")
cdp.close()
