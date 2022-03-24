
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


