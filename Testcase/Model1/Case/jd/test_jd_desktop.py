import os
import unittest
import ddt
import logging
from selenium import webdriver
from time import sleep

from Comm.Log import screen
from Page.basePage import Page

from Comm.data import read_excel
from main import TestCasePath

logger = logging.getLogger('main.jd')
# 读取测试数据
file = os.path.join(TestCasePath, 'Model1/Testdata/jd/test_jd_desktop.xlsx')
test_data = read_excel(file)

PO_jd = 'Page.jd.jd'
PO_search = 'Page.jd.search_jd'


@ddt.ddt  # 数据驱动
class TestJdSearchDesktop(unittest.TestCase):
    """京东搜索测试"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.count = 0
        self.result = []

    @ddt.data(*test_data)  # 数据驱动传具体数据
    def testJdSearchDesktop(self, test_data):
        """京东搜索测试--电脑"""
        url = 'https://www.jd.com'
        keyword = test_data['keyword']
        wait = self.driver.implicitly_wait(5)

        try:
            self.driver.get(url)
            # 实例化jd主页面
            jd = Page(self.driver, PO_jd)
            # 实例化jd搜索结果页面
            jd_search = Page(self.driver, PO_search)
            wait
            # jd主页面的搜索框元素中输入关键字
            jd.oper_elem('search_ipt', keyword)
            wait
            # 操作jd主页面的搜索按钮元素
            jd.oper_elem('search_btn')

            sleep(1)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)

            # jd搜索结果页面，获取结果列表
            lis = jd_search.oper_elems('result_list')

            # 在取到的结果列表中，循环获取商品价格和商品名称，结果存EXCEL就没写了
            for each in lis:
                self.count += 1
                page_each = Page(each, PO_search)
                price = page_each.oper_elem('price')
                name = page_each.oper_elem('pname')
                self.result.append([name, price])

            sleep(1)

        except Exception as E:
            logger.error('error info : %s' % (E))
            screen(test_data['keyword'])

        # 判断是不是取到了60个商品
        self.assertEqual(test_data['count'], self.count)

    def tearDown(self):
        self.driver.quit()
