# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import datetime

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db, collection_category, collection_ranking):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_category = collection_category
        self.collection_ranking = collection_ranking

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'trends'),
            collection_category=crawler.settings.get('MONGO_DATABASE', 'category'),
            collection_ranking=crawler.settings.get('MONGO_DATABASE', 'ranking')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'trends':
            if 'name' in item:
                self.insert_collection_category(item)
            elif 'rank' in item:
                self.insert_collection_ranking(item)
        return item

    def insert_collection_category(self, item):
        if not self.db[self.collection_category].find_one(
                {"category": item['category']}):
            self.db[self.collection_category].insert(dict(item))

    def insert_collection_ranking(self, item):
        if not self.db[self.collection_ranking].find_one(
                {"date": today, "rank": item['rank'], "category": item['category']}):
            self.db[self.collection_ranking].insert(dict(item))