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

class Dtest(unittest.TestCase):
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
        testclass.enter(self)
        #退出插件
        testclass.pressBack(self)


    #滑动查看城市
    @unittest.skip('skip')
    def test_citySlide(self):
        testclass.enter(self)
        result=True
        testclass.swipeUp(self)
        self.driver.find_element_by_name('世界时间').click()
        #判断是否进入了世界时间页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text,'世界时间','进入世界时间失败')
        citys=self.driver.find_elements_by_class_name('android.widget.LinearLayout')
        length=len(citys)

        # 返回主页
        sleep(3)
        testclass.pressBack(self)
        testclass.swipeDown(self)

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
        testclass.pressBack(self)

    # 添加首页城市
    def test_cityTime(self):
        testclass.enter(self)
        testclass.swipeUp(self)
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
        testclass.pressBack(self)
        # 退出插件
        testclass.pressBack(self)

    # 搜索添加城市
    def test_citySearch(self):
        testclass.enter(self)
        testclass.swipeUp(self)
        self.driver.find_element_by_name(u'世界时间').click()
        # 判断是否进入了世界时间页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text, '世界时间','进入世界时间失败')
        keys=['巴林','巴拿马']#列表中所有想添加的城市名

        for key in keys:
            testclass.searchCity(self, key)
            print '添加城市为',key
        #判断结果
        result = True
        for key in keys:
            result = result and (self.driver.page_source.find(key) != -1)
        self.assertEqual(True,result, '添加失败')
        #返回主页
        testclass.pressBack(self)
        # 退出插件
        testclass.pressBack(self)

    # @unittest.skip('skip')
    #时间间隔反复开关
    def test_intervalOnOff(self):
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
    def test_setIterval(self):
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


     # @unittest.skip(u'忽略该挑用例')
    #添加闹钟
    option = [u'只响一次', u'每天', u'法定工作日', u'法定节假日', u'周一至周五']
    apm=[u'上午',u'下午']
    def test_addAlarm(self):
        testclass.enter(self)
        # 进入闹钟设置
        testclass.swipeUp(self)
        self.driver.find_element_by_name(u'闹钟').click()
        sleep(1)
        # 判断是否进入了闹钟页面
        self.assertEqual(self.driver.find_element_by_id('com.inshow.watch.android:id/title_bar_title').text, '闹钟',
                         '进入闹钟失败')

        #定义闹钟格式
        alarm=[
            [Dtest.option[random.randint(0,4)],Dtest.apm[random.randint(0,1)],random.randint(1,12),random.randint(0,59)],
            # [Dtest.option[1],u'上午',4,30]
        ]
        for i in alarm:
            # 进入添加页面
            self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
            sleep(2)
            self.assertNotEqual(self.driver.page_source.find(u'设置闹钟'), -1, '进入添加闹钟页面失败')
            #设置闹钟
            print "设置闹钟", i[0].encode('utf-8'), i[1].encode('utf-8'), i[2], i[3]
            testclass.alartSetting(self, i[0], i[1], i[2], i[3])

        # 返回主页
        testclass.pressBack(self)

        # 退出插件
        testclass.pressBack(self)

    #修改闹钟
    def test_alterAlarm(self):
        testclass.enter(self)
        # 进入闹钟设置
        testclass.swipeUp(self)
        self.driver.find_element_by_name(u'闹钟').click()
        sleep(1)
        # 判断是否进入了闹钟页面
        self.assertEqual(self.driver.find_element_by_id(
            'com.inshow.watch.android:id/title_bar_title').text, '闹钟','进入闹钟失败')

        # 定义闹钟格式
        alarm = [
            [Dtest.option[random.randint(0, 4)], Dtest.apm[random.randint(0, 1)], random.randint(1, 12),random.randint(0, 59)],
            # [Dtest.option[1], u'上午', 4, 30]
        ]

        list=self.driver.find_elements_by_id('com.inshow.watch.android:id/time')
        for i in range(len(alarm)):
            # 进入设置页面
            list[i].click()
            sleep(2)
            self.assertNotEqual(self.driver.page_source.find(u'设置闹钟'), -1, '进入添加闹钟页面失败')
            # 设置闹钟
            print "设置闹钟", alarm[i][0].encode('utf-8'), alarm[i][1].encode('utf-8'), alarm[i][2], alarm[i][3]
            testclass.alartSetting(self,alarm[i][0],alarm[i][1],alarm[i][2],alarm[i][3])



        # 返回主页
        testclass.pressBack(self)
        testclass.swipeDown(self)
        # 退出插件
        testclass.pressBack(self)

    # @unittest.skip(u'忽略该挑用例')
    # 进入设置
    def test_more(self):
        #进入设置
        testclass.enter(self)
        testclass.pressMore(self)
        #退出设置
        testclass.settingBack(self)
        # 退出插件
        testclass.pressBack(self)

    # 设置身体信息
    def test_setBodyInfo(self):
        # 进入设置
        testclass.enter(self)
        testclass.pressMore(self)
        #进入身体信息
        self.driver.find_element_by_name(u'身体信息').click()
        # 判断是否进入了身体信息页面
        self.assertEqual(self.driver.find_element_by_id('com.inshow.watch.android:id/title_bar_title').text, '身体信息',
                         '进入身体信息失败')
        sleep(1)
        #设定修改值
        dataset=[random.randint(1917,2016),random.randint(1,12),(u'男',u'女')[random.randint(0,1)],random.randint(120,220),random.randint(50,150)]
        print '设置为：%d年%d月,性别:%s,身高%d,体重%d'%(dataset[0],dataset[1],dataset[2],dataset[3],dataset[4])
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
        testclass.swipeChoose(self,yearpicker,int(yearpicker.text),dataset[0])
        testclass.swipeChoose(self, mompicker, int(mompicker.text), dataset[1])
        self.driver.find_element_by_name('确定').click()
        #设置性别
        self.driver.find_element_by_name('性别').click()
        self.driver.find_element_by_name(dataset[2]).click()
        #设置身高
        self.driver.find_element_by_name('身高').click()
        heigpicker=self.driver.find_element_by_id('com.inshow.watch.android:id/numberpicker_input')
        testclass.swipeChoose(self, heigpicker,int(heigpicker.text), dataset[3])
        self.driver.find_element_by_name('确定').click()
        #设置体重
        self.driver.find_element_by_name('体重').click()
        weigpicker = self.driver.find_element_by_id('com.inshow.watch.android:id/numberpicker_input')
        testclass.swipeChoose(self, weigpicker, int(weigpicker.text), dataset[4])
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

        self.assertEqual(yeardata,testclass.int2str(dataset[0])+'年'+testclass.int2str(dataset[1])+'月','出生年月设置失败')
        self.assertEqual(sexdata,dataset[2],'性别设置失败')
        self.assertEqual(heigdata,testclass.int2str(dataset[3])+'厘米','身高设置失败')
        self.assertEqual(weigdata,testclass.int2str(dataset[4])+'公斤','体重设置失败')
        # 退出设置
        testclass.settingBack(self)
        # 退出插件
        testclass.pressBack(self)


    #进入设备信息修改设备名称
    def test_setDeviceInfo(self):
        # 进入设置
        testclass.enter(self)
        testclass.pressMore(self)
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
        self.assertEqual(self.driver.find_element_by_id('com.xiaomi.smarthome:id/name').text,key,'修改设备名称失败')

        # 退出设置
        testclass.settingBack(self)
        # 退出插件
        testclass.pressBack(self)


if __name__=='__main__':

    # unittest.main()
    suite=unittest.TestSuite(unittest.makeSuite(Dtest))
    # 获取当前时间，这样便于下面的使用。
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 打开一个文件，将result写入此file中
    fp = open("../report/result" + now + ".html", 'wb')
    # 执行测试

    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='test result',description=u'result:')
    runner.run(suite)
    fp.close()



