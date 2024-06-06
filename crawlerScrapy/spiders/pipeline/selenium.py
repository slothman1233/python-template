
import pymysql

from crawlerScrapy.settings import MYSQL_CHARSET, MYSQL_DB, MYSQL_HOST, MYSQL_PASSWD, MYSQL_PORT, MYSQL_USE_UNICODE, MYSQL_USER


class SeleniumPipeline(object):
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
        # print("### pipeline get spider_data: {}".format(spider_data))

        return cls(spider_data)

    def process_item(self, item, spider):
        """
        return Item 继续处理
        raise DropItem 丢弃
        """
        # print("### call process_item")
        
        # sql语句
        insert_sql = """
        insert into test1(value1, value2, value3) VALUES (%s,%s,%s)
        """
        try:
            # 执行插入数据到数据库操作
            self.cursor.execute(
                insert_sql, (item['value1'], item['value2'], item['value3']))

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

        # print("### spdier open {}".format(spider.name))

    def close_spider(self, spider):
        """
        spider关闭时调用
        """
        self.connect.close()
        # print("### spdier close {}".format(spider.name))
