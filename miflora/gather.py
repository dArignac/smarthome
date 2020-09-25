#!/usr/bin/python3
import configparser
import json
import os
import sys

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


def main():
    sensors = read_config()
    if len(sensors) == 0:
        print("No sensors configured!")
        sys.exit()

    client = mqtt.Client()
    client.connect("127.0.0.1", 1883)

    for _, value in enumerate(sensors):
        poller = MiFloraPoller(value[1], BluepyBackend)
        data = {
            "name": value[0],
            "temperature": poller.parameter_value(MI_TEMPERATURE),
            "moisture": poller.parameter_value(MI_MOISTURE),
            "light": poller.parameter_value(MI_LIGHT),
            "conductivity": poller.parameter_value(MI_CONDUCTIVITY),
            "battery": poller.parameter_value(MI_BATTERY),
        }
        client.publish("/home/miflora", payload=json.dumps(data), qos=1)


if __name__ == "__main__":
    main()
