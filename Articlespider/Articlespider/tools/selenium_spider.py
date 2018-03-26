from selenium import webdriver

import  os

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
driver.get("https://www.zhihu.com/signin")

driver.find_element_by_css_selector(".Login-content input[name='username']").send_keys("869415122@qq.com")
driver.find_element_by_css_selector(".Login-content input[name='password']").send_keys("31415926")
print(driver.find_element_by_css_selector(".Button.SignFlow-submitButton.Button--primary.Button--blue").click())