# -- coding: utf-8 --
import requests
import configparser
import os
import json
from requests.packages import urllib3
import gzip
import tarfile
#解析conf.conf配置文件
################################################################
CPN = os.getcwd()
ppn = os.path.abspath(os.path.join(CPN,os.pardir))
fp = os.path.join(ppn,'config.conf')
conf = configparser.ConfigParser()
conf.read(fp)
################################################################
url = conf.get('default','DSM_url')
pim_url = conf.get('default','PIM_url')
dsm_username = conf.get('DSM','username')
dsm_passwd = conf.get('DSM','password')
pim_username = conf.get('PIM','username')
pim_password = conf.get('PIM','password')
################################################################

cert = ('../lib/cert.pem','../lib/key.pem')
urllib3.disable_warnings()

def login(ManagerId,username,password):
    #登录DSM
    try:
        post_url = url + '/v1/auth/login'
        headers = {"Content-Type":"application/json;charset=UTF-8"}
        data = {'ManagerId':ManagerId,'Username':username,'Password':password}
        data = json.dumps(data)
        res = requests.post(post_url,data=data,headers=headers,verify=False)
        return res
    except Exception,res:
        return res

def CreateSubcription(token,
                      ManagerId="BJ_PIM_1",
                      Username=pim_username,
                      Password=pim_password,
                      IdentityUri=pim_url,
                      LogPeriod=1,
                      Period=5,
                      Heartbeat=30):
    #创建订阅
    try:
        post_url = url + '/v1/dsmJobs'
        headers = {
            "Content-Type":"application/json;charset=UTF-8",
            "X-XSRF-Token":token
        }
        data = {
            "ManagerId":ManagerId,
            "Username":Username,
            "Password":Password,
            "IdentityUri":IdentityUri,
            "LogPeriod":LogPeriod,
            "Period":Period,
            "Heartbeat":Heartbeat
        }
        data = json.dumps(data)
        res = requests.post(post_url,data=data,headers=headers,verify=False,timeout=30)
        return res
    except Exception,res:
        return res

def ListSubcriptions(token,ManagerId):
    #查询订阅
    try:
        managerid = "ManagerId="+ManagerId
        post_url = url + '/v1/dsmJobs'
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-XSRF-Token": token
        }
        res = requests.get(post_url,params=managerid,headers=headers,verify=False)
        return res
    except Exception,res:
        return res

def DeleteSubcription(token,ManagerId):
    #删除订阅
    try:
        post_url = url + '/v1/dsmJobs/' + ManagerId
        # print post_url
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-XSRF-Token": token
        }
        res = requests.delete(post_url,headers=headers,verify=False)
        return res
    except Exception,res:
        return res

def ListResDetails(token,ManagerId):
    #查询配置
    try:
        managerid = "ManagerId="+ManagerId
        post_url = url + '/v1/dsmCm'
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-XSRF-Token": token
        }
        res = requests.get(post_url,params=managerid,headers=headers,verify=False)
        return res
    except Exception,res:
        return res

def ListHistoryMetrics(token,ManagerId,starttime,endtime):
    #补采性能数据
    try:
        post_url = url + '/v1/dsmPm/hisMetrics'
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-XSRF-Token": token
        }
        params = {"ManagerId":ManagerId,"StartTime":starttime,"EndTime":endtime}
        res = requests.get(post_url,params=params,headers=headers,verify=False)
        return res
    except Exception,res:
        return res

def ListHistoryMetrics_notime(token,ManagerId):
    #补采性能数据，不带时间
    try:
        post_url = url + '/v1/dsmPm/hisMetrics'
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-XSRF-Token": token
        }
        params = {"ManagerId":ManagerId}
        res = requests.get(post_url,params=params,headers=headers,verify=False)
        return res
    except Exception,res:
        return res

def ListHistoryLogs(token,ManagerId,starttime,endtime):
    #补采日志数据
    try:
        post_url = url + '/v1/dsmLog/hisLogs'
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-XSRF-Token": token
        }
        params = {"ManagerId":ManagerId,"StartTime":starttime,"EndTime":endtime}
        res = requests.get(post_url,params=params,headers=headers,verify=False)
        return res
    except Exception,res:
        return res

def ListHistoryLogs_notime(token,ManagerId):
    #补采日志数据,不带时间
    try:
        post_url = url + '/v1/dsmLog/hisLogs'
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-XSRF-Token": token
        }
        params = {"ManagerId":ManagerId}
        res = requests.get(post_url,params=params,headers=headers,verify=False)
        return res
    except Exception,res:
        return res

def download_file(token,url):
    #下载文件，并在存放在data目录中
    try:
        file_name = url.split('/')[-1]
        headers = {"X-XSRF-Token": token}
        res = requests.get(url,headers=headers,verify=False)
        with open("../data/"+file_name,'wb') as f:
            f.write(res.content)
        return res
    except Exception,res:
        return res

def ungz_file(url):
    try:
        #解压gz
        gz_file  = "../data/"+url.split('/')[-1]
        tar_file = gz_file.replace(".gz","")
        g_file = gzip.GzipFile(gz_file)
        open(tar_file,'w+').write(g_file.read())
        g_file.close()

        #解压tar
        tar = tarfile.open(tar_file)
        names = tar.getnames()
        tar.extract(names[0],"../data/")
        tar.close()
        if os.path.isfile("../data/"+names[0]):
            return 0
        else:
            return 1
    except EXception,ex:
        print "ungz failed! "
        print ex

def check_json_file(source_file,target_file):
    pass