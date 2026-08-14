import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
import sys

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.request import Request


def first_url(obj):
    return ((obj or {}).get("url_list") or [None])[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("aweme_id", help="抖音视频 aweme_id")
    parser.add_argument("--download", nargs="?", const="", help="下载视频，可选输出路径")
    args = parser.parse_args()

    request = Request()
    data, http_status = request.getJSON(
        "/aweme/v1/web/aweme/detail/",
        {"aweme_id": args.aweme_id},
    )

    detail = data.get("aweme_detail") or {}
    author = detail.get("author") or {}
    stats = detail.get("statistics") or {}
    video = detail.get("video") or {}

    fields = {
        "http_status": http_status,
        "status_code": data.get("status_code"),
        "aweme_id": detail.get("aweme_id"),
        "desc": detail.get("desc"),
        "author_nickname": author.get("nickname"),
        "author_uid": author.get("uid"),
        "create_time": datetime.fromtimestamp(detail["create_time"]).strftime("%Y-%m-%d %H:%M:%S")
        if detail.get("create_time")
        else None,
        "duration_ms": detail.get("duration"),
        "digg_count": stats.get("digg_count"),
        "comment_count": stats.get("comment_count"),
        "share_count": stats.get("share_count"),
        "collect_count": stats.get("collect_count"),
        "cover_url": first_url((video.get("cover") or {})),
        "play_url": first_url((video.get("play_addr") or {})),
    }

    output = json.dumps(fields, ensure_ascii=False, indent=2)
    subprocess.run(["pbcopy"], input=output, text=True, check=True)
    print(output)
    print("\n已复制到剪贴板")

    if args.download is not None:
        if not fields["play_url"]:
            raise SystemExit("没有可下载的 play_url")

        path = Path(args.download or f"{args.aweme_id}.mp4")
        headers = request.HEADERS.copy()
        headers["referer"] = f"https://www.douyin.com/video/{args.aweme_id}"

        with httpx.stream(
            "GET",
            fields["play_url"],
            headers=headers,
            cookies=request.COOKIES,
            timeout=60,
            verify=False,
            follow_redirects=True,
        ) as response:
            response.raise_for_status()
            with path.open("wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)

        print(f"已下载: {path}")


if __name__ == "__main__":
    main()
