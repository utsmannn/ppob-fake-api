import json

from requests import request


class HttpClientService:
    def post(self, url, data):
        req = request(
            method='post',
            url=url,
            json=data
        )
        return req.json()

    def get(self, url):
        return request(
            method='get',
            url=url
        ).json()