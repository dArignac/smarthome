#!/bin/sh
# RPi health script
pip3 install paho-mqtt
sudo apt install -y sysstat
crontab -l > /tmp/crontab; echo "* * * * * /home/$USER/smarthome/scripts/raspi-health.py" >> /tmp/crontab; crontab /tmp/crontab; rm /tmp/crontab
