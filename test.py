# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
timenow=u'每隔20分钟时间，手表将震动提醒'
x = re.sub("\D", "", timenow)
print x