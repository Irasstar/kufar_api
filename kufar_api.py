# kufar.by api url:
# https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated
# kufar.by api parameters:
# ?query=iphone&ot=1&cat=17010&size=200&lang=ru&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30=

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


