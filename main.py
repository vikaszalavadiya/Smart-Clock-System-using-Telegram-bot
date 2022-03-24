#!/usr/bin/python
#Developd by Vikas Zalavadiya
# Prachi Enterprice - Clock System (Version 2.0) (17-12-2020)
#display on lcd(time & moter ON time in sec)
#Relay operate every one min (its seperate thread)
#relay operate time read & write from txt file.
#set time & Moter on time using lcd menu display
#use 3 button from set config. 1-setting btn,2-up btn, 3-down btn

import os
import sys
import time
import threading
import glob
import logging
from RTC_DS1307 import RTC
import RPi.GPIO as GPIO
from RPLCD import CharLCD

    
def display():
    try:
        print("Prachi Enterprise")
        print(" ")
        print("Clock System (Version 2.0)")
        lcd.clear()
        lcd.cursor_pos = (0,5)
        lcd.write_string("PRACHI")
        lcd.cursor_pos = (1,3)
        lcd.write_string("ENTERPRISE")
        time.sleep (2)
        lcd.clear()
        lcd.cursor_pos = (0,0)
        lcd.write_string("CLOCK SYSTEM v.2")
        lcd.cursor_pos = (1,0)
        for i in range(16):
            v11 = "."
            lcd.write_string(v11)
            time.sleep (0.2)        
        lcd.clear()
        
    except Exception as e:
        print(e)
        exec_info = sys.exc_info()
        logging.exception("CZIOT logging starts")
        logging.exception(e)
        logging.exception("CZIOT logging ends")
        GPIO.output(errorpin, GPIO.HIGH)
        return 0
        
    

