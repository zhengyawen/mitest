# -*- coding:utf-8 -*-
import unittest
import HTMLTestRunner
import time
from testcase import alarm,city,interval,setting
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')



if __name__=='__main__':
    # 构造测试集

    suite4=unittest.TestLoader().loadTestsFromTestCase(alarm.Alarm)
    suite2=unittest.TestLoader().loadTestsFromTestCase(city.City)
    suite3=unittest.TestLoader().loadTestsFromTestCase(interval.Interval)
    suite1=unittest.TestLoader().loadTestsFromTestCase(setting.Setting)
    #
    # suite = unittest.TestSuite([suite1,suite2,suite3,suite4])

    suite = unittest.TestSuite()
    suite.addTest(setting.Setting('test_set1'))
    #生成报告
    # # 获取当前时间，这样便于下面的使用。
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 打开一个文件，将result写入此file中
    fp = open("report/result" + now + ".html", 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='test result',description='result:')
    runner.run(suite)
    fp.close()

