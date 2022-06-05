#!/bin/sh
pip3 install -r requirements.txt
sudo pip3 install -r requirements.txt
crontab -l > /tmp/crontab; echo "* * * * * /home/$USER/smarthome/bluedevices/gather.py miflora --debug=0" >> /tmp/crontab; crontab /tmp/crontab; rm /tmp/crontab
sudo crontab -l > /tmp/crontabSudo; echo "* * * * * /home/$USER/smarthome/bluedevices/gather.py inkbird --debug=0" >> /tmp/crontabSudo; sudo crontab /tmp/crontabSudo; rm /tmp/crontabSudo