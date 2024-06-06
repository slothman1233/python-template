import scrapy

from crawlerScrapy.spiders.utils.file import file_write, file_write_enum
from mark import BASE_DIR


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        print(file_write(f'{BASE_DIR}/crawlerScrapy/log/111.txt','fd\n',file_write_enum.addto )) 
        print(123323)
        pass
