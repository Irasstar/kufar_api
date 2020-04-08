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


class SearchConfig:
    def __init__(self):
        self.params = {}
        self.api_type = ''
        self.search_api_url = ''

    def configure(self, url_with_settings):
        parsed_url = urlparse(url_with_settings)
        self.params = parse_qs(parsed_url.query)
        self.params['size'] = ['200']
        if 'auto.kufar' in url_with_settings:
            self.api_type = 'auto'
            self.search_api_url = 'https://auto.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'
        else:
            self.api_type = 'cre_api'
            self.search_api_url = 'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'


class Core:
    """First of all, call configure function to set search settings(category, subcategory, region, price range etc).
    Configure function takes url with config query string(take it from kufar.by after setting all search parameters)"""
    def __init__(self):
        self.settings = SearchConfig()

    def get_ads(self, search_request=''):
        """request self.params['size'] ads"""
        if search_request is not '':
            self.settings.params['query'][0] = search_request
        response = requests.get(self.settings.search_api_url, self.settings.params)
        return response.content.decode()

    def get_all_ads(self, search_request=''):
        ads_count = self.get_ads_count()

    def set_search_settings(self, url):
        self.settings.configure(url)

    def get_ads_count(self, search_request=''):
        api_url = 'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/count'
        response = requests.get(api_url, self.settings.params)
        return response.content.decode()

    def get_small_image(self, image_id):
        pass

    def get_full_size_image(self, image_id):
        pass


if __name__ == "__main__":
    my_core = Core()
    my_core.set_search_settings('https://www.kufar.by/listings?query=%D0%B0%D1%83%D0%B4%D0%B8&ot=1&rgn=7&ar=')
    print(my_core.get_ads('audi'))

