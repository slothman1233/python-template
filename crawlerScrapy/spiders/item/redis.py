import scrapy


class RedisItem(scrapy.Item):
    title = scrapy.Field()
    action = scrapy.Field()
    momey = scrapy.Field()