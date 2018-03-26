# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi



class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

#write item(Article) information to json file  self defined
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding="utf-8")
    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()


class JsonExporterPipeline(object):
    #call exporter provided by scrapy
    def __init__(self):
        self.file = open('article_export.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item


# class MysqlPipeline(object):
#     def __init__(self):
#         self.conn = MySQLdb.connect('host','user','password','dbname',charset='utf8')
#         self.cursor = self.conn.cursor()
#     def process_item(self,item,spider):

class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
        dic = dict(
        host = settings["MYSQL_HOST"],
        db = settings["MYSQL_DBNAME"],
        user = settings["MYSQL_USER"],
        passwd = settings["MYSQL_PASSWORD"],
        charset='utf8',
        cursorclass=MySQLdb.cursors.DictCursor,
        use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool("MySQLdb",**dic)
        return cls(dbpool)

    def process_item(self,item,spider):


       query = self.dbpool.runInteraction(self.do_insert,item)
       query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = """
                insert into article(title,url,create_date,url_object,front_img_url,front_img_path,like_num,record_num,
                comment_num,tags,content)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql,(item["title"],item["url"],item["create_date"],item["url_object_id"],
                                   item["front_img_url"],item.get("front_img_path",""),item["like_num"],item["record_num"],
                                   item["comment_num"],item["tags"],item["content"]))










class ArticleImageStore(ImagesPipeline):
    def item_completed(self, results, item, info):
        img_file_path = ""
        if "front_img_url" in item:
            for ok, value in results:
                img_file_path = value.get("path", "")
            item["front_img_path"] = img_file_path
        return item



