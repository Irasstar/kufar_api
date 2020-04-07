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

    def configure(self, url_with_settings):
        parsed_url = urlparse(url_with_settings)
        self.params = parse_qs(parsed_url.query)
        if 'auto.kufar' in url_with_settings:
            self.api_type = 'auto'
        else:
            self.api_type = 'cre_api'


from urllib.parse import urlparse, parse_qs

class Core:
    # def init(self):
    #     self.requests = []

    def get_data(self):
        pass

    def _get_from_cre_api(self, params):
        api_url = 'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'
        response = requests.get(api_url, params)
        print(response.content.decode())

    def _get_from_auto_api(self, params):
        api_url = 'https://auto.kufar.by/api/search/ads-search/v1/engine/v1/search/rendered-paginated'
        response = requests.get(api_url, params)
        print(response.content.decode())

    def extract_params_from_url(self, url):
        parsed_url = urlparse(url)
        return parse_qs(parsed_url.query)


if __name__ == "__main__":
    my_core = Core()
    print(my_core.extract_params_from_url('https://www.kufar.by/listings?query=%D0%B0%D1%83%D0%B4%D0%B8&ot=1&rgn=7&ar='))