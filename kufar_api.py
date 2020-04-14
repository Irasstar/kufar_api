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


class WrongArgsCombinationError(Exception):
    """raises when you set wrong combination of a function parameters"""
    def __str__(self):
        return 'Be careful! Set wrong combination of function args.'


class SearchConfig:
    def __init__(self):
        self.params = {}
        self.api_type = ''
        self.search_api_url = ''
        self.ads_count_api_url = ''

# >>> ads search request configuration part starts

    def configure(self, url_with_settings):
        # init ads search settings (category, cost etc)
        parsed_url = urlparse(url_with_settings)
        self.params = parse_qs(parsed_url.query)
        # exclude search query from config.
        if self.params.get('query') is not None:
            del self.params['query']
        self.params['size'] = ['200']
        # main api url configure
        if 'auto.kufar' in url_with_settings:
            self.api_type = 'auto'
            self.search_api_url = 'https://auto.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'
        else:
            self.api_type = 'cre_api'
            self.search_api_url = 'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'
        # set ads count URL
        self.ads_count_api_url = re.sub(r'(rendered-paginated)', 'count', self.search_api_url)

# <<< ads search request configuration part finish

# >>> user urls part starts
    @staticmethod
    def get_ad_owner_info_url(user_id):
        # response difference is user ads count and avatar id instead direct link in get_user_profile_info
        return f'https://www.kufar.by/item/api/aduserinfo/{user_id}'

    @staticmethod
    def get_user_profile_info_url(user_id):
        # I think this request is useless except "communication info"
        return f'https://profile-api.trust-pro.mpi-internal.com/profile/sdrn:kufar:user:{user_id}'

# <<< user urls part finish

# ads + images part start
    @staticmethod
    def get_user_avatar_url(image_id):
        str_image_id = str(image_id)
        return f'https://content.kufar.by/prc_thumbs/{str_image_id[:2]}/{str_image_id}.jpg'

    @staticmethod
    def get_user_ads_url(user_id):
        return f'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated' \
               f'?size=200&sort=lst.d&atid={user_id}&lang=ru'

    @staticmethod
    def get_small_image_url(image_id, is_yams_storage=True):
        str_image_id = str(image_id)
        if is_yams_storage:
            return f'https://yams.kufar.by/api/v1/kufar-ads/images/{str_image_id[:2]}/{str_image_id}.jpg' \
                   f'?rule=line_thumbs'
        else:
            return f'https://content.kufar.by/mobile_thumbs/{str_image_id[:2]}/{str_image_id}.jpg'

    @staticmethod
    def get_large_image_url(image_id, is_yams_storage=True):
        str_image_id = str(image_id)
        if is_yams_storage:
            return f'https://yams.kufar.by/api/v1/kufar-ads/images/{str_image_id[:2]}/{str_image_id}.jpg?rule=gallery'
        else:
            return f'https://content.kufar.by/gallery/{str_image_id[:2]}/{str_image_id}.jpg'

# <<< ads part + images finish


class Core:
    """First of all, call configure function to set search settings(category, subcategory, region, price range etc).
    Configure function takes url with config query string(take it from kufar.by after setting all search parameters)"""
    def __init__(self):
        self.settings = SearchConfig()

    def get_ads_page(self, search_request=''):
        """function requests json with self.params['size'] ads. By default page size is 200 ads"""
        if search_request is not '':
            self.settings.params.update({'query': [search_request]})
        response = requests.get(self.settings.search_api_url, self.settings.params)
        return response.json()

    def get_all_ads(self, search_request='', force_get_all_ads=False):
        """Search_request variable sets as (query=) parameter in query string. Be careful with this bk
        if you set force_get_all_ads = True without query string, you will download all ads from
        kufar dashboard (it can be about 900 000 ads)"""
        content = []
        if search_request or self.settings.params.get('query') not in ('', None) or force_get_all_ads:
            while True:
                response = self.get_ads_page(search_request)
                content.extend(response['ads'])
                next_page_not_exists = True
                for page in response['pagination']['pages']:
                    if page['label'] == 'next':
                        self.settings.params.update({'cursor': [page['token']]})
                        next_page_not_exists = False
                if next_page_not_exists:
                    if self.settings.params.get('cursor') is not None:
                        del self.settings.params['cursor']
                    return content
        else:
            raise WrongArgsCombinationError

    def set_search_settings(self, url):
        """The function get url with search parameters. Search query (query=) parameter is an optional."""
        self.settings.configure(url)

    def get_ads_count(self, search_request=''):
        response = requests.get(self.settings.ads_count_api_url)
        return response.json()

    def get_user_info(self, user_id):
        user_info_url = self.settings.get_user_info_url(user_id)
        response = requests.get(user_info_url)
        return response.json()

    def get_small_image(self, image_id):
        image_url = self.settings.get_small_size_image_url(image_id)
        response = requests.get(image_url)
        return response.content

    def get_full_size_image(self, image_id):
        image_url = self.settings.get_full_size_image_url(image_id)
        response = requests.get(image_url)
        return response.content


if __name__ == "__main__":
    pass
