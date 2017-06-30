# -*- coding:utf-8 -*-
import unittest
import HTMLTestRunner
import time
from testcase import test1
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')



if __name__=='__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    #全部运行，不计顺序
    # suite = unittest.TestSuite(unittest.makeSuite(test1.Dtest))

    #单挑运行
    suite.addTest(test1.Dtest('test_enter'))#进入插件
    # suite.addTest(test1.Dtest('test_cityTime'))#添加世界城市
    # suite.addTest(test1.Dtest('test_citySearch')) # 搜索添加城市
    # # suite.addTest(test1.Dtest('test_citySlide')) #滑动查看城市
    # suite.addTest(test1.Dtest('test_intervalOnOff'))#时间间隔反复开关
    # suite.addTest(test1.Dtest('test_setIterval'))#设置时间间隔和重新计时
    # suite.addTest(test1.Dtest('test_addAlarm'))#添加闹钟,现在闹钟添加功能取消
    # suite.addTest(test1.Dtest('test_alterAlarm'))#修改闹钟
    # suite.addTest(test1.Dtest('test_more'))# 进入设置
    # suite.addTest(test1.Dtest('test_setBodyInfo'))# 设置身体信息
    # suite.addTest(test1.Dtest('test_setDeviceInfo'))#进入设备信息

    #
    # # # 获取当前时间，这样便于下面的使用。
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 打开一个文件，将result写入此file中
    fp = open("report/result" + now + ".html", 'wb')
    # 执行测试

    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='test result',description='result:')
    runner.run(suite)
    fp.close()
    #
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)