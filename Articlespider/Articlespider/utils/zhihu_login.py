import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re


agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
header = {
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com",
    "User-Agent":agent


}
def zhihu_login(account,passwd):
    #login in to zhihu.com
    if re.match("^1\d{10}",account):
        print("Login in with phone")
        post_url = "http://www.zhihu.com/login/phone_num"


def get_xsrf():
    response = requests.get("https://www.zhihu.com",headers=header)
    print(response.text)

get_xsrf()