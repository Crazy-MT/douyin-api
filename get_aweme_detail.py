import argparse
import json
from utils.request import Request

parser = argparse.ArgumentParser()
parser.add_argument("aweme_id", help="抖音视频 aweme_id")
args = parser.parse_args()

r = Request()
data, http_status = r.getJSON(
    "/aweme/v1/web/aweme/detail/",
    {"aweme_id": args.aweme_id}
)

print("HTTP_STATUS:", http_status)
print(json.dumps(data, ensure_ascii=False, indent=2))