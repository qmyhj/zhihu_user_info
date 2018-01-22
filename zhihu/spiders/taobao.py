# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from ..items import TaobaoItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    count = 1
    chrome_opt = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_opt.add_experimental_option("prefs", prefs)

    def __init__(self):
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Chrome(chrome_options=self.chrome_opt)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self):
        self.browser.close()

    def start_requests(self):
        start_urls = ['https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%89%8B%E6%9C%BA&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest&p4ppushleft=5%2C48&s={page}'.format(page=str(48 * i)) for i in range(4, 5)]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = TaobaoItem()
        titles = response.css('a.product-title::attr("title")').extract()
        prices = response.css('span.price.g_price.g_price-highlight strong::text').extract()
        week_sales = response.css('span.week-sale span.num::text').extract()
        shops_nums = response.css('a.seller-link::text').re('.*?(\d+).*')

        for title, price, week_sale, shops_num in zip(titles, prices, week_sales, shops_nums):
            item['title'] = title
            item['price'] = price
            item['week_sale'] = week_sale
            item['shops_num'] = shops_num
            yield item
            print('*'*10 + str(self.count) + '*'*10)
            self.count += 1



