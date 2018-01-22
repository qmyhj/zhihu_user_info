# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymongo
import pymysql
import logging
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            yield scrapy.Request(url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('item contains no images')
        item['image_path'] = image_path
        return item



class ZhihuPipeline(object):

    def __init__(self, crawler):
        self.mongo_uri = crawler.settings.get('MONGO_URI')
        self.mongo_db = crawler.settings.get('MONGO_DB')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # self.db['user'].insert_one(dict(item))
        self.db['user'].update({'url_token': item['url_token']}, {'$set': item}, True)
        return item

class MysqlPipeline(object):
    def __init__(self, params):
        self.conn = pymysql.Connect(**params)
        self.cursor = self.conn.cursor()

    @classmethod
    def from_settings(cls, settings):
        return cls(settings.get('PARAMS'))

    def process_item(self, item, spider):
        # 建立mysql表时，一定要制定编码为utf8，否则后期插入会报错, windows下mysql默认使用latin字符集
        sql, values = item.get_sql()
        self.cursor.execute(sql, values)
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, params):
        self.dbpool = adbapi.ConnectionPool('pymysql', **params)
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings.get('PARAMS'))

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert, item)
        query.addErrback(self.handle_error, item, spider)

    def insert(self, cursor, item):
        sql, values = item.get_sql()
        cursor.execute(sql, values)

    def handle_error(self, failure, item, spider):
        self.logger.debug(failure)
