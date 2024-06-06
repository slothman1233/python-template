import random
import time
import scrapy
from scrapy import Request
from crawlerScrapy.settings import PROXIES
from crawlerScrapy.spiders.item.selenium_item import SeleniumItem

from crawlerScrapy.spiders.settings.selenium import settings

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from crawlerScrapy.spiders.utils.webdriver import execute_script, input_assign, select_assign


class QuoteSpider(scrapy.Spider):
    a = 1
    name = 'selenium'
    custom_settings = settings
    url_base = "https://fetalmedicine.org/research/assess/preeclampsia/first-trimester"
    # allowed_domains = ['quotes.com']
    # start_urls = [
    #     'https://fetalmedicine.org/research/assess/preeclampsia/first-trimester']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        self.driver = createSelenium()

    def start_requests(self):
        self.a += 1
        self.url = '{}?a={}'.format(self.url_base, self.a)
        yield Request(url=self.url)
        # yield Request(url='https://www.cnblogs.com', callback=self.parse)
    def close(spider, reason):
        spider.driver.close()

    def parse(self, response):
        print("response", response)

        t1 = time.time()

        # print('Before search================')

        # 设置胎儿类型
        select_assign(self.driver, "CalculatorPeMom_twins", 1)

        # 设置胎儿头臀长度
        input_assign(self.driver, 'CalculatorPeMom_crl1', 55)

        # 设置检测时间
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_ga_at').value='01-10-2022'")

        # 母体出生日期
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_dob').value='01-10-1995'")

        # 设置母体身高
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_height').value='160'")

        # 设置母体体重
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_weight').value='55'")

        # 设置种族血统
        select_assign(self.driver, "CalculatorPeMom_race", 4)

        # 设置母体是否孕期抽烟
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_smoking_0').click()")

        # 设置母体是否患有PE
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_mother_pe_0').click()")

        # 设置受孕方式
        select_assign(self.driver, "CalculatorPeMom_conception", 1)

        # 设置是否患有慢性高血压
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_chronic_hypertension_0').click()")

        # 设置是否患有I型糖尿病
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_diabetes_type_i_0').click()")

        # 设置母体是否患有II型糖尿病
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_diabetes_type_ii_0').click()")
        select_assign(self.driver, "CalculatorPeMom_diabetes_drugs", 1)

        # 是否系统性红斑狼疮
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_sle_0').click()")

        # 是否抗磷脂综合症
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_aps_0').click()")

        # 母体是否有个怀孕史
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_previous_0').click()")

        # 设置平均动脉压
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_map').value='5'")

        # 设置平均子动脉PI
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_utpi').value='5'")

        # 设置测量日期
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_biophysical_at').value='01-10-2022'")

        # 设置血清PLGF
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_include_plgf_0').click()")

        # 设置血清Pappa
        execute_script(
            self.driver, "document.querySelector('#CalculatorPeMom_include_pappa_0').click()")

        # 提交计算请求
        execute_script(
            self.driver, "document.querySelector(\"input[type='submit']\").click()")

        WebDriverWait(self.driver, 5).until(
            EC.url_changes(self.url))

        # print(self.driver.current_url)

        try:
            self.driver.find_element(by=By.ID, value="calculator-errors")
            return
        except:
            pass

        item = SeleniumItem()

        # Preeclampsia risk from history only  仅病史中的先兆子痫风险   //*[@id="pe-report"]/div[4]/div[1]/table
        item['value1'] = self.driver.find_element(
            by=By.XPATH, value="//*[@id='pe-report']/div[4]/div[1]/table").text

        # Preeclampsia risk from history plus MAP, UTPI  先兆子痫风险病史加 MAP、UTPI   //*[@id="pe-report"]/div[4]/div[2]/table
        item['value2'] = self.driver.find_element(
            by=By.XPATH, value="//*[@id='pe-report']/div[4]/div[2]/table").text

        # Recommendation 建议 //*[@id="pe-report"]/div[5]
        item['value3'] = self.driver.find_element(
            by=By.XPATH, value="//*[@id='pe-report']/div[5]").text

        # print(value1, value2, value3)

        t2 = time.time()

        print(t2 - t1)

        # print(value1, value2, value3)
        print(item)
        yield item

        if self.a <= 20:
            self.a += 1
            self.url = '{}?a={}'.format(self.url_base, self.a)
            yield Request(url=self.url, callback=self.parse, meta={'name': self.a})


def createSelenium():
    '''
    创建selenuim浏览器
    '''

    proxy_url = random.choice(PROXIES)
    options = webdriver.ChromeOptions()  # 在options 中可添加其他配置属性 如添加header头，添加代理等。
    options.add_argument('--no-sandbox')  # 以 no sandbox方式启动
    options.add_argument('headless')  # headless模式启动

    # options.add_argument('--proxy-server={}'.format(proxy_url))  # 添加代理IP


    # 创建一个driver对象，后续通过这个driver实现对浏览器的操作。
    driver = webdriver.Chrome(
        chrome_options=options, executable_path="../../chromedriver.exe")
    # driver = webdriver.Chrome(chrome_options=options)
    return driver
