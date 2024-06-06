import scrapy


class SeleniumItem(scrapy.Item):
    value1 = scrapy.Field()
    value2 = scrapy.Field()
    value3 = scrapy.Field()
    pass