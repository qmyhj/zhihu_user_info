# -*- coding: utf-8 -*-

import logging
import requests
from fake_useragent import UserAgent


class RandomUserAgentMiddlewares(object):

    def __init__(self):
        self.ua = UserAgent()
        self.logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        ua = self.ua.random
        self.logger.debug('Using random User-Agent ' + ua)
        request.headers['User-Agent'] = ua


class HttpProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.proxy_url = proxy_url
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings.get('PROXY_URL'))

    def get_proxy_url(self, url):
        r = requests.get(url)
        return r.text

    def process_request(self, request, spider):
        proxy = self.get_proxy_url(self.proxy_url)
        self.logger.debug('Using HttpProxy ' + proxy)
        request.meta['proxy'] = 'http://' + proxy





