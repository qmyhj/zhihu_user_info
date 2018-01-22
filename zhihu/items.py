# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    url_token = scrapy.Field()
    answer_count = scrapy.Field()
    articles_count = scrapy.Field()
    gender = scrapy.Field()

    def get_sql(self):
        sql = """
        insert into info(id, name, type, url_token, answer_count, articles_count, gender) 
        values(%s, %s, %s, %s, %s, %s, %s)
        """
        values = (self['id'], self['name'], self['type'], self['url_token'], self['answer_count'], self['articles_count'], self['gender'])
        return sql.strip(), values


class DoubanItem(scrapy.Item):
    image_urls = scrapy.Field()
    image_path = scrapy.Field()


class TaobaoItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    week_sale = scrapy.Field()
    shops_num = scrapy.Field()