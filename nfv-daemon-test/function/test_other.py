# -- coding: utf-8 --
import unittest
import sys
import datetime

sys.path.append("../../nfv-daemon-test")
from lib import base_function

class test_other(unittest.TestCase):
    #PIM list测试
    @classmethod
    def setUpClass(cls):
        cls.zone = '.000Z'
        cls.ManagerId = "BJ_PIM_1"
        token = base_function.login(cls.ManagerId, base_function.dsm_username, base_function.dsm_passwd)
        cls.token1 = eval(token.content)['Token']
        base_function.DeleteSubcription(cls.token1,ManagerId=cls.ManagerId)
        token = base_function.login(cls.ManagerId, base_function.dsm_username, base_function.dsm_passwd)
        cls.token = eval(token.content)['Token']
        base_function.CreateSubcription(cls.token,ManagerId=cls.ManagerId)

    def test_NFV_Daemon_ListResDetails_01(self):
        #查询配置信息
        print self.ManagerId
        res = base_function.ListResDetails(self.token,self.ManagerId)
        print res.content
        self.assertEqual(200,res.status_code)
        self.assertIn(base_function.url,res.content)

    def test_NFV_Daemon_ListResDetails_02(self):
        # 查询配置信息,ManagerId错误
        res = base_function.ListResDetails(self.token,"manageid-error")
        self.assertEqual(404, res.status_code)

    def test_NFV_Daemon_ListResDetails_03(self):
        #下载配置信息
        result = base_function.ListResDetails(self.token, self.ManagerId)
        print result.json()
        result = result.text
        fileurl = eval(result)['FileUri']
        print fileurl
        res = base_function.download_file(self.token,fileurl)
        self.assertEqual(200,res.status_code)

    def test_NFV_Daemon_ListResDetails_04(self):
        #下载配置信息，信息不存在
        fileurl = base_function.url + "/v1/dsmCm/files/20160601-140112.gz"
        res = base_function.download_file(self.token, fileurl)
        print res.content,res.status_code
        self.assertEqual(404,res.status_code)

    def test_NFV_Daemon_ListResDetails_05(self):
        #下载配置信息，token信息错误
        fileurl = base_function.url + "/v1/dsmCm/files/20160601-140112.gz"
        res = base_function.download_file("token-error", fileurl)
        self.assertEqual(401,res.status_code)

    def test_NFV_Daemon_ListHistoryMetrics_01(self):
        #补采1天性能数据
        endtime = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + self.zone
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=1)).isoformat() + self.zone

        res = base_function.ListHistoryMetrics(self.token,self.ManagerId,starttime,endtime)

        fileurls = res.json()['FileUris']
        if fileurls != None:
            file_num = len(fileurls)
        else:
            file_num = 0
        print fileurls
        self.assertEqual(200,res.status_code)
        self.assertTrue(file_num>0)

    def test_NFV_Daemon_ListHistoryMetrics_02(self):
        #补采性能数据，ManagerId错误
        endtime = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + self.zone
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=1)).isoformat() + self.zone
        res = base_function.ListHistoryMetrics(self.token, 'managerid-error', starttime, endtime)
        print res.content
        self.assertEqual(404,res.status_code)

    def test_NFV_Daemon_ListHistoryMetrics_03(self):
        #补采性能数据，开始时间大于结束时间
        endtime = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + self.zone
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=1)).isoformat() + self.zone
        res = base_function.ListHistoryMetrics(self.token, self.ManagerId, endtime, starttime)
        self.assertEqual(400,res.status_code)

    def test_NFV_Daemon_ListHistoryMetrics_04(self):
        #补采性能数据，日期格式错误
        endtime = datetime.datetime.utcnow().replace(microsecond=0)
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=7))
        res = base_function.ListHistoryMetrics(self.token, self.ManagerId, starttime, endtime)
        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_ListHistoryMetrics_05(self):
        #补采7天以内性能数据
        endtime = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + self.zone
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=7)).isoformat() + self.zone
        res = base_function.ListHistoryMetrics(self.token, self.ManagerId,starttime, endtime)

        fileurls = res.json()['FileUris']
        if fileurls != None:
            file_num = len(fileurls)
        else:
            file_num = 0
        self.assertEqual(200, res.status_code)
        self.assertTrue(file_num > 0)

    def test_NFV_Daemon_ListHistoryMetrics_06(self):
        #补采七天以前性能数据
        endtime = (datetime.datetime.utcnow().replace(microsecond=0)- datetime.timedelta(days=7)).isoformat() + self.zone
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=8)).isoformat() + self.zone
        res = base_function.ListHistoryMetrics(self.token, self.ManagerId, starttime, endtime)

        fileurls = res.json()['FileUris']
        if fileurls != None:
            file_num = len(fileurls)
        else:
            file_num = 0
        self.assertEqual(200, res.status_code)
        self.assertTrue(file_num == 0)

    def test_NFV_Daemon_ListHistoryMetrics_07(self):
        #补采性能数据，不带时间
        res = base_function.ListHistoryMetrics_notime(self.token, self.ManagerId)

        fileurls = res.json()['FileUris']
        if fileurls != None:
            file_num = len(fileurls)
        else:
            file_num = 0
        self.assertEqual(200, res.status_code)
        self.assertTrue(file_num > 0)

    def test_NFV_Daemon_ListHistoryMetrics_08(self):
        #下载性能数据
        res = base_function.ListHistoryMetrics_notime(self.token,self.ManagerId)
        fileurls = res.json()['FileUris']
        if fileurls != None:
            fileurl = fileurls[-1]

        res = base_function.download_file(self.token,fileurl)
        self.assertEqual(200,res.status_code)

        if base_function.ungz_file(fileurl) == 0:
            base_function.check_json_file(source_file,target_file)

    def test_NFV_Daemon_ListHistoryMetrics_09(self):
        #下载性能数据，文件不存在
        fileuri = base_function.url+'/v1/dsmPm/files/test1111.tar.gz'
        res = base_function.download_file(self.token, fileuri)
        self.assertEqual(404, res.status_code)

    def test_NFV_Daemon_ListHistoryLogs_01(self):
        #补采日志数据，1天内
        endtime = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + self.zone
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=1)).isoformat() + self.zone
        res = base_function.ListHistoryLogs(self.token, self.ManagerId, starttime, endtime)
        print endtime
        print res.content
        fileurls = res.json()['FileUris']
        if fileurls != None:
            file_num = len(fileurls)
        else:
            file_num = 0

        self.assertEqual(200, res.status_code)
        self.assertTrue(file_num > 0)

    def test_NFV_Daemon_ListHistoryLogs_02(self):
        #补采日志数据，ManagerId错误
        endtime = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + self.zone
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=1)).isoformat() + self.zone
        res = base_function.ListHistoryLogs(self.token, 'managerid-error', starttime, endtime)

        self.assertEqual(404, res.status_code)

    def test_NFV_Daemon_ListHistoryLogs_03(self):
        #补采日志数据，开始时间大于结束时间
        endtime = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + self.zone
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=1)).isoformat() + self.zone
        res = base_function.ListHistoryLogs(self.token, self.ManagerId, endtime, starttime)

        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_ListHistoryLogs_04(self):
        #补采日志数据，日期格式错误
        endtime = datetime.datetime.utcnow().replace(microsecond=0)
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=1))
        res = base_function.ListHistoryLogs(self.token, self.ManagerId, starttime, endtime)

        self.assertEqual(400, res.status_code)

    def test_NFV_Daemon_ListHistoryLogs_05(self):
        #补采七天内的日志数据
        endtime = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + self.zone
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=7)).isoformat() + self.zone
        res = base_function.ListHistoryLogs(self.token, self.ManagerId, starttime, endtime)

        fileurls = res.json()['FileUris']
        if fileurls != None:
            file_num = len(fileurls)
        else:
            file_num = 0

        self.assertEqual(200, res.status_code)
        self.assertTrue(file_num > 0)

    def test_NFV_Daemon_ListHistoryLogs_06(self):
        #补采七天以前的日志数据
        endtime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=7)).isoformat() + self.zone
        starttime = (datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(days=8)).isoformat() + self.zone
        res = base_function.ListHistoryLogs(self.token, self.ManagerId, starttime, endtime)

        fileurls = res.json()['FileUris']
        if fileurls != None:
            file_num = len(fileurls)
        else:
            file_num = 0

        self.assertEqual(200, res.status_code)
        self.assertTrue(file_num == 0)

    def test_NFV_Daemon_ListHistoryLogs_07(self):
        #补采日志数据,不带时间
        res = base_function.ListHistoryLogs_notime(self.token, self.ManagerId)

        fileurls = res.json()['FileUris']
        if fileurls != None:
            file_num = len(fileurls)
        else:
            file_num = 0
        self.assertEqual(200, res.status_code)
        self.assertTrue(file_num > 0)

    def test_NFV_Daemon_ListHistoryLogs_08(self):
        #下载日志数据
        res = base_function.ListHistoryLogs_notime(self.token, self.ManagerId)
        fileurls = res.json()['FileUris']
        if fileurls != None:
            fileuri = fileurls[-1]

        res = base_function.download_file(self.token,fileuri)
        self.assertEqual(200,res.status_code)

    def test_NFV_Daemon_ListHistoryLogs_09(self):
        # 下载日志数据，文件不存在
        fileuri = base_function.url + '/v1/dsmLog/files/test1111.tar.gz'
        res = base_function.download_file(self.token, fileuri)
        self.assertEqual(404, res.status_code)