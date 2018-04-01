# -*- coding: utf-8 -*-
import json
import re

import datetime
import scrapy


from selenium import webdriver
from settings import USER_AGENT
import  os
from urllib import parse
from scrapy.loader import ItemLoader

from items import ZhihuQuestion, ZhihuAnswer
import random

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
# driver.get("https://www.zhihu.com/signin?next=%2F")

class ZhihuSpider(scrapy.Spider):
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/#signin']
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    #rand_index = random.randint(0,len(USER_AGENT)-1)

    headers = {
        'authorization': 'oauth ' + client_id,
        'Host': 'www.zhihu.com',
        'Origin': 'https://www.zhihu.com',
        'Referer': 'https://www.zhihu.com/signup?next=%2F',
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/124 (KHTML, like Gecko) Safari/125.1'
    }


    def parse(self, response):
        """

        :param response:
        :return:
        """

        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        all_urls = filter(lambda x:False if x.startwith("java") else True,all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*",url)
            if match_obj:
                ####if matched ,then parse
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)

                yield scrapy.Request(url=request_url,meta={"question_id":question_id},headers=self.headers,callback=self.parse_question)

            else:
                ##dfs
                yield scrapy.Request(url,headers=self.headers,callback=self.parse)


    def parse_question(self,response):
        """
        deal with question page
        :return:
        """
        question_itemloader = ItemLoader(ZhihuQuestion(),response=response)
        question_itemloader.add_css("title","h1.QuestionHeader-title::text")
        question_itemloader.add_css("content",".QuestionHeader-detail")
        question_itemloader.add_value("url",response.url)
        question_itemloader.add_value("zhihu_id", response.meta.get("question_id"))
        question_itemloader.add_css("answer_num",".List-headerText span::text")
        question_itemloader.add_css("comments_num",".QuestionHeader-Comment button::text")
        question_itemloader.add_css("watch_user_num",".NumberBoard-itemValue::text")
        question_itemloader.add_css("topics",".QuestionHeader-topics .Popover::text")

        question_item = question_itemloader.load_item()



        yield scrapy.Request(self.start_answer_url.format(response.meta.get("question_id"),20,0),callback=self.parse_answer,headers=self.headers)

        yield question_item

    def parse_answer(self,response):
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        totals_answer = ans_json["paging"]["totals"]
        next_url = ans_json["paging"]["next"]
        ##extract answer

        for answer in ans_json["data"]:
            ans_item = ZhihuAnswer()
            ans_item["zhihu_id"] = answer["id"]
            ans_item["url"] = answer["url"]
            ans_item["question_id"] = answer["question"]["id"]
            ans_item["author_id"] = answer["author"].get("id",None)
            ans_item["content"] = answer.get("content",None)
            ans_item["praise_num"] = answer["voteup_count"]
            ans_item["comments_num"] = answer["comment_count"]
            ans_item["create_time"] = answer["created_time"]
            ans_item["update_time"] = answer["updated_time"]
            ans_item["crawl_time"] = datetime.datetime.now()
            yield ans_item




        if not is_end:
            yield scrapy.Request(next_url,callback=self.parse_answer,headers=self.headers)


















    ##do requests by selenium simulator
    def start_requests(self):
        driver.get('https://www.zhihu.com/signin?next=%2F')

        driver.find_element_by_css_selector(".Login-content input[name='username']").send_keys("869415122@qq.com")
        driver.find_element_by_css_selector(".Login-content input[name='password']").send_keys("31415926")
        driver.find_element_by_css_selector(".Button.SignFlow-submitButton.Button--primary.Button--blue").click()

        import time
        time.sleep(10)
        Cookies = driver.get_cookies()
        #print(Cookies)

        cookie_dict = {}
        import pickle
        for cookie in Cookies:
            f = open('/Users/chris/Pyproject/scrapy/Articlespider/Articlespider'+cookie['name']+'.zhihu','wb')
            pickle.dump(cookie,f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        ##driver.close()
        return [scrapy.Request(url=self.start_urls[0],dont_filter=True,cookies=cookie_dict,headers=self.headers)]




