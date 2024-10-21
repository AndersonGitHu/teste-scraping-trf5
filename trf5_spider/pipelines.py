# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class Trf5SpiderPipeline:
#     def process_item(self, item, spider):
#         return item

import pymongo
from scrapy import settings
from scrapy.exceptions import DropItem


class Trf5SpiderPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_collection):

       
        self.mongo_uri = mongo_uri
        print('==============================================================')
        self.mongo_db = mongo_db        
        self.mongo_collection = mongo_collection

        
        # connection = pymongo.MongoClient(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        # db = connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGODB_URI"),
            mongo_db=crawler.settings.get("MONGODB_DB"),
            mongo_collection=crawler.settings.get("MONGODB_COLLECTION")
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):     

        self.db[self.mongo_collection].replace_one(filter={'numero_processo': item.get('numero_processo')}, replacement=dict(item), upsert=True)

        return item