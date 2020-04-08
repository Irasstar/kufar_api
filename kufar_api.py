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



class Core:
    def __init__(self):
        self.url = 'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'
        self.params = {
            'query': '',
            'ot': 1,
            'cat': 17010,  # search category
            'size': 200,  # max size = 200
            'lang': 'ru',
            'cursor': '',  # page token (set here next page token from paginagion dict in response)

        }
    def get_data(self):
        response = requests.get(self.url, self.params)
        print(response.content.decode())

if __name__ == "__main__":
    my_core = Core()
    my_core.get_data()