# -*- coding:utf-8 -*-
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
from time import sleep
import time

#截图
def screenshot(self):
    now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    self.driver.get_screenshot_as_file( 'screenshot/'+now +".png")
    print  'screenshot:', now, '.png'
#进入插件
def enter(self):
    #若不在主页面则重新进入app
    while self.driver.current_activity!='.SmartHomeMainActivity':
        self.driver.close_app()
        self.driver.launch_app()
        self.driver.wait_activity('.SmartHomeMainActivity', 10, 1)
    sleep(3)
    el = self.driver.find_elements_by_id('com.xiaomi.smarthome:id/name')

    #找到关键字“手表”
    for i in el:
        if i.text.find('手表')>-1:
            i.click()
            break

    sleep(2)
    u=self.driver.current_activity
    self.assertEqual(u, u'.frame.plugin.runtime.activity.PluginHostActivityMain','进入插件失败')
    city = self.driver.find_element_by_id('com.inshow.watch.android:id/tv_city')
    #等待设备连接
    while (city.get_attribute('text').find('设备连接中')> -1):
        sleep(1)
    #连接失败重试一次
    if city.get_attribute('text').find('连接失败')> -1:
        city.click()
        if city.get_attribute('text')>-1:
            self.assertEqual(0,1, '设备连接失败')
    else:
        self.assertEqual(1,1, '设备连接失败')
#添加城市
# def addcity(self,name):
#     self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
#     self.assertNotEqual(self.driver.page_source.find(u'请选择城市'), -1, '进入选择城市页面失败')
#     sleep(2)
#     self.driver.find_element_by_name(name).click()
#     sleep(2)
#     self.driver.find_element_by_id('com.inshow.watch.android:id/select_all_select').click( )

#搜索并添加联系人
def searchName(self,name):
    self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
    self.assertNotEqual(self.driver.page_source.find(u'请选择联系人'), -1, '进入选择联系人页面失败')
    sleep(2)
    self.driver.find_element_by_id('com.inshow.watch.android:id/et_search').send_keys(name.decode())
    sleep(2)
    self.driver.find_element_by_id('com.inshow.watch.android:id/tvName').click()
    sleep(2)
    self.driver.find_element_by_id('com.inshow.watch.android:id/select_all_select').click()
    sleep(2)
    self.driver.find_element_by_id('com.inshow.watch.android:id/select_all_select').click()

#搜索并添加城市
def searchCity(self,name):
    self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
    self.assertNotEqual(self.driver.page_source.find(u'请选择城市'), -1, '进入选择城市页面失败')
    sleep(2)
    self.driver.find_element_by_id('com.inshow.watch.android:id/et_search').send_keys(name.decode())
    sleep(2)
    self.driver.find_element_by_id('com.inshow.watch.android:id/tv_name').click()
    sleep(2)
    self.driver.find_element_by_id('com.inshow.watch.android:id/select_all_select').click()
    sleep(2)
    self.driver.find_element_by_id('com.inshow.watch.android:id/select_all_select').click()
#时间转化
def int2str(t):
    if t<10:
        return '0'+str(t)
    else:
        return str(t)
#设置闹钟
def alartSetting(self,repeat,apm,h,m):
    self.driver.find_element_by_name(u'重复').click()

    wer = self.driver.find_element_by_name(repeat)
    wer.click()

    # 设置备注
    # self.driver.find_element_by_id('com.inshow.watch.android:id/editText').click()
    # self.driver.find_element_by_id('com.inshow.watch.android:id/editText').send_keys(remark.decode())

    # 设置时间
    input = self.driver.find_elements_by_id('com.inshow.watch.android:id/numberpicker_input')

    # 设置上下午
    if (input[0].get_attribute('text') != apm) and input[0].get_attribute('text') == u'上午':
        swipeChoose(self, input[0], 1, 2)
    if (input[0].get_attribute('text') != apm) and input[0].get_attribute('text') == u'下午':
        swipeChoose(self, input[0], 2, 1)
    sleep(1)
    # 设置小时
    hour = int(input[1].get_attribute('text'))
    swipeChoose(self, input[1], hour, h)

    # 设置分钟
    minute = int(input[2].get_attribute('text'))
    swipeChoose(self, input[2], minute, m)


    # 点击确定
    self.driver.find_element_by_id('com.inshow.watch.android:id/select_all_select').click()
    sleep(3)
    # 判断结果
    if apm == u'下午':
        settime = int2str(h+12) + ":" + int2str(m)
    else:
        settime = int2str(h) + ":" + int2str(m)
    # a= self.driver.page_source
    # f = open("report/alarm-pagesource.txt", 'w')
    # f.write(a)
    # f.close()
    try:
        a=self.driver.find_element_by_xpath('//android.widget.TextView[@text="'+settime+'"]')
    except:
        self.assertEqual(True,False, '闹钟设置失败')
        raise AssertionError
    week = self.driver.find_element_by_xpath('//android.widget.TextView[@text="'+settime+'"]/following-sibling::android.widget.LinearLayout/android.widget.TextView[1]').text
    status = self.driver.find_element_by_id('com.inshow.watch.android:id/switchButton').get_attribute('checked')
    self.assertEqual(week, repeat, '闹钟周期错误')
    self.assertEqual(status, u'true', '闹钟状态错误')

def switchButtonOnOff(self):
    self.driver.find_element_by_id('com.inshow.watch.android:id/switchButton').click()
    sleep(2)

#switchbutton状态
def switchButtonStatus(self):
    status = self.driver.find_element_by_id('com.inshow.watch.android:id/switchButton').get_attribute('checked')
    if status==u'true':
        return True
    else:
        return False
    sleep(1)
 #手指上滑

def swipeUp(self):
    width = self.driver.get_window_size()['width']
    height = self.driver.get_window_size()['height']
    self.driver.swipe(width/2, height*5/6, width/2, height/6)
    sleep(3)

#手指下滑
def swipeDown(self):
    width = self.driver.get_window_size()['width']
    height = self.driver.get_window_size()['height']
    self.driver.swipe(width/2, height/6,width/2, height*5/6)
    sleep(3)

#滑动选择菜单
def swipeChoose(self,el,original,end):
    startX = int(el.location['x'])
    startY = int(el.location['y'])
    endX = int(el.size['width']) + startX
    endY = int(el.size['height']) + startY
    centerX = (startX + endX) / 2
    centerY = (startY + endY) / 2
    # 滑动选择轴

    if end > original:
        step = end - original
        for i in range(step):
            self.driver.swipe(centerX, endY, centerX, startY, 1000)
            sleep(1)
    else:
        step = original -end
        for i in range(step):
            self.driver.swipe(centerX, startY, centerX, endY, 1000)
            sleep(1)

#点击more，进入设置
def pressMore(self):
    self.driver.find_element_by_id('com.inshow.watch.android:id/title_bar_more').click()
    sleep(3)

#点击返回键
def pressBack(self):
    self.driver.find_element_by_id('com.inshow.watch.android:id/title_bar_return').click()
    sleep(3)
#设置返回
def settingBack(self):
    self.driver.find_element_by_id('com.xiaomi.smarthome:id/module_a_3_return_btn').click()
    sleep(3)