# -*- coding:utf-8 -*-
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
from time import sleep
import time

#截图
def screenshort(self):
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    self.driver.get_screenshot_as_file( now +".png")
#进入插件
def enter(self):
    #若不在主页面则重新进入app
    while self.driver.current_activity!='.SmartHomeMainActivity':
        self.driver.close_app()
        self.driver.launch_app()
        self.driver.wait_activity('.SmartHomeMainActivity', 10, 1)
    sleep(3)
    el = self.driver.find_elements_by_id('com.xiaomi.smarthome:id/name')
    devicesname=[u'米家石英手表',u'我的手表']

    tag=0
    for i in el:
        for j in devicesname:
            if i.text==j:
                tag=1
                i.click()
                break
        if tag==1:
            break
    sleep(2)
    u=self.driver.current_activity

    self.assertEqual(u, u'.frame.plugin.runtime.activity.PluginHostActivityMain','进入插件失败')
    city = self.driver.find_element_by_id('com.inshow.watch.android:id/tv_city')
    while (city.get_attribute('text') == u'设备连接中，请稍等...'):
        sleep(1)
    if city.get_attribute('text') == u'连接失败，点击重试？':
        city.click()
        if city.get_attribute('text') == u'连接失败，点击重试？':
            self.assertEqual(0,1, '设备连接失败')
    else:
        self.assertEqual(1,1, '设备连接失败')
#添加城市
def addcity(self,name):
    self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
    self.assertNotEqual(self.driver.page_source.find(u'请选择城市'), -1, '进入选择城市页面失败')
    sleep(2)
    self.driver.find_element_by_name(name).click()
    sleep(2)

#搜索并添加城市
def searchCity(self,name):
    self.driver.find_element_by_id('com.inshow.watch.android:id/add').click()
    self.assertNotEqual(self.driver.page_source.find(u'请选择城市'), -1, '进入选择城市页面失败')
    sleep(2)
    self.driver.find_element_by_id('com.inshow.watch.android:id/et_search').send_keys(name.decode())
    sleep(2)
    self.driver.find_element_by_id('com.inshow.watch.android:id/tv_name').click()
    sleep(2)

#switchbutton开关
def alartSetting(self,repeat,remark,apm,h,m):
    self.driver.find_element_by_name(u'重复').click()
    sleep(3)

    wer = self.driver.find_element_by_name(repeat)
    wer.click()

    sleep(3)

    # 设置备注
    self.driver.find_element_by_id('com.inshow.watch.android:id/editText').click()
    self.driver.find_element_by_id('com.inshow.watch.android:id/editText').send_keys(remark.decode())

    # 设置时间
    input = self.driver.find_elements_by_id('com.inshow.watch.android:id/numberpicker_input')
    sleep(1)
    # 设置上下午
    if (input[0].get_attribute('text') != apm) and input[0].get_attribute('text') == u'上午':
        swipeChoose(self, input[0], 1, 2)
    if (input[0].get_attribute('text') != apm) and input[0].get_attribute('text') == u'下午':
        swipeChoose(self, input[0], 2, 1)
    sleep(1)
    # 设置小时
    hour = int(input[1].get_attribute('text'))
    swipeChoose(self, input[1], hour, h)
    sleep(1)
    # 设置分钟
    minute = int(input[2].get_attribute('text'))
    swipeChoose(self, input[2], minute, m)
    sleep(1)

    # 点击确定
    self.driver.find_element_by_id('com.inshow.watch.android:id/select_all_select').click()
    sleep(2)

    # 判断结果
    if apm == u'下午':
        settime = str(h + 12) + ":" + str(m)
    else:
        settime = '0' + str(h) + ":" + str(m)
    time = self.driver.find_elements_by_id('com.inshow.watch.android:id/time')[0].text
    week = self.driver.find_elements_by_id('com.inshow.watch.android:id/weekNum')[0].text
    status = self.driver.find_elements_by_id('com.inshow.watch.android:id/timeLeft')[0].text
    self.assertEqual(time, settime, '闹钟时间错误')
    self.assertEqual(week, repeat, '闹钟周期错误')
    self.assertEqual(status, u'已开启', '闹钟状态错误')

def switchButtonOnOff(self):
    self.driver.find_element_by_id('com.inshow.watch.android:id/switchButton').click()
    sleep(3)

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