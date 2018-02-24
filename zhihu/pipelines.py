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


class MongoPipeline(object):

    def __init__(self, settings):
        self.mongo_host = settings.get('MONGO_HOST')
        self.mongo_db = settings.get('MONGO_DB')
        self.mongo_table = settings.get('MONGO_TABLE')

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_host)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.mongo_table].insert_one(dict(item))
        return item

class MysqlPipeline(object):
    def __init__(self, params):
        self.conn = pymysql.Connect(**params)
        self.cursor = self.conn.cursor()

    @classmethod
    def from_settings(cls, settings):
        return cls(settings.get('MYSQL_PARAMS'))

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
        return cls(settings.get('MYSQL_PARAMS'))

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert, item)
        query.addErrback(self.handle_error, item, spider)

    def insert(self, cursor, item):
        sql, values = item.get_sql()
        cursor.execute(sql, values)

    def handle_error(self, failure, item, spider):
        self.logger.debug(failure)
