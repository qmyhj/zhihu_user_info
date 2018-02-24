# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    url_token = scrapy.Field()
    answer_count = scrapy.Field()
    articles_count = scrapy.Field()
    gender = scrapy.Field()

    def get_sql(self):
        sql = """
        INSERT INTO info(id, name, type, url_token, answer_count, articles_count, gender) 
        VALUES(%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name)
        """
        values = (self['id'], self['name'], self['type'], self['url_token'], self['answer_count'], self['articles_count'], self['gender'])
        return sql.strip(), values
