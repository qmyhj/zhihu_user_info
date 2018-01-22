# -*- coding: utf-8 -*-
import scrapy
from ..items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    def start_requests(self):
        start_urls = ['https://movie.douban.com/tag/%E5%8A%A8%E6%BC%AB?start={page}&type=T'.format(page=str(20*i)) for i in range(10)]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = DoubanItem()
        item['image_urls'] = response.css('a.nbg > img::attr(src)').extract()
        yield item