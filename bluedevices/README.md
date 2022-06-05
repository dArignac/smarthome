# Bluetooth Devices

Some bluetooth devices are supported. Their values are read from bluetooth and written to the
specific MQTT topic. Please read this whole document for setting it up properly.

Therefore the script `bluedevices/gather.py` is used and set up via crontab.
See the crontab entry in `bluedevices/setup.sh`. If you just want a specific type, you can
adjust it there. _Note that the inkbird script is added to the root user's crontab as it needs to
access bluetooth_.

_Supported types_

- `miflora` - [Xiaomi Mi Plant sensors](https://de.gearbest.com/other-garden-supplies/pp_373947.html).
- `inkbird` - Inkbird devices, only tested wih [Inkbird IBS-TH1](https://inkbird.com/products/bluetooth-thermometer-ibs-th1)

## Device identification

To configure the bluetooth device, we need its MAC address. There are multiple ways to gather it.

_The mac address of Miflora devices usually starts with `C4:7C:8D`._

### Android

You can use an Android app like [Bluetooth LE Scanner](https://play.google.com/store/apps/details?id=uk.co.alt236.btlescan).

If you already have multiple sensors running, this is probably the best approach, as you can go somewhere without bluetooth noise and scan for your sensor.

### Raspberry Pi 2

You will need a bluetooth dongle. I use the [TP-Link UB400](https://www.tp-link.com/de/home-networking/adapter/ub400/) which works out of the box.

Run `sudo bluetoothctl` and then run `scan on` and wait, to scan and list the devices around. Use `scan off` to stop scanning and `exit` to exit.

### Raspberry Pi 4

Run `sudo hcitool -lescan`.

## Device configuration

Per supported bluetooth device type there can be a config section in the `bluedevices/config.ini`.
Add a line per device to the section with the name of the device and its mac address. Ensure that the name is unique, as it will be used as device name in influxdb.

```
[miflora]
BeautifulPlant1 = C4:7C:8D:00:00:01
BeautifulPlant2 = C4:7C:8D:00:00:02

[inkbird]
Outdoor = 12:23:34:45:56:67
```
