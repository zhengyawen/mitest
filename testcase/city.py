# -*- coding:utf-8 -*-
import unittest
from appium import webdriver
from time import sleep
import testcase.testclass
import HTMLTestRunner
import re
import selenium
import random
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class City(unittest.TestCase):
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

    # 进入插件
    def test_enter(self):
        testcase.testclass.enter(self)
        #退出插件
        testcase.testclass.pressBack(self)


    #滑动查看城市
    # @unittest.skip('skip')
    def test_city1(self):
        testcase.testclass.enter(self)
        result=True
        testcase.testclass.swipeUp(self)
        self.driver.find_element_by_name('世界时间').click()
        #判断是否进入了世界时间页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text,'世界时间','进入世界时间失败')
        citys=self.driver.find_elements_by_class_name('android.widget.LinearLayout')
        length=len(citys)

        # 返回主页
        sleep(3)
        testcase.testclass.pressBack(self)
        testcase.testclass.swipeDown(self)

        #滑动城市
        if length ==1:
            result==True
        else:
            for i in range(length):
                el=self.driver.find_element_by_id('com.inshow.watch.android:id/tv_city')
                old=el.get_attribute('text')
                self.driver.swipe(700, 900, 300, 900)
                sleep(1)
                el = self.driver.find_element_by_id('com.inshow.watch.android:id/tv_city')
                new = el.get_attribute('text')
                result=result and (old !=new)
        self.assertEqual(result,True, '滑动世界城市失败')
        # 退出插件
        testcase.testclass.pressBack(self)

    # 添加首页城市
    def test_city2(self):
        testcase.testclass.enter(self)
        testcase.testclass.swipeUp(self)
        self.driver.find_element_by_name('世界时间').click()
        # 判断是否进入了世界时间页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text, '世界时间','进入世界时间失败')
        #进入添加世界时间页面
        self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
        self.assertNotEqual(self.driver.page_source.find(u'请选择城市'), -1, '进入选择城市页面失败')
        #获取城市列表
        tv=self.driver.find_elements_by_id('com.inshow.watch.android:id/tv_name')

        city=[]
        for i in tv:
            city.append(i.text.encode('utf-8'))
        print '城市列表为',city
        key=city[random.randint(0,tv.__len__()-1)]
        print '世界城市设置为',key
        self.driver.find_element_by_name(key).click()
        self.driver.find_element_by_id('com.inshow.watch.android:id/select_all_select').click()

        #判断结果
        self.assertEqual(
            self.driver.find_element_by_id('com.inshow.watch.android:id/title_bar_title').text, '世界时间','返回世界时间失败')
        if(self.driver.page_source.find(key)>-1):
            result=True
        else:
            result=False
        self.assertEqual(result,True, '添加世界城市失败')
        # 返回主页
        sleep(3)
        testcase.testclass.pressBack(self)
        # 退出插件
        testcase.testclass.pressBack(self)

    # 搜索添加城市
    def test_city3(self):
        testcase.testclass.enter(self)
        testcase.testclass.swipeUp(self)
        self.driver.find_element_by_name(u'世界时间').click()
        # 判断是否进入了世界时间页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text, '世界时间','进入世界时间失败')
        keys=['巴林','巴拿马']#列表中所有想添加的城市名

        for key in keys:
            testcase.testclass.searchCity(self, key)
            print '添加城市为',key
        #判断结果
        result = True
        for key in keys:
            result = result and (self.driver.page_source.find(key) != -1)
        self.assertEqual(True,result, '添加失败')
        #返回主页
        testcase.testclass.pressBack(self)
        # 退出插件
        testcase.testclass.pressBack(self)


if __name__=='__main__':

    # unittest.main()
    suite=unittest.TestSuite(unittest.makeSuite(City))
    # 获取当前时间，这样便于下面的使用。
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 打开一个文件，将result写入此file中
    fp = open("../report/result" + now + ".html", 'wb')
    # 执行测试

    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='test result',description=u'result:')
    runner.run(suite)
    fp.close()



