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
![image](https://user-images.githubusercontent.com/47386222/219616796-aa5bc192-eb6d-474f-960d-fa867222f761.png)
![image](https://user-images.githubusercontent.com/47386222/219616288-b84536df-3a8e-493d-bec2-aaf14dacba84.png)

![image](https://user-images.githubusercontent.com/47386222/219616950-5e5d8edf-b4de-4c90-a460-b78026977b01.png)
![image](https://user-images.githubusercontent.com/47386222/219617003-581dfd4c-12e2-412d-8d5d-b2236a5ca488.png)

