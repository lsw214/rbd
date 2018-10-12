# -- coding: utf-8 --
import unittest
import sys
sys.path.append('../../nfv-daemon-test')
from lib import base_function

class Test_NFV_subcription(unittest.TestCase):
    #订阅相关测试
    @classmethod
    def setUpClass(cls):
        cls.ManagerId = "BJ_PIM_1"
        token = base_function.login(cls.ManagerId, base_function.dsm_username, base_function.dsm_passwd)
        token = eval(token.content)['Token']
        base_function.DeleteSubcription(token, cls.ManagerId)

    def setUp(self):
        token = base_function.login(self.ManagerId, base_function.dsm_username, base_function.dsm_passwd)
        self.token = eval(token.content)['Token']

    def tearDown(self):
        base_function.DeleteSubcription(self.token,self.ManagerId)

    def test(self):
        pass

    def test_NFV_Daemon_CreateSubcription_01(self):
        #订阅
        res = base_function.CreateSubcription(self.token)
        print res.content
        self.assertEqual(201,res.status_code)

    def test_NFV_Daemon_CreateSubcription_02(self):
        #订阅,LogPeriod为string类型
        LogPeriod = "1"
        res = base_function.CreateSubcription(self.token,LogPeriod=LogPeriod)
        print res.content
        self.assertEqual(400,res.status_code)

    def test_NFV_Daemon_CreateSubcription_03(self):
        #订阅,LogPeriod为float类型
        LogPeriod = 1.5
        res = base_function.CreateSubcription(self.token, LogPeriod=LogPeriod)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_CreateSubcription_04(self):
        #订阅,LogPeriod长度为8
        LogPeriod = 12345678
        res = base_function.CreateSubcription(self.token, LogPeriod=LogPeriod)
        self.assertEqual(201, res.status_code)

    def test_NFV_Daemon_CreateSubcription_05(self):
        # 订阅,LogPeriod长度为9
        LogPeriod = 123456789
        res = base_function.CreateSubcription(self.token, LogPeriod=LogPeriod)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_CreateSubcription_06(self):
        # 订阅,LogPeriod设置为0
        LogPeriod = 0
        res = base_function.CreateSubcription(self.token, LogPeriod=LogPeriod)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_CreateSubcription_07(self):
        #订阅,Period为string类型
        Period = '15'
        res = base_function.CreateSubcription(self.token, Period=Period)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_CreateSubcription_08(self):
        # 订阅,Period为float类型
        Period = 15.5
        res = base_function.CreateSubcription(self.token, Period=Period)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_CreateSubcription_09(self):
        #订阅,Period长度为8
        Period = 10000000
        res = base_function.CreateSubcription(self.token, Period=Period)
        print res.content
        self.assertEqual(201, res.status_code)

    def test_NFV_Daemon_CreateSubcription_10(self):
        # 订阅,Period长度为9
        Period = 123456789
        res = base_function.CreateSubcription(self.token, Period=Period)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_CreateSubcription_11(self):
        # 订阅,Period设置为0
        Period = 0
        res = base_function.CreateSubcription(self.token, Period=Period)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_CreateSubcription_12(self):
        # 订阅,Period设置为1
        Period = 1
        res = base_function.CreateSubcription(self.token, Period=Period)
        self.assertEqual(400, res.status_code)
    def test_NFV_Daemon_CreateSubcription_13(self):
        # 订阅,Period设置为5
        Period = 5
        res = base_function.CreateSubcription(self.token, Period=Period)
        self.assertEqual(201, res.status_code)
    def test_NFV_Daemon_CreateSubcription_14(self):
        #订阅,Heartbeat为string类型
        Heartbeat = "8"
        res = base_function.CreateSubcription(self.token, Heartbeat=Heartbeat)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_CreateSubcription_15(self):
        # 订阅,Heartbeat为float类型
        Heartbeat = 8.8
        res = base_function.CreateSubcription(self.token, Heartbeat=Heartbeat)
        self.assertEqual(400, res.status_code)
    def test_NFV_Daemon_CreateSubcription_16(self):
        # 订阅,Heartbeat长度为8
        Heartbeat = 12345678
        res = base_function.CreateSubcription(self.token, Heartbeat=Heartbeat)
        self.assertEqual(201, res.status_code)
    def test_NFV_Daemon_CreateSubcription_17(self):
        # 订阅,Heartbeat长度为9
        Heartbeat = 123456789
        res = base_function.CreateSubcription(self.token, Heartbeat=Heartbeat)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_CreateSubcription_18(self):
        # 订阅,Heartbeat设置为0
        Heartbeat = 0
        res = base_function.CreateSubcription(self.token, Heartbeat=Heartbeat)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_CreateSubcription_19(self):
        #订阅，ManagerId重复订阅
        base_function.CreateSubcription(self.token)
        res = base_function.CreateSubcription(self.token)
        self.assertEqual(403, res.status_code)

    def test_NFV_Daemon_CreateSubcription_20(self):
        # 订阅，IdentityUri重复订阅
        base_function.CreateSubcription(self.token)

        manageid = 'BJ_PIM_2'
        token = base_function.login(manageid,"admin","admin")
        token = eval(token.content)['Token']
        print token

        res = base_function.CreateSubcription(token,ManagerId=manageid)
        base_function.DeleteSubcription(token, ManagerId=manageid)
        print res.content
        self.assertEqual(403, res.status_code)

    def test_NFV_Daemon_CreateSubcription_21(self):
        #订阅，user中manageId不存在
        base_function.CreateSubcription(self.token,self.ManagerId)
        base_function.DeleteSubcription(self.token,self.ManagerId)
        res = base_function.CreateSubcription(self.token,self.ManagerId)
        print res.content
        self.assertEqual(401,res.status_code)

    def test_NFV_Daemon_ListSubcriptions_01(self):
        #正确的ManagerId请求
        base_function.CreateSubcription(self.token)
        res = base_function.ListSubcriptions(self.token,self.ManagerId)
        print res.content
        self.assertEqual(200,res.status_code)

    def test_NFV_Daemon_ListSubcriptions_02(self):
        #错误的ManagerId请求
        base_function.CreateSubcription(self.token)
        res = base_function.ListSubcriptions(self.token, ManagerId='BJ_PIM_11111')
        self.assertEqual(404, res.status_code)

    def test_NFV_Daemon_DeleteSubcription_01(self):
        #删除订阅
        base_function.CreateSubcription(self.token)
        res = base_function.DeleteSubcription(self.token,self.ManagerId)
        self.assertEqual(204,res.status_code)

    def test_NFV_Daemon_DeleteSubcription_02(self):
        #删除订阅，ManagerId错误
        base_function.CreateSubcription(self.token)
        res = base_function.DeleteSubcription(self.token, ManagerId='BJ_PIM_11111')
        self.assertEqual(404, res.status_code)