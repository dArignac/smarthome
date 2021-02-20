#!/usr/bin/python3
import configparser
import json
import logging
import multiprocessing
import os
import sys
import threading

import paho.mqtt.client as mqtt
from btlewrap import BluepyBackend

from miflora import miflora_scanner
from miflora.miflora_poller import (
    MI_BATTERY,
    MI_CONDUCTIVITY,
    MI_LIGHT,
    MI_MOISTURE,
    MI_TEMPERATURE,
    MiFloraPoller,
)

# enable for debugging
# logging.basicConfig(level=logging.DEBUG, format='%(message)s')
# logger = logging.getLogger(__name__)

def read_config():
    sensors = []
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini"))
    if len(config["sensors"]) == 0:
        return sensors
    for key in config["sensors"]:
        # split key by underscore and captilize, e.g. jasmin_plant will become "Jasmin Plant"
        sensors.append(
            (
                " ".join(list(a.capitalize() for a in key.split("_"))),
                config["sensors"][key],
            )
        )
    return sensors

def get_sensor_data_and_publish(name, id):
    print(f"Querying sensor '{name}' with id '{id}")

    data = None
    try:
        poller = MiFloraPoller(id, BluepyBackend)
        data = {
            "name": name,
            "temperature": poller.parameter_value(MI_TEMPERATURE),
            "moisture": poller.parameter_value(MI_MOISTURE),
            "light": poller.parameter_value(MI_LIGHT),
            "conductivity": poller.parameter_value(MI_CONDUCTIVITY),
            "battery": poller.parameter_value(MI_BATTERY),
        }
    except:
        print(f"Unable to query sensor {name} with id {id}")
        return
    
    if data is not None:
        print(f"Publishing sensor '{name}' with id '{id}")
        try:
            client.publish("/home/miflora", payload=json.dumps(data), qos=1)
        except:
            print(f"Unable to publish data for sensor {name} to mqtt")

client = mqtt.Client()

def main():
    sensors = read_config()
    if len(sensors) == 0:
        print("No sensors configured, please create a config.ini file!")
        sys.exit()

    client.connect("127.0.0.1", 1883)

    jobs = []

    for _, value in enumerate(sensors):
        p = multiprocessing.Process(
            target=get_sensor_data_and_publish,
            args=(value[0], value[1])
        )
        jobs.append(p)
    
    for j in jobs:
        j.start()
    
    for j in jobs:
        j.join()

if __name__ == "__main__":
    main()
