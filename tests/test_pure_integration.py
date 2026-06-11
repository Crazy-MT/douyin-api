# -*- coding: utf-8 -*-
"""测试纯 Python a_bogus 集成到 Request 类"""
import sys
sys.path.insert(0, 'D:/python-project/douyin-api')

from utils.request import Request
import httpx
import json

r = Request()

# 测试纯 Python 方法
url = 'https://www.douyin.com/aweme/v1/web/aweme/detail/'
params = {
    'aweme_id': '7123456789012345678',
    'device_platform': 'webapp',
    'aid': '6383',
}
params = r.get_params(params)

# 用纯 Python 生成
a_bogus_pure = r.get_sign_pure(url, params)
print(f"纯 Python 生成: {a_bogus_pure[:60]}...")
print(f"长度: {len(a_bogus_pure)}")

# 真实请求测试
params['a_bogus'] = a_bogus_pure
cfg = json.load(open('D:/python-project/douyin-api/config/cookie.json', encoding='utf-8'))

headers = {
    "User-Agent": r.HEADERS.get("User-Agent"),
    "Referer": "https://www.douyin.com/",
}

print("\n发送请求...")
with httpx.Client(verify=False, timeout=10) as client:
    resp = client.get(url, params=params, headers=headers, cookies=cfg)

print(f"HTTP {resp.status_code}")

if resp.status_code == 200:
    try:
        data = resp.json()
        print(f"返回 keys: {list(data.keys())}")
        if 'aweme_detail' in data:
            print("\nSUCCESS - 纯 Python 方法集成成功！")
        else:
            print(f"返回数据异常: {data}")
    except:
        print(f"JSON 解析失败: {resp.text[:200]}")
else:
    print(f"FAIL: {resp.text[:200]}")
