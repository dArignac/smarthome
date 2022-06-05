#!/usr/bin/python3
import argparse
import configparser
import multiprocessing
import os
import sys
import json

from bluepy.btle import Scanner

import paho.mqtt.client as mqtt
from btlewrap import BluepyBackend

from miflora.miflora_poller import (
    MI_BATTERY,
    MI_CONDUCTIVITY,
    MI_LIGHT,
    MI_MOISTURE,
    MI_TEMPERATURE,
    MiFloraPoller,
)

client = mqtt.Client()

DEBUG = False
SENSOR_TYPES = ["miflora", "inkbird"]


class Inkbird():
    def __init__(self, name, mac, mqtt) -> None:
        self.name = name
        self.mac = mac.lower()
        self.mqtt = mqtt
        self.scanner = Scanner()
        self.scanner.clear()
        self.scanner.start()
        self.update()

    def update(self):
        try:
            self.scanner.process(timeout=8.0)
        except:
            print("error scanning bluetooth for inkbird", sys.exec_info()[0])

        for dev in self.scanner.getDevices():
            if dev.addr == self.mac:
                self.handleDevice(dev)

    def handleDevice(self, dev):
        if DEBUG:
            print("Bluetooth querying inkbird device {} ({}), RSSI={} dB".format(
                dev.addr, dev.addrType, dev.rssi))
        for (adtype, desc, value) in dev.getScanData():
            # print("[%s]  %s = %s" % (adtype, desc, value))
            if adtype == 255:
                humidity = int(value[6:8]+value[4:6], 16)/100
                temperature = int(value[2:4]+value[:2], 16)
                temperature_bits = 16
                if temperature & (1 << (temperature_bits-1)):
                    temperature -= 1 << temperature_bits
                temperature = (temperature / 100)
                battery = int(value[14:16], 16)
                self.toMQTT(temperature, humidity, battery)

    def toMQTT(self, temperature, humidity, battery):
        payload = {
            "battery": battery,
            "humidity": humidity,
            "temperature": temperature,
            "sensor": self.name
        }
        try:
            client.publish(
                "/home/bluetooth/inkbird",
                payload=json.dumps(payload),
                qos=1
            )
        except:
            print(
                f"Unable to publish data for inkbird sensor {self.name} to mqtt")


def read_config():
    sensors = {}
    config = configparser.ConfigParser()
    try:
        config.read(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "config.ini"))
        for sensor_type in SENSOR_TYPES:
            sensors[sensor_type] = []
            for key in config[sensor_type]:
                # split key by underscore and captilize, e.g. jasmin_plant will become "Jasmin Plant"
                sensors[sensor_type].append(
                    (
                        " ".join(list(a.capitalize() for a in key.split("_"))),
                        config[sensor_type][key],
                    )
                )
    except:
        pass
    return sensors


# FIXME the job handling is inefficient if we have multiple inkbirds, as we scan for each device again
def publish_inkbird(sensor_name, sensor_mac):
    if DEBUG:
        print(
            f"Querying inkbird sensor '{sensor_name}' with mac '{sensor_mac}")
    Inkbird(sensor_name, sensor_mac, client)


def publish_miflora(sensor_name, sensor_mac):
    if DEBUG:
        print(
            f"Querying miflora sensor '{sensor_name}' with mac '{sensor_mac}")

    data = None
    try:
        poller = MiFloraPoller(sensor_mac, BluepyBackend)
        data = {
            "name": sensor_name,
            "temperature": poller.parameter_value(MI_TEMPERATURE),
            "moisture": poller.parameter_value(MI_MOISTURE),
            "light": poller.parameter_value(MI_LIGHT),
            "conductivity": poller.parameter_value(MI_CONDUCTIVITY),
            "battery": poller.parameter_value(MI_BATTERY),
        }
    except Exception as e:
        print(
            f"Unable to query miflora sensor {sensor_name} with id {sensor_mac} -> {e}")
        return

    if data is not None:
        if DEBUG:
            print(
                f"Publishing miflora sensor '{sensor_name}' with id '{sensor_mac}")
        try:
            client.publish(
                "/home/bluetooth/miflora",
                payload=json.dumps(data),
                qos=1
            )
        except:
            print(
                f"Unable to publish data for miflora sensor {sensor_name} to mqtt")


def main(requested_sensor_types):
    config = read_config()
    client.connect("127.0.0.1", 1883)
    jobs = []

    for sensor_type in SENSOR_TYPES:
        if sensor_type in requested_sensor_types:
            for _, value in enumerate(config[sensor_type]):
                p = multiprocessing.Process(
                    target=getattr(sys.modules[__name__],
                                   f"publish_{sensor_type}"),
                    args=(value[0], value[1])
                )
                jobs.append(p)

    if len(jobs) > 0:
        for j in jobs:
            j.start()

        for j in jobs:
            j.join()


def comma_separated_list(string):
    return [x.strip() for x in string.split(",") if x in SENSOR_TYPES]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sensors",
        help="sensor identifiers as comma seperated list. Unknown values will be stripped. Example: miflora,inkbird",
        type=comma_separated_list
    )
    parser.add_argument("--debug", type=int, help="print debug information")
    args = parser.parse_args()

    DEBUG = args.debug == 1
    main(args.sensors)
