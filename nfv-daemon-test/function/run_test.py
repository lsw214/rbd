# -- coding: utf-8 --
import unittest
import sys,time
import test_login,test_Subcription,test_other
sys.path.append('../../nfv-daemon-test')
from lib import HTMLTestRunner

#add test suit
suit = unittest.TestSuite()
suit.addTest(unittest.makeSuite(test_login.Test_NFV_login))
suit.addTest(unittest.makeSuite(test_Subcription.Test_NFV_subcription))
suit.addTest(unittest.makeSuite(test_other.test_other))

#start testcase and Generating test reports
curr_time = time.strftime('%y-%m-%d-%H-%M-%S',time.localtime(time.time()))
report_file = '../report/report_'+curr_time+'.html'
fp = open(report_file,'w+')
runer = HTMLTestRunner.HTMLTestRunner(stream=fp,title='NFV DAEMON Test')
runer.run(suit)