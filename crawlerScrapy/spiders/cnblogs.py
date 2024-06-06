import scrapy
from scrapy import Request
from crawlerScrapy.spiders.item.cnblogs_item import CnblogsItem

from crawlerScrapy.spiders.settings.cnblogs import settings


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    # allowed_domains = ['cnblogs']
    # start_urls = ['https://www.cnblogs.com']
    custom_settings = settings

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        

    def start_requests(self):
        # yield scrapy.Request(url, callback=self.parse, headers=headers, meta={'proxy': proxy_addr})
        # headers=headers, meta={'proxy': proxy_addr})

        yield Request(url='https://www.cnblogs.com', callback=self.parse)

    def parse(self, response):
        # print(response.text)
        article_list = response.css('article.post-item')
        print(len(article_list))
        for article in article_list:
            item = CnblogsItem()

            item['title'] = article.css(
                'a.post-item-title::text').extract_first()
            item['desc'] = article.css('p.post-item-summary::text').extract()
            item['real_desc'] = item['desc'][0].replace(
                '\n', '').replace(' ', '')
            if not item['real_desc']:
                item['real_desc'] = item['desc'][1].replace(
                    '\n', '').replace(' ', '')
            item['pub_time'] = article.css(
                'span.post-meta-item>span::text').extract_first()
            item['author'] = article.css(
                'footer.post-item-foot span::text').extract_first()
            item['url'] = article.css(
                'a.post-item-title::attr(href)').extract_first()
            yield item
        next = 'https://www.cnblogs.com' + \
            response.css('.pager a:last-child::attr(href)').extract_first()
        yield Request(url=next)

    def close(spider, reason):
        print(reason)
        pass
