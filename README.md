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

![image](https://user-images.githubusercontent.com/47386222/217337132-1526d1eb-2563-47df-a48d-85200daa060d.png)

![image](https://user-images.githubusercontent.com/47386222/217337366-530243b2-9f78-4d63-b075-d0a3012534f7.png)

![image](https://user-images.githubusercontent.com/47386222/217337660-6b9f25bf-c283-4bd9-8649-2472c2649e5b.png)
![image](https://user-images.githubusercontent.com/47386222/217340413-ca922749-98ac-469f-adfa-c9df0a4b3e2c.png)


