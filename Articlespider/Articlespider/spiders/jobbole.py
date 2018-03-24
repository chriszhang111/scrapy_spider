# -*- coding: utf-8 -*-

import scrapy
import re
from scrapy.http import Request
from urllib import parse
import os
import sys

from items import JobboleArticleItem

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




"""

        number_of_like = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()
        match_num = ".*?(\d+).*"  ##ways to extract number ou of strings



        through css
        x = response.css(".entry-header h1::text").extract_first()

        number_of_like = response.css(".vote-post-up h10::text").extract()[0]
        favor_num = response.css(".bookmark-btn::text").extract()[0]
        comment_num = response.css("a[href='#article' span::text").extract()
        tags = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tags = "".join(tags)
         """


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']



    def parse(self, response):
        """

        :param response: response
        :return:None
        """
        urls = response.css("#archive .floated-thumb .post-thumb a")

        for post_node in urls:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_img_url":image_url},callback=self.parse_article)

        # next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        # if next_url:
        #      yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)





    def parse_article(self,response):
        """

        :param response:
        :return:
        """

        job_article_instance = JobboleArticleItem()

        front_img_url = response.meta.get("front_img_url",None)
        #print(front_img_url)
        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip()
        like_num = response.css(".vote-post-up h10::text").extract()[0]
        record_num = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(".*?(\d+).*",record_num)
        if match_re:
            record_num = int(match_re.group(1))
        else:
            record_num = 0

        comment_num = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*",comment_num)
        if match_re:
            comment_num = int(match_re.group(1))
        else:
            comment_num = 0
        content = response.css("div.entry").extract()[0]

        tags = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tags = "".join(tags)


        job_article_instance["title"] = title
        job_article_instance["create_date"] = create_date
        job_article_instance["url"] = response.url
        job_article_instance["front_img_url"] = front_img_url
        job_article_instance["like_num"] = like_num
        job_article_instance["record_num"] = record_num
        job_article_instance["comment_num"] = comment_num
        job_article_instance["tags"] = tags
        job_article_instance["content"] = content

        yield job_article_instance



















