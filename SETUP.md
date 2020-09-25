# Prepare Raspberry Image

Use the Github project https://github.com/RPi-Distro/pi-gen to generate a proper Raspberry Pi image. I'm in Germay so I set the keyboard etc. accordingly.

Therefore create a `config` file like this:

```
IMG_NAME='Raspbian'
TARGET_HOSTNAME='nodered'
KEYBOARD_LAYOUT='Deutsch'
TIMEZONE_DEFAULT='Europe/Berlin'
WPA_ESSID='Wifi-Name'
WPA_PASSWORD='Wifi-Password'
WPA_COUNTRY='DE'
ENABLE_SSH=1
STAGE_LIST='stage0 stage1 stage2'
```

It installs a somewhat minimal version of Raspberry OS having Wifi and SSH enabled and configured.

**NOTE:** for the Raspberry Pi 4 model with 5 GHz wifi, the wifi is disabled per default.

There is a [PR](https://github.com/RPi-Distro/pi-gen/pull/416) open as of 2020-09-01 that fixes the issue. Until it is merged, you can grab the changes like so:

```
# if already cloned, ensure your on the current master
git clone https://github.com/RPi-Distro/pi-gen.git
cd pi-gen
git fetch origin pull/416/head:wifi-fix
git checkout wifi-fix
```

Then run the image creation with `./build-docker.sh`. It will take a while.
If it fails (it certainly does on my system), just rerun with `CONTINUE=1 ./build-docker.sh`.

If it was successfull, write the image (it is in the `deploy` folder) to the SD card. Use the Raspberry Pi Imager for that: https://www.raspberrypi.org/downloads/.

# Raspberry Pi Setup

Start the Pi and connect via SSH.

Set a new password for the `pi` user: `passwd`.

Install git to be able to clone the repo: `sudo apt install -y git`.

Clone the repo `git clone https://github.com/dArignac/smarthome.git`.

# Docker and other prerequisites

Run `setup.sh`. It should complete without any error and shows that docker is running.

Log out and log in again to have the group change reflected on the current user.

# Attach Hard Disk

An external hard disk is used to store all the data, as writing it to the Raspberry's SD card will decrease its lifespan.

Ensure it has `etx4` file system. Plug it in. Ensure it can be found with `sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL`.

If found, create a new mount folder (of course you can name it different): `sudo mkdir /mnt/pi1`

With `sudo blkid` check the path of the disk and mount it accordingly: `sudo mount /dev/sda1 /mnt/pi1`

## Auto mounting

Grab the partition UUID `PARTUUID` with `sudo blkid`.

Edit `fstab` (`sudo nano /etc/fstab`) and add the line (replace the `PARTUUID` with the partition id):

```
PARTUUID=14ec74ef-01  /mnt/pi1  ext4    defaults,auto,users,rw,nofail 0 0
```

# Storage folders

Grep the id of your user and of the `docker` group.

```
$ id $USER
uid=1000(pi) gid=1000(pi) groups=1000(pi),4(adm),20(dialout),24(cdrom),27(sudo),29(audio),44(video),46(plugdev),60(games),100(users),105(input),109(netdev),999(spi),998(i2c),997(gpio),995(docker)
```

Create the folders and set the permissions:

```
sudo mkdir -p /mnt/pi1/mosquitto/data /mnt/pi1/mosquitto/log /mnt/pi1/nodered /mnt/pi1/influxdb /mnt/pi1/grafana
sudo chown 1000:995 -R /mnt/pi1/mosquitto /mnt/pi1/nodered /mnt/pi1/influxdb /mnt/pi1/grafana
```

# JeeLink

Attach in USB port and check if recognized: `lsusb`.
It should be something like `Future Technology Devices International, Ltd FT232 Serial (UART) IC`.

Check `dmesg` to find where it was mounted: `dmesg | grep tty`
Should print something like that: `[  303.711275] usb 1-1.4: FTDI USB Serial Device converter now attached to ttyUSB0`.

Check that `/dev/ttyUSB0` exists.

Check the id of `dialout` group and adjust `docker-compose.yaml` at the nodered service ( `group_add`) if the id **is not** `20`.

## Flash Jeelink to turn off blue led

Download [Arduino IDE](https://www.arduino.cc/en/Main/Software).

Load the `LaCrosseITPlusReader10` sketch from the `jeelink` folder in the IDE. You may need to put it to `/home/<user>/Arduino`. Compile it and upload it to the JeeLink.

The sketch was provided by the FHEM project, you can grab it [here](https://svn.fhem.de/trac/browser/trunk/fhem/contrib/arduino/36_LaCrosse-LaCrosseITPlusReader.zip). I adjusted that the blue LED is permanently off because it annoys me.

I had issue with writing to the JeeLink, though my user belongs to the `dialout` group. The crude workaround was to run the Arduino IDE as root ¯\\_(ツ)_/¯

# Publish RPi health data

As everything runs in Docker but we want to gather the health data of the Raspberry Pi that runs all the services, we need to publish the data via MQTT and then handle in nodered.

There we use a small script that gathers all the information and publishes them to the MQTT topic via cronjob every minute. The script is automatically installed in the crontab.
