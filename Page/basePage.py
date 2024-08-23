from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import importlib
import logging

SimpleActions = ['clear()', 'send_keys()', 'click()', 'submit()', 'size', 'text', 'is_displayed()', 'get_attribute()']
logger = logging.getLogger('main.page')


class Page(object):

    def __init__(self, driver, page):
        self.driver = driver
        self.page = page
        self.elements = get_page_elements(page)
        self.by = ()
        self.action = None

    def _get_page_elem(self, elem):
        # 获取定位元素的 by，以及操作action
        for each in self.elements:
            if each['name'] == elem:
                self.by = each['by']
                if 'action' in each and each['action'] is not None:
                    self.action = each['action']
                else:
                    self.action = None

    def oper_elem(self, elem, args=None):
        self._get_page_elem(elem)
        cmd = self._selenium_cmd('find_element', args)
        return eval(cmd)

    def oper_elems(self, elem, args=None):
        self._get_page_elem(elem)
        cmd = self._selenium_cmd('find_elements', args)
        return eval(cmd)

    def _selenium_cmd(self, find_type='find_element', args=None):
        # 拼接 selenium 查找命令， 查找单个元素时find_type为'find_element'，多个元素时为'find_elements'
        cmd = 'self.driver.' + find_type + '(*self.by)'
        if self.action:
            if self.action in SimpleActions:
                cmd = cmd + '.' + self.action
                if args:
                    cmd = cmd[:-1] + 'args' + ')'
        return cmd


def get_page_elements(page):
    """动态加载页面定义文件，获取文件中定义的元素列表elements"""
    elements = None
    if page:
        try:
            m = importlib.import_module(page)
            elements = m.elements
        except Exception as e:
            logger.error('error info : %s' % (e))
    return elements




