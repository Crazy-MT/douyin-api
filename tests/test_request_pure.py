# -*- coding: utf-8 -*-
"""测试 Request 类默认使用纯算法"""
import sys
sys.path.insert(0, 'D:/python-project/douyin-api')

from utils.request import Request
import json

print("=== 测试 Request 默认使用纯算法 ===\n")

r = Request()

# 测试 1：普通接口（非 bdms_uris）
print("测试 1：视频详情接口")
uri = '/aweme/v1/web/aweme/detail/'
params = {'aweme_id': '7123456789012345678'}
params = r.get_params(params)

# 调用 getJSON 会自动生成 a_bogus
result = r.getJSON(uri, params)

# getJSON 返回 (response, status_code)
if isinstance(result, tuple):
    response, status = result
else:
    response = result
    status = None

print(f"返回状态: {response.get('status_code') if isinstance(response, dict) else status}")
if isinstance(response, dict) and 'aweme_detail' in response:
    print("SUCCESS - 纯算法生成有效！")
    print(f"返回 keys: {list(response.keys())}")
    if response.get('aweme_detail'):
        print(f"aweme_detail 存在，长度: {len(str(response['aweme_detail']))}")
else:
    print(f"FAIL - 返回类型: {type(response)}")
    if isinstance(response, dict):
        print(f"keys: {list(response.keys())}")
        if 'status_msg' in response:
            print(f"错误信息: {response['status_msg']}")
