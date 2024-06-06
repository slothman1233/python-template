settings = {
    # "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    # "DEFAULT_REQUEST_HEADERS": {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Accept-Language': 'en',
    # },
    # "SPIDER_MIDDLEWARES": {
    #     'crawlerScrapy.middlewares.CnblogsSpiderMiddleware': 543,
    # },
    "DOWNLOADER_MIDDLEWARES": {
        'crawlerScrapy.spiders.middelware.downloader.useragent.UserAgentDownloader': 543,
        # 'crawlerScrapy.spiders.middelware.downloader.proxy.ProxyDownloader': 200,

    },
    "ITEM_PIPELINES": {
        'crawlerScrapy.spiders.pipeline.cnblogs.CnblogsPipeline': 300,
        # 'crawlerScrapy.pipelines.CrawlerScrapyPipeline':300
    }
}
