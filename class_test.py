from kufar_api import Core, SearchConfig
from unittest import TestCase


class TestConfigure(TestCase):

    def setUp(self):
        self.config = SearchConfig()

    def test_configure_init_auto(self):
        # def tests base search request configuration of auto api
        conf_url = 'https://auto.kufar.by/listings?cat=2010&brn=3'
        self.config.configure(conf_url)
        self.assertEqual(self.config.ads_count_api_url,
                         'https://auto.kufar.by/ads-search/v1/engine/v1/search/count',
                         'auto ads count url')
        self.assertEqual(self.config.api_type, 'auto', 'auto api type')
        self.assertEqual(self.config.params,
                         {'cat': ['2010'], 'brn': ['3'], 'size': ['200']},
                         'auto_url_params')
        self.assertEqual(self.config.search_api_url,
                         'https://auto.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated',
                         'search api url auto')

    def test_configure_init_cre_api(self):
        # def tests base search request configuration of cre_api
        conf_url = 'https://www.kufar.by/listings?query=ps4&ot=1&rgn=7'
        self.config.configure(conf_url)
        self.assertEqual(self.config.ads_count_api_url,
                         'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/count',
                         'acre api ads count url')
        self.assertEqual(self.config.api_type, 'cre_api', 'cre api type')
        self.assertEqual(self.config.params,
                         {'query': ['ps4'], 'ot': ['1'], 'rgn': ['7'], 'size': ['200']},
                         'cre api url params')
        self.assertEqual(self.config.search_api_url,
                         'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated',
                         'search api url auto')

    def test_get_ad_owner_info_url(self):
        url = self.config.get_ad_owner_info_url('1234')
        self.assertEqual(url, 'https://www.kufar.by/item/api/aduserinfo/1234', 'id is str')

        url = self.config.get_ad_owner_info_url(1234)
        self.assertEqual(url, 'https://www.kufar.by/item/api/aduserinfo/1234', 'id is int')

    def test_get_user_profile_info_url(self):
        url = self.config.get_user_profile_info_url('1234')
        self.assertEqual(url,
                         'https://profile-api.trust-pro.mpi-internal.com/profile/sdrn:kufar:user:1234', 'id is str')
        url = self.config.get_user_profile_info_url(1234)
        self.assertEqual(url,
                         'https://profile-api.trust-pro.mpi-internal.com/profile/sdrn:kufar:user:1234', 'id is int')

    def test_get_user_avatar_url(self):
        url = self.config.get_user_avatar_url('1234')
        self.assertEqual(url,
                         'https://content.kufar.by/prc_thumbs/12/1234.jpg', 'id is str')
        url = self.config.get_user_avatar_url(1234)
        self.assertEqual(url,
                         'https://content.kufar.by/prc_thumbs/12/1234.jpg', 'id is int')

    def test_get_user_ads_url(self):
        url = self.config.get_user_ads_url('1234')
        self.assertEqual(url,
                         'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'
                         '?size=200&sort=lst.d&atid=1234&lang=ru', 'id is string')

        url = self.config.get_user_ads_url(1234)
        self.assertEqual(url,
                         'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'
                         '?size=200&sort=lst.d&atid=1234&lang=ru', 'id is int')

    def test_get_small_image_url_yams_true(self):
        url = self.config.get_small_image_url('1234', True)
        self.assertEqual(url,
                         'https://yams.kufar.by/api/v1/kufar-ads/images/12/1234.jpg?rule=line_thumbs',
                         'id is str')
        url = self.config.get_small_image_url(1234, True)
        self.assertEqual(url,
                         'https://yams.kufar.by/api/v1/kufar-ads/images/12/1234.jpg?rule=line_thumbs',
                         'id is int')

    def test_get_small_image_url_yams_false(self):
        url = self.config.get_small_image_url('1234', False)
        self.assertEqual(url,
                         'https://content.kufar.by/mobile_thumbs/12/1234.jpg',
                         'id is str')
        url = self.config.get_small_image_url(1234, False)
        self.assertEqual(url,
                         'https://content.kufar.by/mobile_thumbs/12/1234.jpg',
                         'id is int')

    def test_get_large_image_url_yams_true(self):
        url = self.config.get_large_image_url('1234', True)
        self.assertEqual(url,
                         'https://yams.kufar.by/api/v1/kufar-ads/images/12/1234.jpg?rule=gallery',
                         'id is str')
        url = self.config.get_large_image_url(1234, True)
        self.assertEqual(url,
                         'https://yams.kufar.by/api/v1/kufar-ads/images/12/1234.jpg?rule=gallery',
                         'id is int')

    def test_get_large_image_url_yams_false(self):
        url = self.config.get_large_image_url('1234', False)
        self.assertEqual(url,
                         'https://content.kufar.by/gallery/12/1234.jpg',
                         'id is str')
        url = self.config.get_large_image_url(1234, False)
        self.assertEqual(url,
                         'https://content.kufar.by/gallery/12/1234.jpg',
                         'id is int')

class TestCore(TestCase):

    def setUp(self):
        self.testCore = Core()

    def test_get_ads_page(self):
        # url without search request
        self.testCore.set_search_settings('https://www.kufar.by/listings?rgn=7')
        response = self.testCore.get_ads_page()
        self.assertIsInstance(response, dict, 'search request is empty')

        response = self.testCore.get_ads_page('ps4')
        self.assertIsInstance(response, dict, 'search request with query')

    # def test_get_all_ads(self):
    #     # url without search request
    #     self.testCore.set_search_settings('https://www.kufar.by/listings?rgn=7')
    #     response = self.testCore.get_ads_page()
    #     self.assertIsInstance(response, dict, 'search request is empty')
    #
    #     response = self.testCore.get_ads_page('ps4')
    #     self.assertIsInstance(response, dict, 'search request with query')

    # def test_get_ads_count(self):
    #     # url without search request
    #     response = self.testCore.get_ads_page()
    #     self.assertIsInstance(response, dict, 'search request is empty')
    #
    #     response = self.testCore.get_ads_page('ps4')
    #     self.assertIsInstance(response, dict, 'search request with query')



