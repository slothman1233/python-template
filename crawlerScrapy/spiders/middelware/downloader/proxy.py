from crawlerScrapy.settings import PROXIES
import random

# 设置代理
class ProxyDownloader(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES).strip()
        request.meta['proxy'] = proxy
    # Downloader Middleware的核心方法，只有实现了其中一个或多个方法才算自定义了一个Downloader Middleware
    def process_response(self, request, response, spider):
        print(response)
        # 请求失败不等于200
        if response.status != 200:
            # 重新选择一个代理ip
            proxy = random.choice(PROXIES).strip()
            print("this is response ip:" + proxy)
            # 设置新的代理ip内容
            request.mete['proxy'] = proxy
            return request
        return response
    def process_exception(self, request, exception, spider):
        print(request,exception)
        
        pass