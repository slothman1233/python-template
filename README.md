# python scrapy爬虫

[TOC]

### 运行要求

```bash   
python 3.9.13 
```

### docker 命令

```bash
docker build -t scrapy . --tag scrapy:1
docker run -d -p :8085:80  scrapy:1
```

### 命令介绍

```bash
pip install -r requirements.txt -- 安装依赖

python run.py     ----- 单线程运行
python threadRun.py  ----- 多线程运行
scrapy crawl example ----- 运行单个程序
```

### 命令行传参

> 注意一个`-a`一个参数

```
scrapy crawl example -a "search=sss" -a "year=2022"
```

在__init__方法接受

```
class SciencedirectspiderSpider(scrapy.Spider):
    name = 'sciencedirectspider'
    allowed_domains = ['sciencedirect.com']
    start_urls = ['https://www.sciencedirect.com/search?qs=kidney%20stone']
　　　# 在初始化这里进行
    def __init__(self, year='', search='', **kwargs):
```

### 目录说明

> ├── cnblogs.py 带MySQL示例
>
> ├── example.py 基础示例
>
> ├── redis.py 分布式加MySQL示例
>
> ├── selenium.py selenium加MySQL示例

 __这4个示例，保留需要的，同时删除 'item','middelware','settings' 目录下对应不需要的文件。__

__requirements.txt 需要删除不需要的依赖， 如果项目添加了新的依赖需要在该文件中添加。__

```
├── crawlerScrapy  项目目录
│   ├── depends  放chrome第三方
│   ├── spiders  spider
│   │   ├── item     数据结构文件夹
│   │   ├── middelware 中间件文件夹
│   │   │   ├── downloader 下载中间件
│   │   │   ├── dupefilter 自定义过滤方法
│   │   │   └── spider 爬虫中间件
│   │   ├── cnblogs.py 带MySQL示例
│   │   ├── example.py 基础示例
│   │   ├── redis.py 分布式加MySQL示例
│   │   ├── selenium.py selenium加MySQL示例
│   │   ├── pipeline  管道文件夹
│   │   ├── settings  单独配置文件夹
│   │   └── utils    工具类
│   │   │   ├── file 文件处理工具
│   │   │   └── webdriver selenium处理工具
│   ├── items.py 数据结构（不建议使用）
│   ├── middlewares.py 中间件（不建议使用）
│   ├── threadRun.py 多线程运行
│   ├── run.py 单线程运行
│   └── settings.py 全局配置
├── dockerfile  docker配置文件
├── .dockerignore  
├── .gitignore  
├── install.py  docker里面的 chrome浏览器安装
├── mark.py    
├── requirements.txt  项目依赖安装项
└── scrapy.cfg  

```

### 创建页面说明

```bash

└── crawlerScrapy  项目目录
    └── spiders  spider
        ├── quotes.py 创建的爬虫页
        ├── item     数据结构文件夹
        │   └── quotes_item.py 对应的数据结构
        ├── middelware 中间件文件夹（非必要）
        │   └── downloader 下载中间件
        │   │   └── quotes.py 中间件
        │   └── spider 爬虫中间件
        │   │   └── quotes.py 中间件
        ├── settings  单独配置文件夹
        │   └── quotes.py 对应的配置文件
        └── pipeline  管道文件夹
            └── quotes.py 对应的管道文件夹

```

#### spiders/quotes.py 内容如下：

爬虫文件

```python
import scrapy
from crawlerScrapy.spiders.settings.quotes import settings

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = settings
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {}
def parse(self, response):
    pass
```

#### spiders/item/quotes.py 内容如下：

管道文件

```python
import scrapy

class QuotesItem(scrapy.Item):
    # title = scrapy.Field()
    pass
```

#### spiders/pipeline/quotes_item.py 内容如下：

数据结构

```python
import pymysql

from crawlerScrapy.settings import MYSQL_CHARSET, MYSQL_DB, MYSQL_HOST, MYSQL_PASSWD, MYSQL_PORT, MYSQL_USE_UNICODE, MYSQL_USER

class QuotesPipeline(object):
    def __init__(self, spider_data):
        self.spider_data = spider_data
        # 连接数据库
        self.connect = pymysql.connect(
            host=MYSQL_HOST,  # 数据库地址
            port=MYSQL_PORT,  # 数据库端口
            db=MYSQL_DB,  # 数据库名
            user=MYSQL_USER,  # 数据库用户名
            passwd=MYSQL_PASSWD,  # 数据库密码
            charset=MYSQL_CHARSET,  # 编码方式
            use_unicode=MYSQL_USE_UNICODE)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        """
        获取spider的settings参数,返回Pipeline实例对象
        """
        spider_data = crawler.settings.get("SPIDER_DATA")
        print("### pipeline get spider_data: {}".format(spider_data))

        return cls(spider_data)

    def process_item(self, item, spider):
        """
        return Item 继续处理
        raise DropItem 丢弃
        """
        print("### call process_item")
        
         # sql语句
        insert_sql = """
        insert into redis(title, action, momey) VALUES (%s,%s,%s)
        """
        try:
            # 执行插入数据到数据库操作
            self.cursor.execute(
                insert_sql, (item['title'], item['action'], item['momey']))

            # 提交sql语句
            self.connect.commit()
        except Exception as e:
            print('mysql写入错误error:{} --- item={}'.format(e, item))
            pass


        return item

    def open_spider(self, spider):
        """
        spider开启时调用
        """
        print("### spdier open {}".format(spider.name))

    def close_spider(self, spider):
        """
        spider关闭时调用
        """
        print("### spdier close {}".format(spider.name))
        
        self.connect.close()

```

