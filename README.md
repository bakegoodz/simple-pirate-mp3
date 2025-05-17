# simple-pirate-mp3
Simple MP3 player for the Raspberry Pi and Pirate Audio Hat  
The Hat uses a st7789 screen and GPIO buttons  

How to install/use
Install Raspberry Pi OS  
Make sure set the settings in Raspberry Pi imager to enable SSH login and connecting to your network or wifi  

ssh to the raspberry pi  
mkdir music # put your mp3 files into this folder  
sudo apt update  
sudo apt upgrade  
sudo raspi-config # turn on spi and i2c in Interface Options  

sudo nano /boot/firmware/config.txt  
#Turn off built in HDMI audio  
dtparam=audio=off  
#add this below to enable Pirate Audio  
hdmi_audio=0  
dtoverlay=hifiberry-dac  
gpio=25=op,dh  

sudo apt install python3-rpi.gpio python3-spidev python3-pip python3-pil python3-numpy git libopenblas-dev mpg321  
sudo pip3 install pidi-display-st7789 --break-system-packages  

sudo reboot  

wget https://github.com/bakegoodz/simple-pirate-mp3/raw/refs/heads/main/mp3.py  
nano mp3.py  
# Change Directory to where your mp3 files are  
crontab -e  
@reboot sudo /usr/bin/python3 /home/user/mp3.py  
#Set this this to your path of mp3.py  
