# -*- encoding: utf-8 -*-
'''
@File    :   request.py
@Time    :   2024年07月15日
@Author  :   erma0
@Version :   1.1
@Link    :   参考   https://github.com/ShilongLee/Crawler/blob/main/service/douyin/logic/common.py
@Desc    :   抖音sign
'''
import json
import os
import random
import re
import subprocess
from urllib.parse import quote

import httpx
from loguru import logger

from utils.cookies import get_cookie_dict
from utils.execjs_fix import execjs


# import requests


class Request(object):
    HOST = 'https://www.douyin.com'
    LIVE_HOST = 'https://live.douyin.com'
    WEB2_HOST = 'https://www-hj.douyin.com'
    PARAMS = {
        'device_platform': 'webapp',
        'aid': '6383',
        'channel': 'channel_pc_web',
        'update_version_code': '170400',
        'pc_client_type': '1',  # Windows
        'version_code': '190500',
        'version_name': '19.5.0',
        'cookie_enabled': 'true',
        'screen_width': '2560',  # from cookie dy_swidth
        'screen_height': '1440',  # from cookie dy_sheight
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Chrome',
        'browser_version': '126.0.0.0',
        'browser_online': 'true',
        'engine_name': 'Blink',
        'engine_version': '126.0.0.0',
        'os_name': 'Windows',
        'os_version': '10',
        'cpu_core_num': '24',  # device_web_cpu_core
        'device_memory': '8',  # device_web_memory_size
        'platform': 'PC',
        'downlink': '10',
        'effective_type': '4g',
        'round_trip_time': '50',
        # 'webid': '',   # from doc
        # 'verifyFp': '',   # from cookie s_v_web_id
        # 'fp': '', # from cookie s_v_web_id
        # 'msToken': '',  # from cookie msToken
        # 'a_bogus': '' # sign
    }
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "referer": "https://www.douyin.com/?recommend=1",
        "priority": "u=1, i",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "accept": "application/json, text/plain, */*",
        "dnt": "1",
    }
    filepath = os.path.dirname(__file__)
    SIGN = execjs.compile(
        open(os.path.join(filepath, '../lib/douyin.js'), 'r', encoding='utf-8').read())
    WEBID = ''
    client = httpx.Client(
        proxies=None,
        timeout=30.0,
        verify=False,
        follow_redirects=True
    )

    def __init__(self, cookie='', UA=''):
        self.COOKIES = get_cookie_dict(cookie)
        if UA:  # 如果需要访问搜索页面源码等内容，需要提供cookie对应的UA
            version = UA.split(' Chrome/')[1].split(' ')[0]
            _version = version.split('.')[0]
            self.HEADERS.update({
                "User-Agent": UA,  # 主要是这个
                "sec-ch-ua": f'"Chromium";v="{_version}", "Not(A:Brand";v="24", "Google Chrome";v="{_version}"',
            })
            self.PARAMS.update({
                "browser_version": version,
                "engine_version": version,  # 主要是这个
            })

    def get_sign(self, uri: str, params: dict) -> dict:
        query = '&'.join([f'{k}={quote(str(v))}' for k, v in params.items()])
        call_name = 'sign_datail'
        if 'reply' in uri:
            call_name = 'sign_reply'
        a_bogus = self.SIGN.call(
            call_name, query, self.HEADERS.get("User-Agent"))
        return a_bogus

    def get_sign_bdms(self, uri: str, params: dict) -> str:
        """使用 bdms 方案生成 a_bogus 签名（通过 Node.js 子进程）"""
        query = '&'.join([f'{k}={quote(str(v))}' for k, v in params.items()])
        url = f'{self.HOST}{uri}?{query}'
        uifid = self.COOKIES.get('UIFID', '')

        # 使用 subprocess 调用 Node.js
        js_path = os.path.join(self.filepath, '../lib/index.js')
        # Windows 路径转为正斜杠，避免转义问题
        js_path = js_path.replace('\\', '/')
        js_code = f'''
const {{ get_a_bogus }} = require("{js_path}");
const result = get_a_bogus({json.dumps(url)}, {json.dumps(uifid)});
if (global._process) global.process = global._process;
console.log(JSON.stringify({{ a_bogus: result }}));
process.exit(0);
'''
        try:
            result = subprocess.run(
                ['node', '-e', js_code],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.path.dirname(js_path)
            )
            if result.returncode == 0:
                # 从输出中提取 JSON 结果
                for line in result.stdout.strip().split('\n'):
                    if line.startswith('{'):
                        data = json.loads(line)
                        a_bogus = data.get('a_bogus', '')
                        if a_bogus:
                            return a_bogus
                # 没找到 a_bogus，打印完整输出便于调试
                print(f"Node.js stdout: {result.stdout}")
                print(f"Node.js stderr: {result.stderr}")
            else:
                print(f"Node.js error (code={result.returncode}):")
                print(f"  stdout: {result.stdout}")
                print(f"  stderr: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("Node.js timeout")
        except Exception as e:
            print(f"Error calling Node.js: {e}")
        return ''

    def get_params(self, params: dict) -> dict:
        params.update(self.PARAMS)
        params['msToken'] = self.get_ms_token()
        params['screen_width'] = self.COOKIES.get('dy_swidth', 2560)
        params['screen_height'] = self.COOKIES.get('dy_sheight', 1440)
        params['cpu_core_num'] = self.COOKIES.get('device_web_cpu_core', 24)
        params['device_memory'] = self.COOKIES.get('device_web_memory_size', 8)
        params['verifyFp'] = self.COOKIES.get('s_v_web_id', None)
        params['fp'] = self.COOKIES.get('s_v_web_id', None)
        params['uifid'] = self.COOKIES.get('UIFID', None)
        params['webid'] = self.get_webid()
        return params

    def get_webid(self):
        if not self.WEBID:
            url = 'https://www.douyin.com/?recommend=1'
            text = self.getHTML(url)
            pattern = r'\\"user_unique_id\\":\\"(\d+)\\"'
            match = re.search(pattern, text)
            if match:
                self.WEBID = match.group(1)
        return self.WEBID

    def get_ms_token(self, randomlength=120):
        """
        返回cookie中的msToken或随机字符串
        """
        ms_token = self.COOKIES.get('msToken', None)
        if not ms_token:
            ms_token = ''
            base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
            length = len(base_str) - 1
            for _ in range(randomlength):
                ms_token += base_str[random.randint(0, length)]
        return ms_token

    def getHTML(self, url) -> str:
        headers = self.HEADERS.copy()
        headers['sec-fetch-dest'] = 'document'
        response = self.client.get(url, headers=headers, cookies=self.COOKIES)
        if response.status_code != 200 or response.text == '':
            logger.error(f'HTML请求失败, url: {url}, header: {headers}')
            return ''
        return response.text

    def getJSON(self, uri: str, params: dict, data: dict = None, live=None, web2=None):
        url = f'{self.HOST}{uri}'
        live_url = f'{self.LIVE_HOST}{uri}'
        web2_url = f'{self.WEB2_HOST}{uri}'
        params = self.get_params(params)
        # 特定接口使用 bdms 签名
        if uri in ['/aweme/v2/web/module/feed/', '/aweme/v1/web/locate/post/', '/aweme/v1/web/commit/item/digg/',
                   '/aweme/v1/web/aweme/favorite/']:
            params["a_bogus"] = self.get_sign_bdms(web2_url, params)
            print("params['a_bogus']", params["a_bogus"])
        else:
            params["a_bogus"] = self.get_sign(uri, params)

        # 这个接口必须更改referer的值为当前请求页面的url
        referer_map = {
            '/aweme/v1/web/aweme/related/': f"https://www.douyin.com/video/{params.get('aweme_id')}",
            '/aweme/v1/web/comment/list/': f"https://www.douyin.com/video/{params.get('aweme_id')}",
            '/aweme/v1/web/comment/list/reply/': f"https://www.douyin.com/video/{params.get('item_id')}",
            '/aweme/v1/web/user/profile/other/': f"https://www.douyin.com/user/{params.get('sec_user_id')}?",
            '/aweme/v1/web/aweme/post/': f"https://www.douyin.com/user/{params.get('sec_user_id')}?",
            '/aweme/v1/web/locate/post/': f"https://www.douyin.com/",
            '/aweme/v1/web/im/spotlight/relation/': f"https://www.douyin.com/user/",
            '/aweme/v1/web/user/following/list/': f"https://www.douyin.com/user/",
            '/aweme/v1/web/user/follower/list/': f"https://www.douyin.com/user/",
            '/aweme/v1/web/aweme/favorite/': f"https://www.douyin.com/",
            '/aweme/v1/web/aweme/listcollection/': f"https://www.douyin.com/user/self?from_tab_name=main&showTab=favorite_collection",
            '/aweme/v1/web/music/listcollection/': f"https://www.douyin.com/user/self?from_tab_name=main&showSubTab=music&showTab=favorite_collection",
            '/aweme/v1/web/collects/video/list/': f"https://www.douyin.com/user/self?from_tab_name=main&showSubTab=favorite_folder&showTab=favorite_collection",
            '/aweme/v1/web/collects/list/': f"https://www.douyin.com/user/self?from_tab_name=main&showSubTab=favorite_folder&showTab=favorite_collection",
            '/aweme/v1/web/mix/listcollection/': f"https://www.douyin.com/user/self?from_tab_name=main&showSubTab=favorite_folder&showTab=favorite_collection",
            '/aweme/v1/web/series/collections': f"https://www.douyin.com/user/self?from_tab_name=main&showSubTab=favorite_folder&showTab=favorite_collection",
            '/aweme/v1/web/mix/list/': f"https://www.douyin.com/user/",
            '/aweme/v1/web/home/search/item/': f"https://www.douyin.com/user/",
            '/aweme/v1/web/seo/inner/link/': f"https://www.douyin.com/user/",
            '/aweme/v2/web/module/feed/': f"https://www.douyin.com/jingxuan",
        }
        for pattern, referer_value in referer_map.items():
            if pattern == uri:
                self.HEADERS['referer'] = referer_value
                break

        # 需要 POST 的接口列表
        post_uris = ['/aweme/v2/web/module/feed/']

        if data is not None or uri in post_uris:
            bd_client_data = self.COOKIES.get("bd_ticket_guard_client_data", None)
            self.HEADERS["Content-Type"] = "application/x-www-form-urlencoded"
            self.HEADERS["Uifid"] = self.COOKIES.get("UIFID", None)
            # self.HEADERS["Bd-Ticket-Guard-Client-Data"] = bd_client_data
            # self.HEADERS["Bd-Ticket-Guard-Web-Version"] = '1'
            # self.HEADERS["Bd-Ticket-Guard-Version"] = '2'
            # self.HEADERS["Bd-Ticket-Guard-Iteration-Version"] = '1'
            self.HEADERS["X-Secsdk-Csrf-Token"] = 'DOWNGRADE'
            # POST 请求时也要判断是否使用 web2
            if web2:
                post_headers = self.HEADERS.copy()
                post_headers['sec-fetch-site'] = 'same-site'
                post_headers['origin'] = 'https://www.douyin.com'
                response = self.client.post(
                    web2_url, params=params, data=data or {}, headers=post_headers, cookies=self.COOKIES)
                actual_url = web2_url
            else:
                response = self.client.post(
                    url, params=params, data=data or {}, headers=self.HEADERS, cookies=self.COOKIES)
                actual_url = url
            print(f'POST url:{response.url}, code:{response.status_code}')
        elif live:
            response = self.client.get(
                live_url, params=params, headers=self.HEADERS, cookies=self.COOKIES)
            print(f'url:{response.url}, code:{response.status_code}')
            actual_url = live_url
        elif web2:
            # web2 请求需要修改 headers（跨子域名）
            web2_headers = self.HEADERS.copy()
            web2_headers['sec-fetch-site'] = 'same-site'
            web2_headers['origin'] = 'https://www.douyin.com'
            response = self.client.get(
                web2_url, params=params, headers=web2_headers, cookies=self.COOKIES)
            print(f'url:{response.url}, code:{response.status_code}')
            actual_url = web2_url
        else:
            response = self.client.get(
                url, params=params, headers=self.HEADERS, cookies=self.COOKIES)
            # print(f'url:{response.url}, header:{self.HEADERS}')
            actual_url = url
        if response.status_code != 200 or response.text == '':
            logger.error(
                f'JSON请求失败：url: {actual_url},  params: {params},header: {self.HEADERS}, code: {response.status_code}, body: {response.text[:500] if response.text else "empty"}')
            return {}
        return response.json()


if __name__ == "__main__":
    r = Request()
    print(r.get_webid())