def initpinfunc(): #Initialization func
    try:  
        global lcd
        global rtc
        global relaypin, errorpin, blinkpin
        global relayon
        global setpin, uppin, downpin
        relaypin = 7
        setpin = 8
        uppin = 10
        downpin = 12
        blinkpin = 16
        errorpin = 18
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(setpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(setpin, GPIO.FALLING, callback = controllfunc,bouncetime = 300)
        GPIO.setup(uppin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(uppin, GPIO.FALLING, callback = upfunc,bouncetime = 300)
        GPIO.setup(downpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(downpin, GPIO.FALLING, callback = downfunc,bouncetime = 300)
        GPIO.setup(relaypin, GPIO.OUT)
        GPIO.output(relaypin, GPIO.HIGH)
        GPIO.setup(errorpin, GPIO.OUT)
        GPIO.output(errorpin, GPIO.LOW)
        GPIO.setup(blinkpin, GPIO.OUT)
        GPIO.output(blinkpin, GPIO.LOW)
        
        lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23],numbering_mode=GPIO.BOARD)
        
        os.system("sudo rmmod rtc-ds1307") # Clear busy I2C Address
        time.sleep(0.5)
        rtc = RTC()
        time.sleep(0.5)
        display()

        
    except Exception as e:
        print(e)
        exec_info = sys.exc_info()
        logging.exception("CZIOT logging starts")
        logging.exception(e)
        logging.exception("CZIOT logging ends")
        GPIO.output(errorpin, GPIO.HIGH)
        return 0

def readtextfile():
    try:
        global relayonval1
        fo = open("/home/pi/clock_system/Relay_Time.txt","r")
        ln = fo.readlines()
        fo.close()
        tempval1 = str(ln)
        relayonval1 = tempval1[2:6]
        relayonval1 = float(relayonval1)
        relayonval1 = round(relayonval1,2)
        print("Read from txt file: ",relayonval1)
    
    except Exception as e:
        relayonval1 = 1.00
        print(e)
        exec_info = sys.exc_info()
        logging.exception("CZIOT logging starts")
        logging.exception(e)
        logging.exception("CZIOT logging ends")
        GPIO.output(errorpin, GPIO.HIGH)
        return 0
    
    
def writetextfile():
    try:
        global relayonval1
        fo = open("/home/pi/clock_system/Relay_Time.txt","w")
        fo.write(str(relayonval1))
        fo.close()
    except Exception as e:
        print(e)
        exec_info = sys.exc_info()
        logging.exception("CZIOT logging starts")
        logging.exception(e)
        logging.exception("CZIOT logging ends")
        GPIO.output(errorpin, GPIO.HIGH)
        return 0
    
    

class runled(threading.Thread): # LCD Display Thread
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            global relaypin, errorpin, blinkpin
            while True:
                GPIO.output(blinkpin, GPIO.HIGH)
                time.sleep(3)
                GPIO.output(blinkpin, GPIO.LOW)
                time.sleep(1)
            
        except Exception as e:
            print(e)
            exec_info = sys.exc_info()
            logging.exception("CZIOT logging starts")
            logging.exception(e)
            logging.exception("CZIOT logging ends")
            GPIO.output(errorpin, GPIO.HIGH)
            return 0
    
    

class runlcd(threading.Thread): # LCD Display Thread
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:            
            global relayonval1
            global auto_mode
            while True:
                if(auto_mode == True):
                    time1 = rtc.getTimeStr()
                    if (time1 == int(0)):
                        time1 =   "Error 121"
                    print ("Time:",time1)
                    lcd.clear()
                    lcd.cursor_pos = (0,0)
                    lcd.write_string("Time:")
                    lcd.cursor_pos = (0,5)
                    lcd.write_string(str(time1))
                    lcd.cursor_pos = (1,0)
                    lcd.write_string("M.on:")
                    lcd.cursor_pos = (1,5)
                    lcd.write_string("%.2f" %(relayonval1)+ " sec")
                time.sleep(1)
        except Exception as e:
            print(e)
            exec_info = sys.exc_info()
            logging.exception("CZIOT logging starts")
            logging.exception(e)
            logging.exception("CZIOT logging ends")
            GPIO.output(errorpin, GPIO.HIGH)
            return 0
            
def checkrelaypin():
    GPIO.output(relaypin, GPIO.HIGH)
    while(GPIO.input(relaypin) == 0):
        print("relay pin low")
        GPIO.output(relaypin, GPIO.HIGH)
         
class runrealy(threading.Thread): # Relay Operate Thread
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            global relayonval1
            global realypin
            global auto_mode
            while True:
                #if(auto_mode == True):
                sec1 = rtc.getSeconds()
                print("Second:",sec1)
                if (59 == sec1):
                    print("Realy On Time: ",relayonval1)
                    GPIO.output(relaypin, GPIO.LOW)
                    time.sleep(relayonval1)
                    GPIO.output(relaypin, GPIO.HIGH)
                    checkrelaypin()
                time.sleep(1)
        except Exception as e:
            print(e)
            exec_info = sys.exc_info()
            logging.exception("CZIOT logging starts")
            logging.exception(e)
            logging.exception("CZIOT logging ends")
            GPIO.output(errorpin, GPIO.HIGH)
            return 0
            

def upfunc(self):
    try:    
        global hrval1,minval1,secval1,relayonval1
        
        if(GPIO.input(uppin) == 0):

            if (setpin_count == 1): # for Second
                if (secval1 == 59):
                    secval1 = 0
                else:
                    secval1 += 1
                lcd.cursor_pos = (0,11)
                lcd.write_string("%02d" %(secval1))
                lcd.cursor_pos = (0,12)
                lcd.cursor_mode = 'blink'
                    
            if (setpin_count == 2): # for minute
                if (minval1 == 59):
                    minval1 = 0
                else:
                    minval1 += 1
                lcd.cursor_pos = (0,8)
                lcd.write_string("%02d" %(minval1))
                lcd.cursor_pos = (0,9)
                lcd.cursor_mode = 'blink'

            if (setpin_count == 3): # for Hour
                if (hrval1 == 23):
                    hrval1 = 0
                else:
                    hrval1 += 1
                lcd.cursor_pos = (0,5)
                lcd.write_string("%02d" %(hrval1))
                lcd.cursor_pos = (0,6)
                lcd.cursor_mode = 'blink'

            if (setpin_count == 4): # for Motor ON time (0.01 value change)
                if (relayonval1 >= 5.00):
                    relayonval1 = relayonval1
                else:
                    relayonval1 += 0.01
                    relayonval1 = round(relayonval1,2)
                lcd.cursor_pos = (1,5)
                lcd.write_string("%.2f" %(relayonval1))
                lcd.cursor_pos = (1,8)
                lcd.cursor_mode = 'blink'
                
            if (setpin_count == 5): # for Motor ON time (0.1 value change)
                print(relayonval1)
                if (relayonval1 >= 5.00):
                    relayonval1 =relayonval1 
                else:
                    relayonval1 += 0.1
                    relayonval1 = round(relayonval1,2)
                lcd.cursor_pos = (1,5)
                lcd.write_string("%.2f" %(relayonval1))
                lcd.cursor_pos = (1,7)
                lcd.cursor_mode = 'blink'

            if (setpin_count == 6): # for Motor ON time (1 value change)
                if (relayonval1 >= 5.00):
                    relayonval1 = relayonval1
                else:
                    relayonval1 += 1
                    relayonval1 = round(relayonval1,2)
                lcd.cursor_pos = (1,5)
                lcd.write_string("%.2f" %(relayonval1))
                lcd.cursor_pos = (1,5)
                lcd.cursor_mode = 'blink'
                
            
                
    except Exception as e:
        print(e)
        exec_info = sys.exc_info()
        logging.exception("CZIOT logging starts")
        logging.exception(e)
        logging.exception("CZIOT logging ends")
        GPIO.output(errorpin, GPIO.HIGH)
        return 0

def downfunc(self):
    try:
        global hrval1,minval1,secval1,relayonval1
        
        if(GPIO.input(downpin) == 0):

            if (setpin_count == 1): # for Second
                if (secval1 == 00):
                    secval1 = 59
                else:
                    secval1 -= 1
                lcd.cursor_pos = (0,11)
                lcd.write_string("%02d" %(secval1))
                lcd.cursor_pos = (0,12)
                lcd.cursor_mode = 'blink'
            
            if (setpin_count == 2): # for minute
                if (minval1 == 00):
                    minval1 = 59
                else:
                    minval1 -= 1
                lcd.cursor_pos = (0,8)
                lcd.write_string("%02d" %(minval1))
                lcd.cursor_pos = (0,9)
                lcd.cursor_mode = 'blink'
                
            if (setpin_count == 3): # for Hour
                if (hrval1 == 0):
                    hrval1 = 23
                else:
                    hrval1 -= 1
                lcd.cursor_pos = (0,5)
                lcd.write_string("%02d" %(hrval1))
                lcd.cursor_pos = (0,6)
                lcd.cursor_mode = 'blink'

            if (setpin_count == 4): # for Motor ON time (0.01 value change)
                relayonval1 -= 0.01
                relayonval1 = round(relayonval1,2)
                if (relayonval1 <= 0.00):
                    relayonval1 = 0.00
                
                lcd.cursor_pos = (1,5)
                lcd.write_string("%.2f" %(relayonval1))
                lcd.cursor_pos = (1,8)
                lcd.cursor_mode = 'blink'
                
            if (setpin_count == 5): # for Motor ON time (0.1 value change)
                relayonval1 -= 0.1
                relayonval1 = round(relayonval1,2)
                if (relayonval1 <= 0.00):
                    relayonval1 = 0.00
                    
                lcd.cursor_pos = (1,5)
                lcd.write_string("%.2f" %(relayonval1))
                lcd.cursor_pos = (1,7)
                lcd.cursor_mode = 'blink'

            if (setpin_count == 6): # for Motor ON time (1 value change)
                relayonval1 -= 1
                relayonval1 = round(relayonval1,2)
                if (relayonval1 <= 0.00):
                    relayonval1 = 0.00
            
                lcd.cursor_pos = (1,5)
                lcd.write_string("%.2f" %(relayonval1))
                lcd.cursor_pos = (1,5)
                lcd.cursor_mode = 'blink'

            
                
    except Exception as e:
        print(e)
        exec_info = sys.exc_info()
        logging.exception("CZIOT logging starts")
        logging.exception(e)
        logging.exception("CZIOT logging ends")
        GPIO.output(errorpin, GPIO.HIGH)
        return 0
      
def controllfunc(self):
    try:
        global auto_mode
        global setpin_count
        global hrval1,minval1,secval1,relayonval1
        
        if(GPIO.input(setpin) == 0):
            #print("Setting Pin Pressed")
            setpin_count += 1
            
        if (setpin_count == 1): #for Secons
            hrval1 = rtc.getHours()
            minval1 = rtc.getMinutes()
            secval1 = rtc.getSeconds()
            print("Hr:" + str(hrval1) + " Min:" + str(minval1) + " Sec:" + str(minval1) + " R.ON:" + str(minval1))

            auto_mode = False
            lcd.cursor_pos = (0,12)
            lcd.cursor_mode = 'blink'
                
        elif (setpin_count == 2): #for minute
            auto_mode = False
            lcd.cursor_pos = (0,9)
            lcd.cursor_mode = 'blink'
            
        elif (setpin_count == 3): #for hour
            auto_mode = False
            lcd.cursor_pos = (0,6)
            lcd.cursor_mode = 'blink'

        elif (setpin_count == 4): # for Motor ON time (0.01 value change)
            auto_mode = False
            lcd.cursor_pos = (1,8)
            lcd.cursor_mode = 'blink'
            
        elif (setpin_count == 5): # for Motor ON time (0.1 value change)
            auto_mode = False
            lcd.cursor_pos = (1,7)
            lcd.cursor_mode = 'blink'
            
        elif (setpin_count == 6): # for Motor ON time (1 value change)
            auto_mode = False
            lcd.cursor_pos = (1,5)
            lcd.cursor_mode = 'blink'
            
        elif (setpin_count == 7): #set all values
            lcd.cursor_mode = 'hide'
            lcd.clear()
            
            rtc.setTime(seconds = secval1, minutes = minval1, hours = hrval1)
            writetextfile()
            
            lcd.cursor_pos = (1,0)
            lcd.write_string("Resetting....")
            time.sleep(1.5)
            auto_mode = True
            setpin_count = 0
            
    except Exception as e:
        print(e)
        exec_info = sys.exc_info()
        logging.exception("CZIOT logging starts")
        logging.exception(e)
        logging.exception("CZIOT logging ends")
        GPIO.output(errorpin, GPIO.HIGH)
        return 0
        
#START PROGRAM
print("*************** START PROGRAM ***************")

global relayonval1
global auto_mode
global setpin_count
auto_mode = True
relayonval1 = 1.00
relayonval1 = round(relayonval1,2)

setpin_count = 0
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename='/home/pi/clock_system/exceptiondata.txt')
initpinfunc()
readtextfile()

v1 = runlcd()
v2 = runrealy()
v3 = runled()
v1.start()
v2.start()
v3.start()


