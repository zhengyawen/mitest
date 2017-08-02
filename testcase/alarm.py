# -*- coding:utf-8 -*-
import unittest
from appium import webdriver
from time import sleep
import testcase.testclass
import HTMLTestRunner
import random
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Alarm(unittest.TestCase):
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


     # @unittest.skip(u'忽略该挑用例')
    #添加闹钟
    option = [u'只响一次', u'每天', u'法定工作日', u'法定节假日', u'周一至周五']
    apm=[u'上午',u'下午']
    def test_alarm1(self):
        testcase.testclass.enter(self)
        # 进入闹钟设置
        testcase.testclass.swipeUp(self)
        self.driver.find_element_by_name(u'闹钟').click()
        sleep(1)
        # 判断是否进入了闹钟页面
        self.assertEqual(self.driver.find_element_by_id('com.inshow.watch.android:id/title_bar_title').text, '闹钟',
                         '进入闹钟失败')

        #定义闹钟格式
        alarm=[
            [Alarm.option[random.randint(0,4)],Alarm.apm[random.randint(0,1)],random.randint(1,12),random.randint(0,59)],
            # [Dtest.option[1],u'上午',4,30]
        ]
        for i in alarm:
            # 进入添加页面
            self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
            sleep(2)
            self.assertNotEqual(self.driver.page_source.find(u'设置闹钟'), -1, '进入添加闹钟页面失败')
            #设置闹钟
            print "设置闹钟", i[0].encode('utf-8'), i[1].encode('utf-8'), i[2], i[3]
            testcase.testclass.alartSetting(self, i[0], i[1], i[2], i[3])
        testcase.testclass.screenshot(self)
        # 返回主页
        testcase.testclass.pressBack(self)

        # 退出插件
        testcase.testclass.pressBack(self)
        # 修改闹钟

    def test_alarm2(self):
        testcase.testclass.enter(self)
        # 进入闹钟设置
        testcase.testclass.swipeUp(self)
        self.driver.find_element_by_name(u'闹钟').click()
        sleep(1)
        # 判断是否进入了闹钟页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text, '闹钟', '进入闹钟失败')


        list = self.driver.find_elements_by_id('com.inshow.watch.android:id/time')
        for j in range(list.__len__()):

            # 进入设置页面
            list[j].click()
            sleep(2)
            alarm = [Alarm.option[random.randint(0, 4)], Alarm.apm[random.randint(0, 1)], random.randint(1, 12),
                     random.randint(0, 59)]
            self.assertNotEqual(self.driver.page_source.find(u'设置闹钟'), -1, '进入添加闹钟页面失败')
            # 设置闹钟
            print "修改闹钟",j,"为", alarm[0].encode('utf-8'), alarm[1].encode('utf-8'), alarm[2], alarm[3]
            testcase.testclass.alartSetting(self, alarm[0], alarm[1], alarm[2], alarm[3])

        testcase.testclass.screenshot(self)
        # 返回主页
        testcase.testclass.pressBack(self)
        testcase. testclass.swipeDown(self)
        # 退出插件
        testcase.testclass.pressBack(self)

    #添加10个
    def test_alarm3(self):
        testcase.testclass.enter(self)
        # 进入闹钟设置
        testcase.testclass.swipeUp(self)
        self.driver.find_element_by_name(u'闹钟').click()
        sleep(1)
        # 判断是否进入了闹钟页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text, '闹钟','进入闹钟失败')

        add=10-self.driver.find_elements_by_id('com.inshow.watch.android:id/time').__len__()
        for j in range(add):
            self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
            self.driver.find_element_by_id('com.inshow.watch.android:id/select_all_select').click()

        self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
        if(self.driver.find_elements_by_id('com.inshow.watch.android:id/select_all_select')==[]):
            re = True
        else:
            re = False
        self.assertEqual(re,True,'已添加10个闹钟后，添加按钮显示错误')
        testcase.testclass.screenshot(self)
        # 返回主页
        testcase.testclass.pressBack(self)
        testcase.testclass.swipeDown(self)
        # 退出插件
        testcase.testclass.pressBack(self)



if __name__=='__main__':

    # unittest.main()
    suite=unittest.TestSuite(unittest.makeSuite(Alarm))
    # 获取当前时间，这样便于下面的使用。
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 打开一个文件，将result写入此file中
    fp = open("../report/result" + now + ".html", 'wb')
    # 执行测试

    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='test result',description=u'result:')
    runner.run(suite)
    fp.close()



