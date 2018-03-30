# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import datetime
from scrapy.loader import ItemLoader
import re
from w3lib.html import remove_tags

def date_convert(value):

    try:
        create_date = datetime.datetime.strptime(value,"%Y%M%D").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_nums(value):
    val = re.match(".*?(\d+).*",value)
    if val:
        return_value = int(val.group(1))
    else:
        return_value = 0
    return return_value

def do_nothing(value):
    return value







class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),

    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_img_url = scrapy.Field(
        output_processor=MapCompose(do_nothing)
    )
    front_img_path = scrapy.Field()
    like_num = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    record_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        output_processor=Join(",")
    )
    content = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
                        insert into article(title,url,create_date,content)
                        VALUES (%s,%s,%s,%s)
                        """
        params = (self.title,self.url,self.create_date,self.content)
        return insert_sql,params

class ZhihuQuestion(scrapy.Item):
    """
    Question item
    """

    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                        insert into zhihu_question(zhihu_id,topics,url,title,content,answer_num,comments_num,watch_user_num,click_num,crawl_time)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num),
                        comments_num=VALUES(comments_num),watch_user_num=VALUES(watch_user_num),
                        click_num=VALUES(click_num)
                        """
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = self["title"][0]
        content = self["content"][0]
        answer_num = get_nums("".join(self["answer_num"]))
        comments_num = get_nums("".join(self["comments_num"]))
        watch_user_num = get_nums("".join(self["watch_user_num"]))
        click_num = get_nums("".join(self["click_num"]))
        crawl_time = datetime.datetime.now().strftime("%Y-%m-%d")

        params = (zhihu_id,topics,url,title,content,answer_num,comments_num,watch_user_num,click_num,crawl_time)



        return insert_sql,params

class ZhihuAnswer(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
                        insert into zhihu_answer(zhihu_id,url,question_id,author_id,content,
                        praise_num,comments_num,create_time,update_time,crawl_time)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE content=VALUES(content), praise_num=VALUES(praise_num),
                        comments_num=VALUES(comments_num),update_time=VALUES(update_time)
                        """


        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime("%Y-%m-%d")
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime("%Y-%m-%d")
        params = (
           self["zhihu_id"],
           self["url"],
            self["question_id"],
            self["author_id"],
            self["content"],
            self["praise_num"],
            self["comments_num"],
            create_time,
            update_time,
            self["crawl_time"].strftime("%Y-%m-%d")
       )





        return insert_sql,params


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def remove_splash(value):
    return value.replace("/","")

def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]
    return "".join(addr_list)


def get_min_salary(value):
    match = re.match("(\d+).*",value)
    return match.group(1)+"k"


class LagouItem(scrapy.Item):

    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field(
        input_processor=MapCompose(get_min_salary)
    )
    city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(",")
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    crawl_time = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
            insert into lagou_job(url, url_object_id, title, salary, city, work_years, degree_need,
            job_type, publish_time, tags, job_advantage, job_desc, job_addr, company_name,
            crawl_time, company_url,) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_desc=VALUES(job_desc)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"],
            self["work_years"], self["degree_need"], self["job_type"],
            self["publish_time"], self["job_advantage"], self["job_desc"],
            self["job_addr"], self["company_name"], self["company_url"],
            self["job_addr"], self["crawl_time"].strftime("%Y-%m-%d"),
        )

        return insert_sql, params







