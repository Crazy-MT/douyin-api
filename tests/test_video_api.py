"""
视频模块 API 测试
测试 api/video.py 中的接口
"""
import unittest
from pprint import pprint

from app import app


class TestVideoAPI(unittest.TestCase):
    """视频相关接口测试"""

    def setUp(self):
        """初始化测试客户端"""
        self.client = app.test_client()

    # ==================== 视频详情接口 ====================

    def test_get_detail(self):
        """测试获取视频详情接口 /aweme/v1/web/aweme/detail/"""
        # 使用一个示例视频 ID
        response = self.client.get('/aweme/v1/web/aweme/detail/?aweme_id=7457492400135621915')
        print('Video Detail Response:')
        pprint(response.get_json())
        # 接口应该返回 200 或 404（视频不存在时）
        self.assertIn(response.status_code, [200, 404])

    def test_get_detail_missing_param(self):
        """测试视频详情接口缺少参数"""
        response = self.client.get('/aweme/v1/web/aweme/detail/')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    # ==================== 相关视频接口 ====================

    def test_get_related(self):
        """测试获取相关视频接口 /aweme/v1/web/aweme/related/"""
        response = self.client.get(
            '/aweme/v1/web/aweme/related/?aweme_id=7457492400135621915&count=10&refresh_index=1'
        )
        print('Related Videos Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    def test_get_related_missing_param(self):
        """测试相关视频接口缺少参数"""
        response = self.client.get('/aweme/v1/web/aweme/related/')
        self.assertEqual(response.status_code, 400)

    def test_get_related_with_filter(self):
        """测试相关视频接口带过滤参数"""
        response = self.client.get(
            '/aweme/v1/web/aweme/related/'
            '?aweme_id=7457492400135621915'
            '&count=10'
            '&refresh_index=2'
            '&filterGids=7457492400135621915'
        )
        print('Related Videos with Filter Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    # ==================== 评论列表接口 ====================

    def test_get_comment_list(self):
        """测试获取评论列表接口 /aweme/v1/web/comment/list/"""
        response = self.client.get(
            '/aweme/v1/web/comment/list/?aweme_id=7457492400135621915&cursor=0&count=20'
        )
        print('Comment List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    def test_get_comment_list_pagination(self):
        """测试评论列表分页"""
        response = self.client.get(
            '/aweme/v1/web/comment/list/?aweme_id=7457492400135621915&cursor=20&count=20'
        )
        print('Comment List Pagination Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    # ==================== 评论回复接口 ====================

    def test_get_reply_list(self):
        """测试获取评论回复接口 /aweme/v1/web/comment/list/reply/"""
        # 需要真实的 item_id 和 comment_id
        response = self.client.get(
            '/aweme/v1/web/comment/list/reply/'
            '?item_id=7457492400135621915'
            '&comment_id=7457500000000000000'
            '&cursor=0'
            '&count=10'
        )
        print('Reply List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    # ==================== 首页瀑布流接口 ====================

    def test_get_module_feed(self):
        """测试获取首页瀑布流接口 /aweme/v2/web/module/feed/"""
        response = self.client.get('/aweme/v2/web/module/feed/?count=20&refresh_index=1')
        print('Module Feed Response:')
        pprint(response.get_json())
        self.assertEqual(response.status_code, 200)

    def test_get_module_feed_with_tag(self):
        """测试首页瀑布流带标签过滤 - 游戏标签"""
        response = self.client.get(
            '/aweme/v2/web/module/feed/?count=10&refresh_index=1&tag_id=300205'
        )
        print('Module Feed with Game Tag Response:')
        pprint(response.get_json())
        self.assertEqual(response.status_code, 200)

    def test_get_module_feed_music_tag(self):
        """测试首页瀑布流带标签过滤 - 音乐标签"""
        response = self.client.get(
            '/aweme/v2/web/module/feed/?count=10&refresh_index=1&tag_id=300209'
        )
        print('Module Feed with Music Tag Response:')
        pprint(response.get_json())
        self.assertEqual(response.status_code, 200)

    # ==================== 推荐页 feed 接口 ====================

    def test_get_tab_feed(self):
        """测试获取推荐页 feed 接口 /aweme/v1/web/tab/feed/"""
        response = self.client.get('/aweme/v1/web/tab/feed/?count=10&refresh_index=1')
        print('Tab Feed Response:')
        pprint(response.get_json())
        self.assertEqual(response.status_code, 200)

    def test_get_tab_feed_pagination(self):
        """测试推荐页 feed 分页"""
        response = self.client.get('/aweme/v1/web/tab/feed/?count=10&refresh_index=2')
        print('Tab Feed Pagination Response:')
        pprint(response.get_json())
        self.assertEqual(response.status_code, 200)

    # ==================== 点赞接口（已注释，暂不测试）====================
    # def test_post_digg(self):
    #     """测试点赞接口 /aweme/v1/web/commit/item/digg/"""
    #     response = self.client.get(
    #         '/aweme/v1/web/commit/item/digg/?aweme_id=7457492400135621915&type=1&item_type=0'
    #     )
    #     print('Digg Response:')
    #     pprint(response.get_json())
    #     self.assertIn(response.status_code, [200, 403])


if __name__ == '__main__':
    unittest.main()
