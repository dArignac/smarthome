#!/bin/sh
sudo pip3 install -r requirements.txt
crontab -l > /tmp/crontab; echo "* * * * * /home/$USER/smarthome/bluedevices/gather.py miflora --debug=0" >> /tmp/crontab; crontab /tmp/crontab; rm /tmp/crontab
