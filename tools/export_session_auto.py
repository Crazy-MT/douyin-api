# -*- coding: utf-8 -*-
"""
一键导出抖音会话签名材料（CDP 自动化，保证同源）

自动化流程：
1. 启动 Edge 调试模式（用日常 profile 或独立 profile）
2. 打开抖音并等待 secsdk 初始化
3. 同时导出 cookie（含 HttpOnly）+ localStorage 密钥
4. 写入 config/cookie.json + lib/reverse/websign_env.json
5. 验证同源并关闭浏览器

前提：Edge 已关闭（若用日常 profile）

用法：
  python tools/export_session_auto.py [--profile daily]

选项：
  --profile daily    使用日常 Edge profile（需要先完全关闭 Edge）
  不传参数           使用独立调试 profile（首次需扫码登录）
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

try:
    from lib.reverse.cdp2 import CDP
except ImportError:
    print("错误：找不到 lib/reverse/cdp2.py")
    sys.exit(1)


def ev(cdp, expr, timeout=30):
    r = cdp.cmd("Runtime.evaluate",
                {"expression": expr, "returnByValue": True, "awaitPromise": True},
                timeout=timeout)
    res = r.get("result", {})
    if "exceptionDetails" in res:
        return None
    return res.get("result", {}).get("value")


def start_edge(profile_mode='debug'):
    """启动 Edge 调试模式"""
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_exe):
        print(f"错误：找不到 Edge：{edge_exe}")
        sys.exit(1)

    if profile_mode == 'daily':
        # 日常 profile（需先关闭所有 Edge）
        user_data = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")
        print("使用日常 Edge profile（请确保已关闭所有 Edge 窗口）")
    else:
        # 独立调试 profile
        user_data = os.path.expandvars(r"%USERPROFILE%\edge-debug-douyin")
        print("使用独立调试 profile")

    cmd = [
        edge_exe,
        "--remote-debugging-port=9222",
        "--remote-allow-origins=*",
        f"--user-data-dir={user_data}",
        "https://www.douyin.com/?recommend=1"
    ]

    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("启动 Edge... (PID:", proc.pid, ")")
    return proc


def get_ws():
    """获取 douyin 页面的 WebSocket URL"""
    import urllib.request
    for _ in range(15):
        try:
            resp = urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=3)
            pages = json.loads(resp.read().decode())
            for p in pages:
                if 'douyin' in p.get('url', '').lower():
                    return p['webSocketDebuggerUrl']
        except Exception:
            pass
        time.sleep(1)
    return None


def main():
    parser = argparse.ArgumentParser(description='一键导出抖音签名材料（CDP 自动化）')
    parser.add_argument('--profile', choices=['daily', 'debug'], default='debug',
                        help='daily=日常profile, debug=独立profile（默认）')
    args = parser.parse_args()

    print("\n=== 一键导出抖音签名材料（CDP 自动化）===\n")

    # 1. 启动浏览器
    proc = start_edge(args.profile)
    time.sleep(3)

    # 2. 连接 CDP
    ws = get_ws()
    if not ws:
        print("错误：未找到 douyin 页面，请手动打开 https://www.douyin.com")
        proc.terminate()
        sys.exit(1)

    cdp = CDP(ws)
    cdp.cmd("Runtime.enable")
    cdp.cmd("Network.enable")

    print("已连接到抖音页面")
    print("等待 3 秒让 secsdk 初始化...")
    time.sleep(3)

    # 3. 检查登录态
    login_check = ev(cdp, """
        fetch('/aweme/v1/web/aweme/favorite/?count=1')
            .then(r=>r.json())
            .then(d=> d.aweme_list ? 'logged' : 'anon')
            .catch(()=>'err')
    """, timeout=10)
    if login_check != 'logged':
        print("\n⚠️  当前页面未登录或登录态无效")
        print("   请在浏览器里扫码登录抖音，然后按回车继续...")
        input()

    # 4. 导出 localStorage + cookie（document.cookie）
    dump_js = """(function(){
      var ls = {};
      for (var i=0;i<localStorage.length;i++){
        var k=localStorage.key(i);
        ls[k]=localStorage.getItem(k);
      }
      return JSON.stringify({
        localStorage: ls,
        cookie: document.cookie,
        href: location.href,
        ua: navigator.userAgent
      });
    })()"""
    data_str = ev(cdp, dump_js)
    if not data_str:
        print("错误：导出 localStorage 失败")
        cdp.close()
        proc.terminate()
        sys.exit(1)

    env_data = json.loads(data_str)

    # 5. 导出全部 cookie（含 HttpOnly）
    r = cdp.cmd("Network.getAllCookies", {})
    all_cookies = r.get("result", {}).get("cookies", [])
    cookie_jar = {}
    for c in all_cookies:
        dom = c.get("domain", "")
        if "douyin" in dom:
            cookie_jar[c["name"]] = c["value"]

    # 用 CDP 拿到的完整 cookie 覆盖 env_data.cookie（document.cookie 拿不到 HttpOnly）
    env_data["cookie"] = "; ".join(f"{k}={v}" for k, v in cookie_jar.items())

    cdp.close()

    # 6. 验证同源
    env_uid = env_data["localStorage"].get("web_runtime_security_uid", "")
    cookie_uid = cookie_jar.get("x-web-secsdk-uid", "")
    same = (env_uid == cookie_uid and env_uid)

    # 7. 写文件
    env_path = ROOT / "lib" / "reverse" / "websign_env.json"
    cookie_path = ROOT / "config" / "cookie.json"

    json.dump(env_data, open(env_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(cookie_jar, open(cookie_path, "w", encoding="utf-8"), ensure_ascii=False)

    print("\n✅ 导出完成（同一会话，已同源）：")
    print(f"   - {env_path.relative_to(ROOT)}  (secsdk 密钥 + localStorage)")
    print(f"   - {cookie_path.relative_to(ROOT)}  ({len(cookie_jar)} 个 cookie，含 HttpOnly)")
    print(f"   web_runtime_security_uid: {env_uid[:36]}...")
    print(f"   登录态: sessionid={'有' if 'sessionid' in cookie_jar else '无（匿名）'}  "
          f"UIFID={'有' if 'UIFID' in cookie_jar else '无'}")
    print(f"   secsdk 同源: {'✅ 一致' if same else '⚠️  不一致'}")

    # 8. 关闭浏览器
    print("\n浏览器将在 3 秒后关闭...")
    time.sleep(3)
    proc.terminate()
    proc.wait(timeout=5)
    print("完成")


if __name__ == "__main__":
    main()
