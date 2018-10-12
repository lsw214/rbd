# -- coding: utf-8 --
import unittest
import sys
sys.path.append('../../nfv-daemon-test')
from lib import base_function
import json

class Test_NFV_login(unittest.TestCase):
    #PIM登录DSM测试
    def test_NFV_Daemon_login_01(self):
        #登录，ManagerId长度为36
        ManagerId = '012345678901234567890123456789123456'
        res = base_function.login(ManagerId,base_function.dsm_username,base_function.dsm_passwd)
        print json.dumps(res.content)
        self.assertEqual(201,res.status_code)

    def test_NFV_Daemon_login_02(self):
        #登录，ManagerId长度为37
        ManagerId = '0123456789012345678901234567891234567'
        res = base_function.login(ManagerId, base_function.dsm_username, base_function.dsm_passwd)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_login_03(self):
        # 登录，ManagerId长度为0
        ManagerId = ''
        res = base_function.login(ManagerId, base_function.dsm_username, base_function.dsm_passwd)
        self.assertEqual(400, res.status_code)
    def test_NFV_Daemon_login_04(self):
        #登录，ManagerId类型为Int
        ManagerId = 123456
        print base_function.dsm_username
        res = base_function.login(ManagerId, base_function.dsm_username, base_function.dsm_passwd)
        print res.content,res.status_code
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_login_05(self):
        # 登录，username类型为Int
        ManagerId = "BJ-PIM-1"
        username = 123456
        res = base_function.login(ManagerId, username, base_function.dsm_passwd)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_login_06(self):
        # 登录，username长度为空
        ManagerId = "BJ-PIM-1"
        username = ""
        res = base_function.login(ManagerId, username, base_function.dsm_passwd)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_login_07(self):
        # 登录，username长度为16
        ManagerId = "BJ-PIM-1"
        username = "0123456789123456"

        res = base_function.login(ManagerId, username, base_function.dsm_passwd)
        self.assertEqual(201, res.status_code)

    def test_NFV_Daemon_login_08(self):
        # 登录，username长度为17
        ManagerId = "BJ-PIM-1"
        username = "01234567891234567"
        res = base_function.login(ManagerId, username, base_function.dsm_passwd)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_login_09(self):
        # 登录，password类型为int
        ManagerId = "BJ-PIM-1"
        passwd = "0123456789123456"
        res = base_function.login(ManagerId, base_function.dsm_username, int(passwd))
        print res.content
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_login_10(self):
        # 登录，password长度为空
        ManagerId = "BJ-PIM-1"
        passwd = ""
        res = base_function.login(ManagerId, base_function.dsm_username, passwd)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_login_11(self):
        # 登录，password长度为16
        ManagerId = "BJ-PIM-1"
        passwd = "0123456789123456"
        res = base_function.login(ManagerId, base_function.dsm_username, passwd)
        self.assertEqual(201, res.status_code)

    def test_NFV_Daemon_login_12(self):
        # 登录，password长度为17
        ManagerId = "BJ-PIM-1"
        passwd = "01234567891234567"
        res = base_function.login(ManagerId, base_function.dsm_username, passwd)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_login_13(self):
        # 登录，password错误
        ManagerId = "BJ-PIM-1"
        res = base_function.login(ManagerId, base_function.dsm_username,'admin11')
        print res.text
        self.assertEqual(401, res.status_code)

    def test_NFV_Daemon_login_14(self):
        # 登录，ManagerId包含特殊字符
        ManagerId = "BJ-PIM-1~!@#$%^&*()_+}{:"
        res = base_function.login(ManagerId, base_function.dsm_username,base_function.dsm_passwd)
        print res.text
        self.assertEqual(201, res.status_code)
