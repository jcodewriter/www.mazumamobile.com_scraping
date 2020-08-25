# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import MySQLdb
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem, NotConfigured
from scrapy.pipelines.images import ImagesPipeline


class MazumamobileScrapingPipeline:
    def process_item(self, item, spider):
        return item


class MobileImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item


class DatabasePipeline(object):
    # Add database connection parameters in the constructor
    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    # Implement from_crawler method and get database connection info from settings.py

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)
    # Connect to the database when the spider starts

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(db=self.db,
                                    user=self.user, passwd=self.passwd,
                                    host=self.host,
                                    charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()
    # Insert data records into the database (one item at a time)

    def process_item(self, item, spider):
        sql = "REPLACE INTO wp_phone_data (phone_ID, phone_Name, phone_Model, phone_Type, excellent_price, good_price, poor_price, faulty_price, dead_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql,
                            (
                                item.get("phoneID"),
                                item.get("phoneName"),
                                item.get("phoneModel"),
                                item.get("phoneType"),
                                item.get("excellentPrice"),
                                item.get("goodPrice"),
                                item.get("poorPrice"),
                                item.get("faultyPrice"),
                                item.get("deadPrice"),
                            )
                            )
        self.conn.commit()
        return item
    # When all done close the database connection

    def close_spider(self, spider):
        self.conn.close()
