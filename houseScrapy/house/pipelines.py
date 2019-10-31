# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.exceptions import DropItem

class HousePipeline(object):
    def process_item(self, item, spider):
        return item

# 数据格式化
class ValueConverterPipeline:

    def process_item(self, item, spider):

        str = item['rating']
        if str == '--':
            item['rating'] = '0.0'


        else:
            value = str[:-2]
            if str[-1:] == '↑':
                item['rating'] = '%s%s' % ('+', value)

            elif str[-1:] == '↓':
                item['rating'] = '%s%s' % ('-', value)


        item['name'] = item['name'][5:-2]
        item['price'] = item['price'][:-3]

        return item

# 数据库持久化
class MysqlPipeline:

    priceInsert = '''insert into newdata(name, price, rating, date)values('{name}', {price}, {rating}, '{date}')'''

    def __init__(self, settings):
        self.settings = settings


    def process_item(self, item, spider):
        if spider.name == "houses":
            sqltext = self.priceInsert.format(
                name=pymysql.escape_string(item['name']),
                price=pymysql.escape_string(item['price']),
                rating=pymysql.escape_string(item['rating']),
                date=pymysql.escape_string(item['date']))
            spider.log(sqltext)
            self.cursor.execute(sqltext)
        else:
            spider.log('Undefined name: %s' % spider.name)

        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


# 去重
class DuplicatesPipeline(object):
    def __init__(self):
        self.house_set = set()

    def process_item(self, item, spider):

        if item in self.house_set:
            raise DropItem("Duplicate data found: %s" % item)

        self.house_set.add(item)
        return item