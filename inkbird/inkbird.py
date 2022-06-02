import sys

from bluepy import btle
from bluepy.btle import Scanner


class Updater():
    def __init__(self, mac) -> None:
        self.mac = mac
        self.scanner = Scanner()
        self.scanner.clear()
        self.scanner.start()

    def update(self):
        try:
            self.scanner.process(timeout=8.0)
        except:
            print("error", sys.exec_info()[0])

        for dev in self.scanner.getDevices():
            if dev.addr == self.mac:
                self.handleDiscovery(dev)

    def handleDiscovery(self, dev):
        print("Device {} ({}), RSSI={} dB".format(
            dev.addr, dev.addrType, dev.rssi))
        for (adtype, desc, value) in dev.getScanData():
            print("[%s]  %s = %s" % (adtype, desc, value))
            if adtype == 255:
                humidity = "%2.2f" % (int(value[6:8]+value[4:6], 16)/100)
                temperature = int(value[2:4]+value[:2], 16)
                temperature_bits = 16
                if temperature & (1 << (temperature_bits-1)):
                    temperature -= 1 << temperature_bits
                temperature = "%2.2f" % (temperature / 100)
                battery = int(value[14:16], 16)
                print(temperature, humidity, battery)


if __name__ == "__main__":
    up = Updater("")
    up.update()
