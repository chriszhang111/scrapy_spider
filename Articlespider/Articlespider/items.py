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