#### spiders/settings/quotes.py 内容如下：

单独的配置文件

```python
settings = {
    #下载中间件调用
    "DOWNLOADER_MIDDLEWARES": {
        'crawlerScrapy.spiders.middelware.downloader.quotes.QuotesDownloader': 543,
        # 'crawlerScrapy.spiders.middelware.downloader.proxy.ProxyDownloader': 200,

    },
    #爬虫中间件调用
    "SPIDER_MIDDLEWARES": {
        'crawlerScrapy.spiders.middelware.spider.quotes.QuotesSpider': 543,
    },
    # 管道调用
    "ITEM_PIPELINES": {
        'crawlerScrapy.spiders.pipeline.quotes.QuotesPipeline': 300
    }
}

```

#### spiders/middelware/downloader/quotes.py 内容如下：（非必要）

下载中间件

```python
class QuotesDownloader(object):
    def __init__(self, spider_data):
        self.spider_data = spider_data
@classmethod
def from_crawler(cls, crawler):
    """
    获取spider的settings参数,返回中间件实例对象
    """
    spider_data = crawler.settings.get("SPIDER_DATA")
    print("### middleware get spider_data: {}".format(spider_data))

    return cls(spider_data)

def process_request(self, request, spider):
    """
    return
        None: 继续处理Request
        Response: 返回Response
        Request: 重新调度
    raise IgnoreRequest:  process_exception -> Request.errback
    """
    print("### call process_request")

def process_response(self, request, response, spider):
    """
    return
        Response: 继续处理Response
        Request: 重新调度
    raise IgnoreRequest: Request.errback
    """
    print("### call process_response")
    return response

def process_exception(self, request, exception, spider):
    """
    return
        None: 继续处理异常
        Response: 返回Response
        Request: 重新调用
    """
    pass
```

#### spiders/middelware/spider/quotes.py 内容如下：（非必要）

爬虫中间件

```python
class QuotesSpider(object):
    def __init__(self, spider_data):
        self.spider_data = spider_data
@classmethod
def from_crawler(cls, crawler):
    """
    获取spider的settings参数,返回中间件实例对象
    """
    spider_data = crawler.settings.get("SPIDER_DATA")
    print("### spider middleware get spider_data: {}".format(spider_data))

    return cls(spider_data)

def process_spider_input(self, response, spider):
    """
    response通过时调用
    return None  继续处理response
    raise Exception
    """

    print("### call process_spider_input")

def process_spider_output(self, response, result, spider):
    """
    response返回result时调用
    return
        iterable of Request、dict or Item
    """
    print("### call process_spider_output")

    for i in result:
        yield i

def process_spider_exception(self, response, exception, spider):
    """
    return
        None
        iterable of Response, dict, or Item
    """
    pass
```

### 注释写法

1.  定义一个函数，冒号结尾换行后开始写函数注释。
2. 注释整个部分使用三引号注释。
3. 一般分为四个部分：整体简介、参数（Parameters）、返回(Returns)和注意(Notes)。
4.  整体简介作用是简短介绍函数的作用。一句话介绍总结函数作用。换行空行，可补充更细节的描述。一行最好不要有太多字符。
5. 空行之后另起一行Parameters，换行，十个-作为分隔符。每遇一个参数另起一行。依次写参数名称，冒号，参数的数据类型，格式，作用。
6. 空行之后另起一行Returns, 换行，十个-作为分隔符。依次介绍返回变量。
7. 空行之后另起一行Notes，写下想告诉读者的注意事项。
8. 另起一行三引号结尾。

```python
def queryURLParams(url='',key=''):
    """
    获取链接后面的参数
    
    Parameters
    ----------
    url : string
        链接地址
    key : string
        获取链接的key
    
    Returns
    ----------
    object类型 

    Notes
    ----------
     参数：
        url="https://www.example.com/?keyword=abc&id=12"
        key='id'
     返回：'12'
     如果没有参数则返回None
    """
```



### 备注

#### 如果不需要使用selenium的情况下的处理：

1. dockerfile文件下代码需要注释

   ```dockerfile
   RUN (echo y | apt-get remove libgdk-pixbuf-2.0-0) && (echo y | apt-get autoremove libgdk-pixbuf2.0-0)
   
   # 记得使用 apt 安装 chrome，而不是 dpkg
   # 下载并安装 chrome, TIPS: dpkg 不会处理依赖，要使用 apt 安装 deb
   RUN (wget -P /code/depends https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb) && (apt install -y /code/depends/google-chrome-stable_current_amd64.deb)
   
   COPY install.py /code/
   RUN python install.py
   ```

2. requirements.txt 文件下 去掉 selenium 插件依赖

#### 中间件启动顺序

download middleware ->  spider middleware  ->  pipeline

#### 处理函数调用顺序

open_spider -> process_request -> process_response -> process_spider_input -> process_spider_output -> spdier close



