# kufar.by api url:

# search
# https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated
# parameters:
# ?query=iphone&ot=1&cat=17010&size=200&lang=ru&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30=
# cursor - current page token
# size - ads quantity
# cat - category

# ads count request
# https://cre-api.kufar.by/ads-search/v1/engine/v1/search/count
# parameters
# ?cur=BYR&rgn=7&size=42&sort=lst.d&query=

# ad user info request
# https://www.kufar.by/item/api/aduserinfo/2499605
# 2499605 - user id

# get image request
# https://yams.kufar.by/api/v1/kufar-ads/images/51/5189867070.jpg?rule=gallery
# rule=gallery - full size image
# rule=line_thumbs - small image
# 5189867070.jpg - image name
# /51/ - first two number of image name

import requests
from urllib.parse import urlparse, parse_qs
import re


class SearchConfig:
    def __init__(self):
        self.params = {}
        self.api_type = ''
        self.search_api_url = ''
        self.ads_count_api_url = ''

    def configure(self, url_with_settings):
        parsed_url = urlparse(url_with_settings)
        self.params = parse_qs(parsed_url.query)
        self.params['size'] = ['200']
        # main api url configure
        if 'auto.kufar' in url_with_settings:
            self.api_type = 'auto'
            self.search_api_url = 'https://auto.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'
        else:
            self.api_type = 'cre_api'
            self.search_api_url = 'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'
        self.ads_count_api_url = re.sub(r'(rendered-paginated)', 'count', self.search_api_url)

    @staticmethod
    def get_user_info_url(user_id):
        return f'https://www.kufar.by/item/api/aduserinfo/{user_id}'

    @staticmethod
    def get_small_size_image_url(image_id):
        str_image_id = str(image_id)
        return f'https://yams.kufar.by/api/v1/kufar-ads/images/{str_image_id[:2]}/{str_image_id}.jpg?rule=line_thumbs'

    @staticmethod
    def get_full_size_image_url(image_id):
        str_image_id = str(image_id)
        return f'https://yams.kufar.by/api/v1/kufar-ads/images/{str_image_id[:2]}/{str_image_id}.jpg?rule=gallery'


class Core:
    """First of all, call configure function to set search settings(category, subcategory, region, price range etc).
    Configure function takes url with config query string(take it from kufar.by after setting all search parameters)"""
    def __init__(self):
        self.settings = SearchConfig()

    def get_ads_page(self, search_request=''):
        """function request json with self.params['size'] ads"""
        if search_request is not '':
            self.settings.params.update({'query': [search_request]})
        response = requests.get(self.settings.search_api_url, self.settings.params)
        return response.json()

    def get_all_ads(self, search_request='', pages_count=-1):
        content = []
        while True:
            response = self.get_ads_page(search_request)
            content.extend(response['ads'])
            next_page_not_exists = True
            for page in response['pagination']['pages']:
                if page['label'] == 'next':
                    self.settings.params.update({'cursor': [page['token']]})
                    next_page_not_exists = False
            if next_page_not_exists:
                del self.settings.params['cursor']
                return content

    def set_search_settings(self, url):
        self.settings.configure(url)

    def get_ads_count(self, search_request=''):
        api_url = 'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/count'
        response = requests.get(api_url, self.settings.params)
        return response.json()

    def get_user_info(self, user_id):
        pass

    def get_small_image(self, image_id):
        pass

    def get_full_size_image(self, image_id):
        pass


if __name__ == "__main__":
    #blablabla
    my_core = Core()
    my_core.set_search_settings('https://www.kufar.by/listings?query=%D0%B0%D1%83%D0%B4%D0%B8&ot=1&rgn=7&ar=')
    print(my_core.get_ads('audi'))
