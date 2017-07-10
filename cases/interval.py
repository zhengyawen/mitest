# -*- coding:utf-8 -*-
import unittest
from appium import webdriver
from time import sleep
from testcase import testclass
import HTMLTestRunner
import re
import selenium
import random
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Interval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('start setup')
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.0'
        desired_caps['deviceName'] = 'b3ce25b8'
        desired_caps['appPackage'] = 'com.xiaomi.smarthome'
        desired_caps['appActivity'] = '.SmartHomeMainActivity'
        desired_caps['newCommandTimeout']='300'
        desired_caps['unicodeKeyboard']=True
        desired_caps['resetKeyboard']=True

        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print('tearDown')


    # @unittest.skip('skip')
    #时间间隔反复开关
    def test_interval1(self):
        testclass.enter(self)
        testclass.swipeUp(self)
        self.driver.find_element_by_name(u'间隔提醒').click()
        sleep(3)
        # 判断是否进入了间隔提醒页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text, '间隔提醒','进入间隔提醒失败')

        result=True
        #反复开关5次
        for i in range(5):
            old=testclass.switchButtonStatus(self)
            testclass.switchButtonOnOff(self)
            new = testclass.switchButtonStatus(self)
            result = result and (old != new)
        #判断结果
        self.assertEqual(True,result,'开关时间间隔失败')
        # 返回主页
        testclass.pressBack(self)
        # 退出插件
        testclass.pressBack(self)

    #设置时间间隔和重新计时
    def test_iterval2(self):
        testclass.enter(self)
        #进入时间间隔设置
        testclass.swipeUp(self)
        self.driver.find_element_by_name(u'间隔提醒').click()
        # 判断是否进入了间隔提醒页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text, '间隔提醒', '进入间隔提醒失败')
        #打开时间间隔
        status=testclass.switchButtonStatus(self)
        if status==False:
            testclass.switchButtonOnOff(self)
        # a= self.driver.page_source
        # f = open("report/alarm-pagesource.txt", 'w')
        # f.write(a)
        # f.close()
        #进入设置
        self.driver.find_element_by_name('设置间隔时间').click()
        #设定时长
        time=random.randint(1,60)
        print '设定间隔时长为',time
        sleep(2)
        el=self.driver.find_element_by_id('com.inshow.watch.android:id/numberpicker_input')
        original=int(el.text)
        testclass.swipeChoose(self,el,original,time)
        self.driver.find_element_by_name('确定').click()

        #判断设置结果
        timenow=self.driver.find_element_by_id('com.inshow.watch.android:id/tvRemindTopTip').text
        x=re.sub("\D","",timenow)
        self.assertEqual(int(x),time,'设定时间间隔失败'  )

        #判断倒计时结果
        sleep(15)
        now=self.driver.find_element_by_id('com.inshow.watch.android:id/tvRemain').get_attribute('text')
        self.assertNotEqual(now,"%d:59"%(time-1),'时间间隔倒计时失败')

        #重新计时
        self.driver.find_element_by_name('重新计时').click()
        end= self.driver.find_element_by_id('com.inshow.watch.android:id/tvRemain').get_attribute('text')
        # self.assertEqual(end, original, '时间间隔重新计时失败')
        self.assertNotEqual(end, now, '设定时间间隔失败')
        #返回主页
        testclass.pressBack(self)

        # 退出插件
        testclass.pressBack(self)



if __name__=='__main__':

    # unittest.main()
    suite=unittest.TestSuite(unittest.makeSuite(Interval))
    # 获取当前时间，这样便于下面的使用。
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 打开一个文件，将result写入此file中
    fp = open("../report/result" + now + ".html", 'wb')
    # 执行测试

    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='test result',description=u'result:')
    runner.run(suite)
    fp.close()



