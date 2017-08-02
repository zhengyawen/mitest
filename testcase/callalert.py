# -*- coding:utf-8 -*-

import unittest
from appium import webdriver
from time import sleep
import testcase.testclass
import random
import HTMLTestRunner
class Callalert(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('start setup')
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.0'
        desired_caps['deviceName'] = 'b3ce25b8'
        desired_caps['appPackage'] = 'com.xiaomi.smarthome'
        desired_caps['appActivity'] = '.SmartHomeMainActivity'
        desired_caps['newCommandTimeout'] = '300'
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True

        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print('tearDown')

    #添加来电提醒
    def test_call1(self):
        print "添加来电提醒"
        testcase.testclass.enter(self)
        testcase.testclass.swipeUp(self)
        self.driver.find_element_by_name('来电提醒').click()
        # 判断是否进入了来电提醒页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text, '来电提醒', '进入来电提醒失败')
        # 进入添加世界时间页面
        self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
        self.assertNotEqual(self.driver.page_source.find(u'请选择联系人'), -1, '进入选择联系人页面失败')
        # 获取来电提醒列表
        tv = self.driver.find_elements_by_id('com.inshow.watch.android:id/tvName')

        contact = []
        for i in tv:
            contact.append(i.text.encode('utf-8'))
        print '联系人列表为', contact
        key = contact[random.randint(0, tv.__len__() - 1)]
        print '联系人设置为', key
        self.driver.find_element_by_name(key).click()
        self.driver.find_element_by_id('com.inshow.watch.android:id/select_all_select').click()

        # 判断结果
        self.assertEqual(
            self.driver.find_element_by_id('com.inshow.watch.android:id/title_bar_title').text, '来电提醒', '返回来电提醒失败')
        if (self.driver.page_source.find(key) > -1):
            result = True
        else:
            result = False
        self.assertEqual(result, True, '添加来电提醒失败')
        # 返回主页
        testcase.testclass.pressBack(self)
        # 退出插件
        testcase.testclass.pressBack(self)

        # 搜索添加联系人
    def test_call2(self):
            testcase.testclass.enter(self)
            testcase.testclass.swipeUp(self)
            self.driver.find_element_by_name(u'来电提醒').click()
            # 判断是否进入了来电提醒页面
            self.assertEqual(self.driver.find_element_by_id(
                'com.inshow.watch.android:id/title_bar_title').text, '来电提醒', '进入来电提醒失败')
            keys = ['d']  # 列表中所有想添加的联系人名

            for key in keys:
                testcase.testclass.searchName(self, key)
                print '添加联系人为', key
            # 判断结果
            result = True
            for key in keys:
                result = result and (self.driver.page_source.find(key) != -1)
            self.assertEqual(True, result, '添加失败')
            # 返回主页
            testcase.testclass.pressBack(self)
            # 退出插件
            testcase.testclass.pressBack(self)

            # 搜索添加城市

