#/bin/sh
# enable I2C interface - it's weird that 0 means on and 1 means off
sudo raspi-config nonint do_i2c 0

# pip for installing smbus and the ic2tools
sudo apt install python-pip i2c-tools
sudo pip install smbus

# daemon to set raspi temperature to fan
sudo tee /lib/systemd/system/pcf4.service > /dev/null <<EOT
[Unit]
Description=PiCoolFAN4 Service supplying RPi core temperature to it
After=multi-user.target
[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/smarthome/PiCoolFAN4/pcf4.py
StandardOutput=inherit
StandardError=inherit
Restart=always
[Install]
WantedBy=multi-user.target
EOT
sudo chmod 644 /lib/systemd/system/pcf4.service
sudo systemctl daemon-reload
sudo systemctl enable pcf4.service
sudo systemctl start pcf4.service

# set cooling profile of fan to Rpi sensor and mild
sudo i2cset -y 1 0x60 0x0f 0xaa && sudo i2cset -y 1 0x60 0x08 0x02

# set temperature threshold
sudo i2cset -y 1 0x60 0x0f 0xaa && sudo i2cset -y 1 0x60 0x01 55

# set the tstep to 1
sudo i2cset -y 1 0x60 0x0f 0xaa && sudo i2cset -y 1 0x60 0x04 1
