# MiFlora

**IMPORTANT: Currently in evaluation, will integrate once it works.**

Tasks:
* can we run all of it in Docker?
* build docker image with https://github.com/GoogleContainerTools/distroless/tree/master/examples/python3
* need to give `/dev/ttyAMA0` to container

## Sensors
To identify the MAC address of the sensors, you can use an app like [Bluetooth LE Scanner](https://play.google.com/store/apps/details?id=uk.co.alt236.btlescan).

Or you use `sudo hcitool -lescan` directly on the Raspberry.

The MAC address usually starts with `C4:7C:8D`.
