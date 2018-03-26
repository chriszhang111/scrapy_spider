# -*- coding: utf-8 -*-
import scrapy

from items import ArticleItemLoader
from selenium import webdriver

import  os

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
# driver.get("https://www.zhihu.com/signin?next=%2F")

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']


    def parse(self, response):
        pass

    def start_requests(self):
        driver.get('https://www.zhihu.com/signin?next=%2F')

        driver.find_element_by_css_selector(".Login-content input[name='username']").send_keys("869415122@qq.com")
        driver.find_element_by_css_selector(".Login-content input[name='password']").send_keys("31415926")
        driver.find_element_by_css_selector(".Button.SignFlow-submitButton.Button--primary.Button--blue").click()

        import time
        time.sleep(10)
        Cookies = driver.get_cookies()
        print(Cookies)

        cookie_dict = {}
        import pickle
        for cookie in Cookies:
            f = open('/Users/chris/Pyproject/scrapy/Articlespider/Articlespider'+cookie['name']+'.zhihu','wb')
            pickle.dump(cookie,f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        driver.close()
        return [scrapy.Request(url=self.start_urls[0],dont_filter=True,cookies=cookie_dict)]




