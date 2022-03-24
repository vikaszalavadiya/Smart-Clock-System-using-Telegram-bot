# RTC_DS1307.py
# Code inspired from GitHub: sorz/DS1307.py
import os
import sys
import time
import smbus
from time import sleep
import threading
import glob
import logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename='/home/pi/clock_system/exceptiondata.txt')
def bcdToInt(bcd):
    try:        
        '''
        Converts byte interpreted as two digit bcd to integer
        (e.g. 88 = b01011000->bcd0101'1000 = 58)
        '''
        out = 0
        for d in (bcd >> 4, bcd):
            for p in (1, 2, 4 ,8):
                if d & 1:
                    out += p
                d >>= 1
            out *= 10
        return out // 10
    except Exception as e:
        print(e)
        exec_info = sys.exc_info()
        logging.exception("CZIOT logging starts")
        logging.exception(e)
        logging.exception("CZIOT logging ends")
        return 0

def intToBcd(n):
    try:
        
        '''
        Converts integer 0..99 to byte interpreted in two digit bcd format.
        (e.g. 58 = bcd0101'1000->b01011000 = 88)
        '''
        bcd = 0
        for i in (n // 10, n % 10):
            for p in (8, 4, 2, 1):
                if i >= p:
                    bcd += 1
                    i -= p
                bcd <<= 1
        return bcd >> 1
    except Exception as e:
        print(e)
        exec_info = sys.exc_info()
        logging.exception("CZIOT logging starts")
        logging.exception(e)
        logging.exception("CZIOT logging ends")
        return 0

class RTC():
    _REG_SECONDS = 0x00
    _REG_MINUTES = 0x01
    _REG_HOURS = 0x02
    _REG_DOW = 0x03
    _REG_DAY = 0x04
    _REG_MONTH = 0x05
    _REG_YEAR = 0x06
    _REG_CONTROL = 0x07

    def __init__(self, type = 1, addr = 0x68):
        try:
            
            '''
            Creates a Real Time Clock abstraction using given SMBus type and I2C address
            @param type: 0 for RPi model A, 1 for higher versions (default: 1)
            @param addr: I2C address (default: 0x68)
            '''
            self._bus = smbus.SMBus(type)
            self._addr = addr
            time.sleep(2)
            
        except Exception as e:
            print(e)
            exec_info = sys.exc_info()
            logging.exception("CZIOT logging starts")
            logging.exception(e)
            logging.exception("CZIOT logging ends")
            

    def _write(self, register, data):
        try:
            self._bus.write_byte_data(self._addr, register, data)
            
        except Exception as e:
            print(e)
            exec_info = sys.exc_info()
            logging.exception("CZIOT logging starts")
            logging.exception(e)
            logging.exception("CZIOT logging ends")

    def _read(self, data):
        try:
            returndata = self._bus.read_byte_data(self._addr, data)
            return returndata
        
        except Exception as e:
            print(e)
            exec_info = sys.exc_info()
            logging.exception("CZIOT logging starts")
            logging.exception(e)
            logging.exception("CZIOT logging ends")
            return None

    def getSeconds(self):
        try:
            
            '''
            Returns current seconds.
            @return: seconds of current date/time (0..59)
            '''
            return bcdToInt(self._read(self._REG_SECONDS))
        
        except Exception as e:
            print(e)
            exec_info = sys.exc_info()
            logging.exception("CZIOT logging starts")
            logging.exception(e)
            logging.exception("CZIOT logging ends")
            return 0

    def getMinutes(self):
        '''
        Returns current minutes.
        @return: minutes of current date/time (0..59)
        '''
        return bcdToInt(self._read(self._REG_MINUTES))

    def getHours(self):
        '''
        Returns current hours.
        @return: hours of current date/time (0..23)
        '''
        d = self._read(self._REG_HOURS)
        if (d == 0x64):
            d = 0x40
        return bcdToInt(d & 0x3F)

    def getDow(self):
        '''
        Returns current day of week.
        @return: day number of current date/time (1..7, 1 for Monday)
        '''
        return bcdToInt(self._read(self._REG_DOW))

    def getDay(self):
        '''
        Returns current day of month.
        @return: day of current date/time (1..31)
        '''
        return bcdToInt(self._read(self._REG_DAY))

    def getMonth(self):
        '''
        Returns current month.
        @return: month of current date/time (1..12)
        '''
        return bcdToInt(self._read(self._REG_MONTH))

    def getYear(self):
        '''
        Returns current year.
        @return: year of current date/time (0..99)
        '''
        return bcdToInt(self._read(self._REG_YEAR))

    def setDate(self, seconds = None, minutes = None, hours = None, dow = None,
            day = None, month = None, year = None):
        '''
        Sets the current date/time.
        Range: seconds [0,59], minutes [0,59], hours [0,23],
               day_of_week [1,7], day [1-31], month [1-12], year [0-99].
        If a parameter is None (default), the current value is unchanged
        '''
        if seconds is not None:
            if seconds < 0 or seconds > 59:
                raise ValueError('Seconds is out of range [0,59].')
            self._write(self._REG_SECONDS, intToBcd(seconds))

        if minutes is not None:
            if minutes < 0 or minutes > 59:
                raise ValueError('Minutes is out of range [0,59].')
            self._write(self._REG_MINUTES, intToBcd(minutes))

        if hours is not None:
            if hours < 0 or hours > 23:
                raise ValueError('Hours is out of range [0,23].')
            self._write(self._REG_HOURS, intToBcd(hours))

        if year is not None:
            if year < 0 or year > 99:
                raise ValueError('Years is out of range [0,99].')
            self._write(self._REG_YEAR, intToBcd(year))

        if month is not None:
            if month < 1 or month > 12:
                raise ValueError('Month is out of range [1,12].')
            self._write(self._REG_MONTH, intToBcd(month))

        if day is not None:
            if day < 1 or day > 31:
                raise ValueError('Day is out of range [1,31].')
            self._write(self._REG_DAY, intToBcd(day))

        if dow is not None:
            if dow < 1 or dow > 7:
                raise ValueError('Day Of Week is out of range [1,7].')
            self._write(self._REG_DOW, intToBcd(dow))

    def getDate(self):
        '''
        Returns the current date/time.
        @return: date/time in a tuple with order
        (year, month, day, dow, hours, minutes, seconds)
        '''
        return (self.getYear(), self.getMonth(), self.getDay(),
                self.getDow(), self.getHours(), self.getMinutes(),
                self.getSeconds())

    def getDateStr(self):
        '''
        Returns the current date/time.
        @return: date/time in a string with format
        year-month-day hours:minutes:seconds
        '''
        return "20%02d-%02d-%02d %02d:%02d:%02d" %(self.getYear(), self.getMonth(), self.getDay(), self.getHours(), self.getMinutes(), self.getSeconds())
###################  Edit By Vikas  ####################################################################
    def setTime(self, seconds = None, minutes = None, hours = None):
        '''
        Sets the current date/time.
        Range: seconds [0,59], minutes [0,59], hours [0,23],
               day_of_week [1,7], day [1-31], month [1-12], year [0-99].
        If a parameter is None (default), the current value is unchanged
        '''
        if seconds is not None:
            if seconds < 0 or seconds > 59:
                raise ValueError('Seconds is out of range [0,59].')
            self._write(self._REG_SECONDS, intToBcd(seconds))

        if minutes is not None:
            if minutes < 0 or minutes > 59:
                raise ValueError('Minutes is out of range [0,59].')
            self._write(self._REG_MINUTES, intToBcd(minutes))

        if hours is not None:
            if hours < 0 or hours > 23:
                raise ValueError('Hours is out of range [0,23].')
            self._write(self._REG_HOURS, intToBcd(hours))

            
    def getTimeStr(self):
        try:
            return "%02d:%02d:%02d" %(self.getHours(), self.getMinutes(), self.getSeconds())
        
        except Exception as e:
            print(e)
            exec_info = sys.exc_info()
            logging.exception("CZIOT logging starts")
            logging.exception(e)
            logging.exception("CZIOT logging ends")
            return 0

