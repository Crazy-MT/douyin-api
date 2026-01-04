"""
用户模块 API 测试
测试 api/user.py 中的接口
"""
import unittest
from pprint import pprint

from app import app


class TestUserAPI(unittest.TestCase):
    """用户相关接口测试"""

    def setUp(self):
        """初始化测试客户端"""
        self.client = app.test_client()
        # 测试用的 sec_user_id（可根据实际情况修改）
        self.test_sec_user_id = 'MS4wLjABAAAAuWb40KLM29J4hu2eXKN5GSZ8k3hdsZHRQ6CUNiW4OAY'
        self.test_user_id = '123456789'

    # ==================== 用户信息接口 ====================

    def test_get_user_info_self(self):
        """测试获取自己的用户信息 /aweme/v1/web/user/profile/self/"""
        response = self.client.get('/aweme/v1/web/user/profile/self/')
        print('User Self Info Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_user_info(self):
        """测试获取其他用户信息 /aweme/v1/web/user/profile/other/"""
        response = self.client.get(
            f'/aweme/v1/web/user/profile/other/?sec_user_id={self.test_sec_user_id}'
        )
        print('User Other Info Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    # ==================== 用户作品列表接口 ====================

    def test_get_user_post(self):
        """测试获取用户作品列表 /aweme/v1/web/aweme/post/"""
        response = self.client.get(
            f'/aweme/v1/web/aweme/post/'
            f'?sec_user_id={self.test_sec_user_id}'
            f'&count=10'
            f'&max_cursor=0'
        )
        print('User Post List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_user_post_with_locate(self):
        """测试获取用户作品列表带定位参数"""
        response = self.client.get(
            f'/aweme/v1/web/aweme/post/'
            f'?sec_user_id={self.test_sec_user_id}'
            f'&count=10'
            f'&max_cursor=0'
            f'&locate_query=true'
            f'&need_time_list=1'
        )
        print('User Post with Locate Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_user_post_locate(self):
        """测试获取用户作品当前视频列表 /aweme/v1/web/locate/post/"""
        response = self.client.get(
            f'/aweme/v1/web/locate/post/'
            f'?sec_user_id=MS4wLjABAAAA3q_M7SAG4eQnFrskafFBDLnycg_2s21oi7Q_aI42C2Q'
            f'&count=10'
            f'&max_cursor=0'
            f'&locate_query=true'
        )
        print('User Post Locate Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    # ==================== 用户喜欢列表接口 ====================

    def test_get_user_favorite(self):
        """测试获取用户喜欢列表 /aweme/v1/web/aweme/favorite/"""
        response = self.client.get(
            f'/aweme/v1/web/aweme/favorite/'
            f'?sec_user_id={self.test_sec_user_id}'
            f'&count=18'
            f'&max_cursor=0'
            f'&min_cursor=0'
        )
        print('User Favorite List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    # ==================== 收藏相关接口 ====================

    def test_get_list_collection(self):
        """测试获取用户收藏视频列表 /aweme/v1/web/aweme/listcollection/"""
        response = self.client.get('/aweme/v1/web/aweme/listcollection/?count=10&cursor=0')
        print('Collection List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_list_collection_music(self):
        """测试获取收藏的音乐 /aweme/v1/web/music/listcollection/"""
        response = self.client.get('/aweme/v1/web/music/listcollection/?count=18&cursor=0')
        print('Music Collection Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    def test_get_list_collects(self):
        """测试获取收藏夹列表 /aweme/v1/web/collects/list/"""
        response = self.client.get('/aweme/v1/web/collects/list/?count=18&cursor=0')
        print('Collects List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    def test_get_list_collects_video(self):
        """测试获取收藏夹视频信息 /aweme/v1/web/collects/video/list/"""
        # 需要真实的 collects_id
        response = self.client.get(
            '/aweme/v1/web/collects/video/list/?collects_id=7417883349374637865&count=18&cursor=0'
        )
        print('Collects Video List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    def test_get_list_collection_mix(self):
        """测试获取收藏的合集 /aweme/v1/web/mix/listcollection/"""
        response = self.client.get('/aweme/v1/web/mix/listcollection/?count=10&cursor=0')
        print('Mix Collection Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    def test_get_list_collection_series(self):
        """测试获取收藏的短剧 /aweme/v1/web/series/collections"""
        response = self.client.get('/aweme/v1/web/series/collections/?count=10&cursor=0')
        print('Series Collection Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    # ==================== 合集相关接口 ====================

    def test_get_mix_list(self):
        """测试获取用户创建的合集 /aweme/v1/web/mix/list/"""
        response = self.client.get(
            f'/aweme/v1/web/mix/list/'
            f'?sec_user_id={self.test_sec_user_id}'
            f'&count=10'
            f'&cursor=0'
        )
        print('Mix List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_mix_detail(self):
        """测试获取合集详情 /aweme/v1/web/mix/detail/"""
        response = self.client.get('/aweme/v1/web/mix/detail/?mix_id=7133033459831801863')
        print('Mix Detail Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_mix_list_detail(self):
        """测试获取合集视频列表 /aweme/v1/web/mix/aweme/"""
        response = self.client.get(
            '/aweme/v1/web/mix/aweme/?mix_id=7133033459831801863&count=10&cursor=0'
        )
        print('Mix Aweme List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    # ==================== 历史记录接口 ====================

    def test_get_view_user_visited_list(self):
        """测试获取查看用户列表 /aweme/v1/web/view/user/visited/list/"""
        response = self.client.get('/aweme/v1/web/view/user/visited/list/?count=10&cursor=0')
        print('View User Visited List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_history_read(self):
        """测试获取观看历史 /aweme/v1/web/history/read/"""
        response = self.client.get(
            '/aweme/v1/web/history/read/'
            '?count=20'
            '&max_cursor=0'
            '&directory=0'
            '&category=0'
            '&status=-1'
        )
        print('History Read Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_history_read_with_filter(self):
        """测试获取观看历史带过滤条件"""
        # 筛选：未看完、1-3分钟、音乐类
        response = self.client.get(
            '/aweme/v1/web/history/read/'
            '?count=20'
            '&max_cursor=0'
            '&directory=2'
            '&category=2'
            '&status=0'
        )
        print('History Read with Filter Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_lvideo_history_read(self):
        """测试获取影视综观看记录 /aweme/v1/web/lvideo/query/history/"""
        response = self.client.get('/aweme/v1/web/lvideo/query/history/?count=20&cursor=0')
        print('Lvideo History Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    # ==================== 用户关系接口 ====================

    def test_get_relation(self):
        """测试获取用户关系列表 /aweme/v1/web/im/spotlight/relation/"""
        import time
        current_time = int(time.time())
        response = self.client.get(
            f'/aweme/v1/web/im/spotlight/relation/'
            f'?count=20'
            f'&max_time={current_time}'
            f'&min_time=0'
        )
        print('Relation List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_user_following(self):
        """测试获取用户关注列表 /aweme/v1/web/user/following/list/"""
        response = self.client.get(
            f'/aweme/v1/web/user/following/list/'
            f'?user_id={self.test_user_id}'
            f'&sec_user_id={self.test_sec_user_id}'
            f'&count=20'
            f'&offset=0'
            f'&source_type=4'
        )
        print('Following List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_user_following_recent(self):
        """测试获取用户关注列表 - 最近关注"""
        response = self.client.get(
            f'/aweme/v1/web/user/following/list/'
            f'?user_id={self.test_user_id}'
            f'&sec_user_id={self.test_sec_user_id}'
            f'&count=20'
            f'&offset=0'
            f'&source_type=1'
        )
        print('Following List Recent Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    def test_get_user_follower(self):
        """测试获取粉丝列表 /aweme/v1/web/user/follower/list/"""
        response = self.client.get(
            f'/aweme/v1/web/user/follower/list/'
            f'?user_id={self.test_user_id}'
            f'&sec_user_id={self.test_sec_user_id}'
            f'&count=20'
            f'&offset=0'
        )
        print('Follower List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    # ==================== 用户主页搜索接口 ====================

    def test_get_search_item(self):
        """测试用户主页搜索 /aweme/v1/web/home/search/item/"""
        response = self.client.get(
            '/aweme/v1/web/home/search/item/'
            '?search_channel=aweme_personal_home_video'
            '&keyword=测试'
            '&count=10'
            '&offset=0'
        )
        print('Search Item Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    def test_get_search_item_favorite(self):
        """测试用户主页搜索 - 喜欢的视频"""
        response = self.client.get(
            '/aweme/v1/web/home/search/item/'
            '?search_channel=aweme_favorite_video'
            '&keyword=音乐'
            '&count=10'
            '&offset=0'
        )
        print('Search Favorite Item Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    def test_get_search_item_collect(self):
        """测试用户主页搜索 - 收藏的视频"""
        response = self.client.get(
            '/aweme/v1/web/home/search/item/'
            '?search_channel=aweme_collect_video'
            '&keyword=游戏'
            '&count=10'
            '&offset=0'
        )
        print('Search Collect Item Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 404])

    # ==================== 关注 feed 接口 ====================

    def test_get_follow_feed(self):
        """测试获取关注用户的视频 /aweme/v1/web/follow/feed/"""
        response = self.client.get(
            '/aweme/v1/web/follow/feed/'
            '?cursor=0'
            '&level=1'
            '&count=20'
            '&pull_type=18'
            '&refresh_type=18'
        )
        print('Follow Feed Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    # ==================== 稍后再看接口 ====================

    def test_get_watchlater_list(self):
        """测试获取稍后再看记录 /aweme/v1/web/watchlater/list/"""
        response = self.client.get(
            '/aweme/v1/web/watchlater/list/?offset=0&list_type=0&operate_type=0'
        )
        print('Watchlater List Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])

    # ==================== 熟悉联系人接口 ====================

    def test_get_familiar_atlist(self):
        """测试获取熟悉联系人列表 /aweme/v1/web/familiar/atlist/"""
        response = self.client.get(
            '/aweme/v1/web/familiar/atlist/?count=20&cursor=0&scene=2&group_id=7586334306945207609'
        )
        print('Familiar Atlist Response:')
        pprint(response.get_json())
        self.assertIn(response.status_code, [200, 403])


if __name__ == '__main__':
    unittest.main()
