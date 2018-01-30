# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .gftmysql.datemysql import MyMysql
import re


class GftsearchPipeline(object):
    def __init__(self):
        self.db = MyMysql("192.168.1.158", "root", "123456", "ssrnDB")
        self.f = open('test-1.json', 'w')

    # 获取爬虫生的item 并返回 item 引擎判断数据处理完成
    def process_item(self, item, spider):
        gid = item['gid']
        title = item["title"]
        author = item['author']
        links = item['links']
        downloads = re.sub(',', '', item['downloads'])
        sq = "REPLACE INTO ssrnpaper (gid ,title, author, link, downloads) VALUES"
        sql = sq + "(" + '{},"{}","{}","{}",{}'.format(gid, title, author, links, downloads) + ");"
        self.db.ExecNonQuery(sql)
        self.f.write(sql)
        return item

    # 爬虫启动时候执行的方法（可选）
    def open_spider(self, spider):
        pass

    # 执行完成后进行的操作（可选）
    def close_spider(self, spider):
        pass

# sq = "REPLACE　INTO ssrnpaper (gid ,title, author, link, downloads) VALUES "
# MyMysql()