# MiFlora

**IMPORTANT: Currently in evaluation, will integrate once it works.**

## Sensor identification
To configure the sensor, we need its MAC address. There are multiple ways to gather it.

The MAC address usually starts with `C4:7C:8D`.

### Android
You can use an Android app like [Bluetooth LE Scanner](https://play.google.com/store/apps/details?id=uk.co.alt236.btlescan).

If you already have multiple sensors running, this is probably the best approach, as you can go somewhere without bluetooth noise and scan for your sensor.

### Raspberry Pi 2
You will need a bluetooth dongle. I use the [TP-Link UB400](https://www.tp-link.com/de/home-networking/adapter/ub400/) which works out of the box.

Run `sudo bluetoothctl` and then run `scan on` and wait, to scan and list the devices around. Use `scan off` to stop scanning and `exit` to exit.

### Raspberry Pi 4
Run `sudo hcitool -lescan`.

## Sensor configuration
Add a line per sensor to the `config.ini` file with the name of the sensor and its mac address. Ensure that the name is unique.

```
[sensors]
Name1 = C4:7C:8D:00:00:01
Name2 = C4:7C:8D:00:00:02
```
