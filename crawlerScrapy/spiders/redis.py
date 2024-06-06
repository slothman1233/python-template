from scrapy_redis.spiders import RedisSpider
import scrapy
from crawlerScrapy.spiders.item.redis import RedisItem
from crawlerScrapy.spiders.settings.redis import settings

class LianjiaSpider(RedisSpider):
    name = 'redis'
    allowed_domains = ['lianjia.com']
    custom_settings = settings
    page = 2
    # start_urls = ['https://sh.lianjia.com/ershoufang/pg1/']
    # myscrawl 自己随便定义
    redis_key = 'myscrawl:start_urls'

    # 优先获取列表
    def start_requests(self):
        for i in range(1,101):
            yield scrapy.Request('https://sh.lianjia.com/ershoufang/pg{}/'.format(i))

    # def setup_redis(self, crawler=None):
    #     return super().setup_redis(crawler)

    def parse(self, response):
        url_list = response.xpath(
            '//div[@class="info clear"]/div[@class="title"]/a/@href').getall()
        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_info)
        if self.page < 101:
            yield scrapy.Request(f'https://sh.lianjia.com/ershoufang/pg{self.page}/')

    def parse_info(self, response):
        item = RedisItem()
        item['title'] = response.xpath(
            '//div[@class="communityName"]/a[1]/text()').get()
        item['action'] = response.xpath(
            'string(//div[@class="areaName"]/span[@class="info"])').get()
        item['momey'] = response.xpath('//div[@class="price"]/span').get()
        yield item
