# -*- coding:utf-8 -*-
import unittest
from appium import webdriver
from time import sleep
import testcase.testclass
import HTMLTestRunner
import re
from selenium.webdriver.support.ui import WebDriverWait
import random
import time


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Setting(unittest.TestCase):
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




    # 设置身体信息
    def test_set1(self):
        # 进入设置
        print "设置身体信息"
        testcase.testclass.enter(self)
        testcase.testclass.pressMore(self)
        #进入身体信息
        self.driver.find_element_by_name(u'身体信息').click()
        # 判断是否进入了身体信息页面
        self.assertEqual(self.driver.find_element_by_id('com.inshow.watch.android:id/title_bar_title').text, '身体信息',
                         '进入身体信息失败')
        sleep(1)
        #设定修改值
        dataset=[random.randint(1917,2016),random.randint(1,12),(u'男',u'女')[random.randint(0,1)],random.randint(120,220),random.randint(50,150)]
        print '设置为：%d年%d月,性别:%s,身高%d,体重%d'%(dataset[0],dataset[1],dataset[2].encode('utf-8'),dataset[3],dataset[4])
        #设置出生年月
        self.driver.find_element_by_name('出生年月').click()
        # a=self.driver.page_source
        # f=open("report/birthdata-pagesouece.txt",'w')
        # f.write(a)
        # f.close()
        yearpicker=self.driver.find_element_by_xpath(
            '//android.widget.TextView[@text="出生年月"]/../../following-sibling::android.widget.FrameLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.LinearLayout/com.inshow.watch.android.view.WatchNumberPicker[1]/android.widget.EditText')
        mompicker=self.driver.find_element_by_xpath(
             '//android.widget.TextView[@text="出生年月"]/../../following-sibling::android.widget.FrameLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.LinearLayout/com.inshow.watch.android.view.WatchNumberPicker[2]/android.widget.EditText')
        testcase.testclass.swipeChoose(self, yearpicker, int(yearpicker.text), dataset[0])
        testcase.testclass.swipeChoose(self, mompicker, int(mompicker.text), dataset[1])
        self.driver.find_element_by_name('确定').click()
        #设置性别
        self.driver.find_element_by_name('性别').click()
        self.driver.find_element_by_name(dataset[2]).click()
        #设置身高
        self.driver.find_element_by_name('身高').click()
        heigpicker=self.driver.find_element_by_id('com.inshow.watch.android:id/numberpicker_input')
        testcase.testclass.swipeChoose(self, heigpicker, int(heigpicker.text), dataset[3])
        self.driver.find_element_by_name('确定').click()
        #设置体重
        self.driver.find_element_by_name('体重').click()
        weigpicker = self.driver.find_element_by_id('com.inshow.watch.android:id/numberpicker_input')
        testcase.testclass.swipeChoose(self, weigpicker, int(weigpicker.text), dataset[4])
        self.driver.find_element_by_name('确定').click()

        #判断设置结果
        yeardata=self.driver.find_element_by_xpath(
            '//android.widget.TextView[@text="出生年月"]/following-sibling::android.widget.TextView[1]').text
        sexdata=self.driver.find_element_by_xpath(
            '//android.widget.TextView[@text="性别"]/following-sibling::android.widget.TextView[1]').text
        heigdata = self.driver.find_element_by_xpath(
            '//android.widget.TextView[@text="身高"]/following-sibling::android.widget.TextView[1]').text
        weigdata = self.driver.find_element_by_xpath(
            '//android.widget.TextView[@text="体重"]/following-sibling::android.widget.TextView[1]').text

        self.assertEqual(yeardata,'%d年%d月'%(dataset[0],dataset[1]),'出生年月设置失败')
        self.assertEqual(sexdata,dataset[2],'性别设置失败')
        self.assertEqual(heigdata, testcase.testclass.int2str(dataset[3]) + '厘米', '身高设置失败')
        self.assertEqual(weigdata, testcase.testclass.int2str(dataset[4]) + '公斤', '体重设置失败')

        testcase.testclass.pressBack(self)
        # 退出设置
        testcase.testclass.settingBack(self)
        # 退出插件
        testcase.testclass.pressBack(self)


    #进入设备信息修改设备名称
    def test_set2(self):
        print "重命名"
        # 进入设置
        testcase.testclass.enter(self)
        testcase.testclass.pressMore(self)
        # 进入身体信息

        list=self.driver.find_element_by_id('com.xiaomi.smarthome:id/name')
        #修改名称
        devicesname = ['米家石英手表', '我的手表','手表啊','小手表','米家手表']
        key=devicesname[random.randint(0,4)]
        print '设置手表名为',key.encode('utf-8')
        self.driver.find_element_by_name(u'重命名').click()
        # a= self.driver.page_source
        # f = open("report/alarm-pagesource.txt", 'w')
        # f.write(a)
        # f.close()
        self.driver.find_element_by_id('com.xiaomi.smarthome:id/client_remark_input_view_edit').send_keys(key.decode())
        self.driver.find_element_by_name(u'确定').click()
        sleep(1)
        #判断是否修改成功
        namenow=self.driver.find_element_by_xpath(
            '//android.widget.TextView[@text="重命名"]/following-sibling::android.widget.TextView[1]').text
        self.assertEqual(namenow,key,'修改设备名称失败')

        # 退出设置
        testcase.testclass.settingBack(self)
        # 退出插件
        testcase.testclass.pressBack(self)

    def test_set3(self):
        print "查看步数"
        # 进入设置
        testcase.testclass.enter(self)
        counter=self.driver.find_element_by_id('com.inshow.watch.android:id/stepCounter')
        step=re.sub(r'\D','',counter.text)
        counter.click()
        sleep(3)
        tvstep=self.driver.find_element_by_id('com.inshow.watch.android:id/tv_step')
        steptext=re.sub(r'\D','',tvstep.text)
        self.assertEqual(step,steptext,'步数数据有误')
        testcase.testclass.pressBack(self)
        testcase.testclass.pressBack(self)

    def test_set4(self):
        print "查看步数周视图"
        # 进入设置
        testcase.testclass.enter(self)
        counter=self.driver.find_element_by_id('com.inshow.watch.android:id/stepCounter')
        counter.click()
        sleep(3)
        self.driver.find_element_by_name('周').click()
        sleep(3)
        testcase.testclass.screenshot(self)
        testcase.testclass.pressBack(self)
        testcase.testclass.pressBack(self)

    def test_set5(self):
        print "查看步数月视图"
        # 进入设置
        testcase.testclass.enter(self)
        counter=self.driver.find_element_by_id('com.inshow.watch.android:id/stepCounter')
        counter.click()
        sleep(3)
        self.driver.find_element_by_name('月').click()
        sleep(3)
        testcase.testclass.screenshot(self)
        testcase.testclass.pressBack(self)
        testcase.testclass.pressBack(self)

if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(Setting('test_set4'))



    # suite=unittest.TestSuite(unittest.makeSuite(Setting))
    # 获取当前时间，这样便于下面的使用。
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 打开一个文件，将result写入此file中
    fp = open("../report/result" + now + ".html", 'wb')
    # 执行测试

    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='test result',description=u'result:')
    runner.run(suite)
    fp.close()



