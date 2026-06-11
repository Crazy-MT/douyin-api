# -*- coding: utf-8 -*-
"""
测试所有可能的关注相关接口
"""
import sys
sys.path.insert(0, 'D:/python-project/douyin-api')

from utils.request import Request

r = Request()

# 可能的关注 feed 接口
uris = [
    '/aweme/v1/web/follow/feed/',  # 关注 feed
    '/aweme/v2/web/follow/feed/',  # v2 版本
    '/aweme/v1/web/tab/feed/',     # 通用 feed（可能支持关注）
]

params_sets = [
    {'cursor': '0', 'level': '1', 'count': '20', 'pull_type': '18', 'refresh_type': '18'},
    {'max_cursor': '0', 'count': '20'},
    {'cursor': '0', 'count': '20'},
]

print("测试所有可能的关注接口:\n")

for uri in uris:
    print(f"\n{'='*60}")
    print(f"接口: {uri}")

    for i, params in enumerate(params_sets, 1):
        print(f"\n  参数组 {i}: {list(params.keys())}")

        result = r.getJSON(uri, params)

        if isinstance(result, tuple):
            response, _ = result
        else:
            response = result

        if isinstance(response, dict) and response:
            keys = list(response.keys())[:5]
            has_data = bool(response.get('aweme_list') or response.get('data'))

            print(f"    Keys: {keys}")
            print(f"    有数据: {has_data}")

            if has_data:
                print(f"\n    ✅ 成功! uri={uri}, params={params}")
                break
        else:
            print(f"    空响应")
    else:
        print(f"  ❌ 该接口所有参数都失败")
