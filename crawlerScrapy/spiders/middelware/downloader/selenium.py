
from scrapy.http import HtmlResponse
from fake_useragent import UserAgent



class SeleniumDownloader(object):
    def process_request(self, request, spider):

        ua = UserAgent()
        
        # print(spider.driver.execute_script("return navigator.userAgent;"))

        spider.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua.chrome})

        # print(spider.driver.execute_script("return navigator.userAgent;"))

        spider.driver.get(request.url)


        response = HtmlResponse(
            url=request.url, body=spider.driver.page_source.encode('utf-8'), request=request)
        return response

     # Downloader Middleware的核心方法，只有实现了其中一个或多个方法才算自定义了一个Downloader Middleware

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        print(request, exception)
        pass
