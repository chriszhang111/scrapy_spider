

import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost",user="root",passwd="31415926",db="article_spider",charset="utf8")
cursor = conn.cursor()

def crawl_ips():
    ####get ips from xiciDaili
    new_list = set()
    page = 0

    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",

               }
    re = requests.get("http://www.xicidaili.com/wn/{0}".format(page),headers=headers)

    selector = Selector(text=re.text)
    all_trs = selector.css("#ip_list tr")
    for tr in all_trs:
        x = tr
        try:

            ip = tr.xpath("./td[2]/text()").extract()[0]
            port = tr.xpath("./td[3]/text()").extract()[0]
            #method = tr.xpath("./td[6]/text()").extract()[0]
        except:
            ip = None
            port = None
            #method = None

        # if(ip and port and method and not method.startswith("sock")):
        #     print(method.lower()+"://"+ip+":"+port)
        if(ip and port):
            new_list.add((ip,port,"https"))




    return new_list


"""
Insert data into databases
"""
# list = crawl_ips()
# # for i in list:
# #     print(i)
# for param in list:
#
#     cursor.execute(
#         "INSERT INTO http_proxy(ip,port,proxy) VALUES(%s,%s,%s)",
#         param)
#     conn.commit()


class GetIp(object):
    def __judge_ip(self,ip,port,proxy):
        if proxy not in ("http","https"):
            return False
        http_utl = "{0}://{1}:{2}".format(proxy,ip,port)

        try:
            proxy_dict = {
                proxy:http_utl
            }

            response = requests.get("http://www.baidu.com",proxies=proxy_dict)

        except Exception as e:
            return False
        else:
            code = response.status_code
            if 200<=code<=300:
                return True
            else:
                return False

    def get_random_ip(self):
        """
        get random ip from database
        :return: str
        """
        sql = "SELECT ip,port,proxy FROM http_proxy ORDER BY RAND() LIMIT 1"
        result = cursor.execute(sql)

        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            proxy = ip_info[2].lower()

            if self.__judge_ip(ip,port,proxy):
                return "{0}://{1}:{2}".format(proxy,ip,port)
            else:
                return self.get_random_ip()






if __name__ == "__main__":

    cla = GetIp()
    print(cla.get_random_ip())


















