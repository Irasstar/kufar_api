# kufar.by api url:

# search
# https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated
# parameters:
# ?query=iphone&ot=1&cat=17010&size=200&lang=ru&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30=

# ads count request
# https://cre-api.kufar.by/ads-search/v1/engine/v1/search/count
# parameters
# ?cur=BYR&rgn=7&size=42&sort=lst.d&query=

# ad user info
# https://www.kufar.by/item/api/aduserinfo/2499605
# 2499605 - user id

import requests


class Core:
    def __init__(self):
        url = 'https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated'
        params = {
            'query': '',
            'ot': 1,
            'cat': 17010,
            'size': 200,  # max size = 200
            'lang': 'ru',
            'cursor': '',  # page token (set here next page token from paginagion dict in response)

        }
