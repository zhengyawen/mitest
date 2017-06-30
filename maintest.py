# -*- coding:utf-8 -*-

from appium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
print('start setup')
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '5.0'
desired_caps['deviceName'] = 'b3ce25b8'
desired_caps['appPackage'] = 'com.xiaomi.smarthome'
desired_caps['appActivity'] = '.SmartHomeMainActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
sleep(3)

driver.find_element_by_name(u'米家手表').click()
sleep(3)

driver.swipe(350,1200,350,200)
sleep(3)
print u'上滑成功'

status= driver.find_element_by_id('com.inshow.watch.android:id/switchButton').is_selected()
print 'status',status

driver.quit()


