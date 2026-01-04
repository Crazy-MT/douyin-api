import unittest
from pprint import pprint

from app import app


class TestCase(unittest.TestCase):
    # 初始化测试客户端
    def setUp(self):
        self.client = app.test_client()

    # 测试 /aweme/v1/web/seo/inner/link 路由
    def test_get_seo_link(self):
        response = self.client.get('/aweme/v1/web/seo/inner/link/')
        print("SEO Link Response:")  # 打印返回的 JSON 数据
        pprint(response.get_json())
        self.assertEqual(response.status_code, 200)

    # 测试 /aweme/v1/web/emoji/list 路由
    def test_get_emoji_list(self):
        response = self.client.get('/aweme/v1/web/emoji/list/')
        print("Emoji List Response:")  # 打印返回的 JSON 数据
        pprint(response.get_json())
        self.assertEqual(response.status_code, 200)

    # 测试 '/aweme/v1/web/im/resources/emoticon/trending'
    def test_get_emoticon_list(self):
        response = self.client.get('/aweme/v1/web/im/resources/emoticon/trending?cursor=0&count=80')
        print("emoticon List Response:")  # 打印返回的 JSON 数据
        pprint(response.get_json())
        self.assertEqual(response.status_code, 200)

    # 测试/aweme/v1/web/tab/feed/
    def test_get_recommend_list(self):
        response = self.client.get('/aweme/v1/web/tab/feed/?count=10')
        print('Recommend List Res')
        pprint(response.get_json())
        self.assertEqual(response.status_code, 200)

    # 测试/aweme/v1/web/hot/search/list/
    def test_get_hot_list(self):
        res = self.client.get('/aweme/v1/web/hot/search/list/')
        self.assertEqual(res.status_code, 200)
        print('Hot list value:')
        pprint(res.get_json())

    # 测试/aweme/v1/web/api/suggest_words/
    def test_get_suggest_words(self):
        res = self.client.get('/aweme/v1/web/api/suggest_words/?query=雍华盛会警察到九楼后续&count=8')
        self.assertEqual(res.status_code, 200)
        print('suggest_words value:')
        pprint(res.get_json())

    # 测试/aweme/v1/web/tab/feed/
    def test_get_tab_feed(self):
        res = self.client.get('/aweme/v1/web/tab/feed/?&count=10&refresh_index=1')
        self.assertEqual(res.status_code, 200)
        print('tab_feed value:')
        pprint(res.get_json())

    # '/aweme/v1/web/user/profile/self/'
    def test_get_user_info_self(self):
        res = self.client.get('/aweme/v1/web/user/profile/self/')
        self.assertEqual(res.status_code, 200)
        print('user value:')
        pprint(res.get_json())

    # '/aweme/v1/web/aweme/listcollection/
    def test_post_listcollection(self):
        res = self.client.get('/aweme/v1/web/aweme/listcollection/?count=10&cursor=0')
        self.assertEqual(res.status_code, 200)
        print('commit value:')
        pprint(res.get_json())

    # '/aweme/v1/web/commit/item/digg/'
    # def test_commit_digg(self):
    #     res = self.client.get('/aweme/v1/web/commit/item/digg/?aweme_id=7457492400135621915&type=0&item_type=0')
    #     self.assertEqual(res.status_code, 200)
    #     print('commit value:')
    #     pprint(res.get_json())

    # '/aweme/v1/web/home/channel/setting/'
    def test_get_channel_setting(self):
        res = self.client.get('/aweme/v1/web/home/channel/setting/')
        self.assertEqual(res.status_code, 200)
        print('channel_setting value:')
        pprint(res.get_json())

    # '/aweme/v2/web/module/feed/'
    def test_get_module_feed(self):
        res = self.client.get('/aweme/v2/web/module/feed/?count=20&refresh_index=1')
        self.assertEqual(res.status_code, 200)
        print('module_feed value:')
        pprint(res.get_json())

    # '/aweme/v1/web/locate/post/'
    def test_get_locate_post(self):
        res = self.client.get('/aweme/v1/web/locate/post/?sec_user_id=&count=10'
                              '&max_cursor=1763284616000&locate_query=true'
                              '&locate_item_id=7547271075232337212&locate_item_cursor=1757235984000')
        self.assertEqual(res.status_code, 200)
        print('locate_post value:')
        pprint(res.get_json())

    # '/aweme/v1/web/view/user/visited/list/'
    def test_get_view_user_visited_list(self):
        res = self.client.get('/aweme/v1/web/view/user/visited/list/?count=10&cursor=0')
        self.assertEqual(res.status_code, 200)
        print('view_user_visited_list value:')
        pprint(res.get_json())

    # '/aweme/v1/web/mix/detail/'
    def test_get_mix_detail(self):
        # 注意：这里需要一个真实的mix_id来测试，目前使用占位符
        res = self.client.get('/aweme/v1/web/mix/detail/?mix_id=7133033459831801863')
        # 由于缺少有效的mix_id，可能返回403或其他错误状态码
        print('mix_detail value:')
        pprint(res.get_json())

    # '/aweme/v1/web/watchlater/list/'
    def test_get_watchlater_list(self):
        res = self.client.get('/aweme/v1/web/watchlater/list/?offset=0&list_type=0&operate_type=0')
        print('watchlater_list value:')
        pprint(res.get_json())

    # '/aweme/v1/web/mix/list/'
    def test_get_mix_list(self):
        # 注意：这里需要一个真实的sec_user_id来测试，目前使用占位符
        res = self.client.get('/aweme/v1/web/mix/list/?sec_user_id=MS4wLjABAAAAuWb40KLM29J4hu2eXKN5GSZ8k3hdsZHRQ6CUNiW4OAY&count=10&cursor=0')
        print('mix_list value:')
        pprint(res.get_json())

    # '/aweme/v1/web/familiar/atlist/'
    def test_get_familiar_atlist(self):
        # 测试获取熟悉联系人列表（AT列表）
        res = self.client.get('/aweme/v1/web/familiar/atlist/?count=20&cursor=0&scene=2&group_id=7586334306945207609')
        print('familiar_atlist value:')
        pprint(res.get_json())


if __name__ == '__main__':
    unittest.main()
