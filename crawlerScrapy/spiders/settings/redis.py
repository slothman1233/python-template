settings = {
    'ITEM_PIPELINES': {
        # 把数据 放在redis里面
        # 'scrapy_redis.pipelines.RedisPipeline': 300,
        'crawlerScrapy.spiders.pipeline.redis.RedisPipeline': 300,
    },

    "SCHEDULER": "scrapy_redis.scheduler.Scheduler"

    # 'REDIS_HOST': 'localhost',  # master IP

    # 'REDIS_PORT': 6379,

    # 'REDIS_PARAMS':{}

    # 'REDIS_URL': 'redis://:gs123456@127.0.0.1:6379',  # 如果redis有密码，使用这个配置

    # 'REDIS_ENCODING': "utf-8"  # redis编码类型 默认：'utf-8'
}
