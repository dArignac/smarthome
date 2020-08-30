# Prepare Raspberry Image1

Use the Github project https://github.com/RPi-Distro/pi-gen to generate a proper Raspberry Pi image. I'm in Germay so I set the keyboard etc. accordingly.

Therefore create a `config` file like this:

```
IMG_NAME='Raspbian'
TARGET_HOSTNAME='nodered'
KEYBOARD_LAYOUT='Deutsch'
TIMEZONE_DEFAULT='Europe/Berlin'
WPA_ESSID='Wifi-Name'
WPA_PASSWORD='Wifi-Password'
ENABLE_SSH=1
STAGE_LIST='stage0 stage1 stage2'
```

It installs a somewhat minimal version of Raspberry OS having Wifi and SSH enabled and configured.

Then run the image creation with `./build-docker.sh`. It will take a while.

If it was successfull, write the image to the SD card. Use the Raspberry Pi Imager for that: https://www.raspberrypi.org/downloads/.

# Docker

Run `setup-docker.sh`.

# Attach Hard Disk

An external hard disk is used to store all the data, as writing it to the Raspberry's SD card will decrease its lifespan.

Ensure it has `etx4` file system. Plug it in. Ensure it can be found with `sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL`.

If found, create a new mount folder (of course you can name it different): `sudo mkdir /mnt/pi1`

With `sudo blkid` check the path of the disk and mount it accordingly: `sudo mount /dev/sda1 /mnt/pi1`

## Auto mounting

Grab the partition UUID `PARTUUID` with `sudo blkid`.

Edit `fstab` (`sudo nano /etc/fstab`) and add the line (replace the `UUID` with the partition id):

```
PARTUUID=14ec74ef-01  /mnt/pi1  ext4    defaults,auto,users,rw,nofail 0 0
```

# Tools

All tools being used are setup up via Docker and integrated into the `docker-compose.yaml` file.

But before ramping it up, we need to do some preparations:

## Storage folders

Grep the id of your `pi` user (or whatever you named it) and of the `docker` group.

```
$ id pi
uid=1000(pi) gid=1000(pi) groups=1000(pi),4(adm),20(dialout),24(cdrom),27(sudo),29(audio),44(video),46(plugdev),60(games),100(users),105(input),109(netdev),999(spi),998(i2c),997(gpio),995(docker)
```

Create the folders and set the permissions:

```
sudo mkdir -p /mnt/pi1/mosquitto/data /mnt/pi1/mosquitto/log /mnt/pi1/nodered /mnt/pi1/influxdb /mnt/pi1/grafana
sudo chown 1000:995 -R /mnt/pi1/mosquitto /mnt/pi1/nodered /mnt/pi1/influxdb /mnt/pi1/grafana
```

# JeeLink

Attach in USB port and check fi recognized: `lsusb`.
It should be something like `Future Technology Devices International, Ltd FT232 Serial (UART) IC`.

Check `dmesg` to find where it was mounted: `dmesg | grep tty`
Should print something like that: `[  303.711275] usb 1-1.4: FTDI USB Serial Device converter now attached to ttyUSB0`.

Check that `/dev/ttyUSB0` exists.

Check the id of `dialout` group and adjust `docker-compose.yaml` at the nodered service ( `group_add`).

## Flash Jeelink to turn off blue led

Download [Arduino IDE](https://www.arduino.cc/en/Main/Software).
Load the `LaCrosseITPlusReader10` sketch from the `jeelink` folder in the IDE. You may need to put it to `/home/<user>/Arduino`. Compile it and upload it to the JeeLink.

The sketch was provided by the FHEM project, you can grab it [here](https://svn.fhem.de/trac/browser/trunk/fhem/contrib/arduino/36_LaCrosse-LaCrosseITPlusReader.zip). I adjusted that the blue LED is permanently off because it annoys me.

I had issue with writing to the JeeLink, though my user belongs to the `dialout` group. The crude workaround was to run the Arduino IDE as root ¯\_(ツ)_/¯
