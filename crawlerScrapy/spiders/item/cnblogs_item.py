import scrapy


class CnblogsItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    real_desc = scrapy.Field()
    pub_time = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    pass

