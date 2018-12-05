# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymongo

class CatPipeline(object):
    def process_item(self, item, spider):
        return item


class MaoyanMysql(object):
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            username=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        sql = 'insert into maoyan(movie, starring, releasetime, top, score, img, link) values("%s", "%s", "%s", "%s",' \
              ' "%s", "%s", "%s")'
        self.cursor.execute(sql % (item['movie'], item['starring'], item['releasetime'], item['top'], item['score'],
                                   item['img'], item['link']))
        self.db.commit()
        return item


class MaoyanPymongo(object):
    def __init__(self, database):
        self.client = pymongo.MongoClient()
        self.db = self.client[database]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        maoyan = {}
        maoyan['movie'] = item['movie']
        maoyan['starring'] = item['starring']
        maoyan['releasetime'] = item['releasetime']
        maoyan['top'] = item['top']
        maoyan['score'] = item['score']
        maoyan['img'] = item['img']
        maoyan['link'] = item['link']
        self.db.maoyan.insert(maoyan)
        return item
