"""
直播模块 API 测试
测试直播相关接口
"""
import unittest
from pprint import pprint

from app import app


class TestLiveAPI(unittest.TestCase):
    """直播相关接口测试"""

    def setUp(self):
        """初始化测试客户端"""
        self.client = app.test_client()

    # ==================== 直播间信息接口 ====================

    def test_get_live_info(self):
        """测试获取直播推流信息 /aweme/v1/web/webcast/room/info_by_scene/"""
        res = self.client.get('/aweme/v1/web/webcast/room/info_by_scene/?room_id=7418107379843173154')
        self.assertEqual(res.status_code, 200)
        print('live_info value:')
        pprint(res.get_json())

    # ==================== 直播观看记录接口 ====================

    def test_get_webcast_history_read(self):
        """测试获取直播观看记录 /webcast/feed/"""
        response = self.client.get('/aweme/v1/web/webcast/feed/?max_time=0')
        print('Webcast History Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])


if __name__ == '__main__':
    unittest.main()
