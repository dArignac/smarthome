#!/bin/sh
sudo pip3 install -r requirements.txt
crontab -l > /tmp/crontab; echo "* * * * * /home/$USER/smarthome/miflora/gather.py" >> /tmp/crontab; crontab /tmp/crontab; rm /tmp/crontab
