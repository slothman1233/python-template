from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def start():
    process = CrawlerProcess(get_project_settings())
    process.crawl("example")
    process.crawl("redis")
    process.start()
    


if __name__ == '__main__':
    start()
