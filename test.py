# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random

import re
timenow=u'每隔20分钟时间，手表将震动提醒'
x = re.sub("\D", "", timenow)

for i in range(10):
    print (u'男',u'女')[random.randint(0,1)]