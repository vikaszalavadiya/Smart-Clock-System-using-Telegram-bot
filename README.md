# Smart Tower clock system (Using Python, Telegram bot, Raspberry Pi)
---------------------------------

### Installation library
---------------------------------
sudo apt-get update  
sudo apt-get upgrade  
sudo apt-get install python-pip   
sudo pip install RPLCD   
sudo pip3 install telepot  
sudo apt install fswebcam  

### Setup Raspberry Pi
---------------------------------  
Set Interfaces & Time:  
VNC: ON  
SSH: ON  
I2C: ON  
Set =>Time, Language & Wi-Fi country.  

Change Hostname & Password:  
Hostname: XXXX  
Password: XXXX  

Connect the Wi-Fi:  
SSID: XXXX  
Password: XXXX  


### Set IP Address (Not Needed Now)
---------------------------------
sudo nano /etc/dhcpcd.conf  
**Edit Lines:**  
interface eth0  
static ip_address=192.168.1.100/24  
static routers=192.168.1.1  
static domain_name_servers=192.168.1.1 8.8.8.8  

### Disable Bluetooth & Audio (Not Needed Now)  
---------------------------------  
Edit Config .txt file. (Add line at last)  

sudo nano /boot/config.txt  
#dtparam=audio=on  
#Comment this to disable Bluetooth  
dtoverlay=pi3-disable-bt  


Set to Auto Run Program  (Edit crontrab file)
---------------------------------

crontab -e  
@reboot sudo ifconfig wlan0 up  
@reboot anydesk  
@reboot sleep 1;sudo /usr/bin/python3 /home/pi/clock_system/main.py &  

Screenshots
---------------------------------

![image](https://user-images.githubusercontent.com/47386222/219615952-b3ef1c72-cfdd-48c2-8ea6-ae44c02ba19f.png)

![image](https://user-images.githubusercontent.com/47386222/219616043-f96f2bc3-8dd2-4750-b921-8ad8307e8627.png)

![image](https://user-images.githubusercontent.com/47386222/219616098-8e396c06-7627-4a4c-ba10-2e619812c6ef.png)

![image](https://user-images.githubusercontent.com/47386222/219616150-8e9a03d1-299a-4c3a-aa14-bba211132693.png)

