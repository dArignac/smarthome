#!/usr/bin/python
# -*- coding: utf-8 -*-
# Written by Ioannis A.Mourtsiadis info@pimodules.compile
# Supplying PiCoolFAN4 with core temperature via I2C


import sys
import time
import datetime
import os
import re     
import getopt

import smbus
import time
import datetime

#You can install psutil using: sudo pip install psutil
#import psutil

i2c = smbus.SMBus(1)

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    time.sleep(0.1)
    res = os.popen('vcgencmd measure_temp').readline()
    cpu_data=res.replace("temp=","").replace("'C\n","")
    cpu_int=int(float(cpu_data))
    return format(cpu_int,"02d")

def PCF4_ctemp():
   time.sleep(0.1)
   cpu_tmp=int(getCPUtemperature(),10)
   i2c.write_byte_data(0x60, 0x00, cpu_tmp)
   time.sleep(0.1)
   ctemp = i2c.read_byte_data(0x60, 0x00)
   ctemp = format(ctemp,"02d")
   return ctemp
   
while True:
    PCF4_ctemp()
    time.sleep(1)


