import os
import unittest
import ddt
import random
import json
import requests
from time import sleep
from Comm.data import read_excel
from Comm.encryption import make_md5
from main import TestCasePath
from APIs.base_api import BaseAPI, check_result


# 开通普通个人的百度翻译接口，设置appid和appkey.
app_id = "13134106065"
app_key = "glnts7218"
# 获取测试数据
file = os.path.join(TestCasePath, 'C:\\Users\\yinghai\\PycharmProjects\\TestFrame\\Testcase\\API\\Testdata\\baidu_fanyi.xlsx')
test_data = read_excel(file)
api = 'APIs.fanyi.baidu'


@ddt.ddt
class TestBaiduFanyi(unittest.TestCase):
    """百度翻译接口测试"""

    def setUp(self):
        self.api = BaseAPI(api)

    @ddt.data(*test_data)
    def test_baidu_fanyi(self, test_data):
        """百度翻译接口测试"""
        api = self.api

        # Build test_data，这是些动态参数，在这里计算
        test_data['fanyi.req.appid'] = app_id
        salt = random.randint(32768, 65536)
        test_data['fanyi.req.salt'] = salt
        sign = make_md5(app_id + test_data['fanyi.req.q'] + str(salt) + app_key)
        test_data['fanyi.req.sign'] = sign

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = api.payload(test_data )

        # Send request
        r = requests.post(api.url, params=payload, headers=headers)
        result = r.json()
        expected = api.load_expected(test_data)
        self.assertEqual(r.status_code, 200)
        check_result(self, expected, result) # 简单的模板验证，大家最好自己写验证。

        sleep(0.5)
