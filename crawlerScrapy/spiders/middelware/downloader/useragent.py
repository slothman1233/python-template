# from crawlerScrapy.settings import USER_AGENT_LIST
# import random
from fake_useragent import UserAgent

# 随机设置UA
class UserAgentDownloader(object):
    def process_request(self, request, spider):
           
        ua = UserAgent()
        # print(ua.ie)   #随机打印ie浏览器任意版本
        # print(ua.firefox) #随机打印firefox浏览器任意版本
        # print(ua.chrome)  #随机打印chrome浏览器任意版本
        # print(ua.random)  #随机打印任意厂家的浏览器 
        # useragent = random.choice(USER_AGENT_LIST)
        request.headers["User-Agent"] = ua.chrome
