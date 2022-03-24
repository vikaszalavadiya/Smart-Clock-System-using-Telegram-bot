#!/usr/bin/python
# Prachi Enterprice
# Clock System (12-9-2020)
# Developd by Vikas Zalavadiya

import sys
import time
from RTC_DS1307 import RTC
import datetime

# Manually Set Time and Date
rtc = RTC()
rtc.setDate(seconds = 0, minutes = 46, hours = 3, dow = 2, day = 12, month = 9, year = 20)
print ("Date set to:", rtc.getDateStr())
