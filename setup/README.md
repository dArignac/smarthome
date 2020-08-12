# Prepare Raspberry Image1

Use the Github project https://github.com/RPi-Distro/pi-gen to generate a proper Raspberry Pi image. I'm in Germay so I set the keyboard etc. accordingly-

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

Then run the image creation with `./build-docker.sh`. It may take a while.

If it was successfull, write the image to the SD card. Use the Raspberry Pi Imager for that: https://www.raspberrypi.org/downloads/

# Install Docker

Install the prerequisites: `sudo apt-get install apt-transport-https ca-certificates software-properties-common -y`.

Install Docker `curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh`.

If it fails because of not being able to validate the certificate, run the following:

```
sudo apt update
sudo apt install --reinstall ca-certificates
sudo c_rehash
```

Enable the `pi` user to use Docker: `sudo usermod -aG docker pi`, afterwards logout and login again.

Check that Docker is running: `sudo systemctl status docker`.

Install docker-compose:

```
sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt-get install -y python3 python3-pip
sudo pip3 install docker-compose
sudo -E curl -L -o /etc/bash_completion.d/docker-compose https://raw.githubusercontent.com/docker/compose/$(docker-compose version --short)/contrib/completion/bash/docker-compose

```

# Attach Hard Disk

An external hard disk is used to store all the data, as writing it to the Raspberry's SD card will decrease its lifespan.

Ensure it has `etx4` file system. Plug it in. Ensure it can be found with `sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL`.

If found, create a new mount folder (of course you can name it different): `sudo mkdir /mnt/elements1`

With `sudo blkid` check the path of the disk and mount it accordingly: `sudo mount /dev/sda1 /mnt/elements1`

## Auto mounting

Grab the partition UUID `PARTUUID` with `sudo blkid`.

Edit `fstab` (`sudo nano /etc/fstab`) and add the line (replace the `UUID` with the partition id):

```
PARTUUID=14ec74ef-01  /mnt/elements1  ext4    defaults,auto,users,rw,nofail 0 0
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
sudo mkdir -p /mnt/elements1/mosquitto/data /mnt/elements1/mosquitto/log /mnt/elements1/nodered /mnt/elements1/influxdb /mnt/elements1/grafana
sudo chown 1000:995 /mnt/elements1/mosquitto /mnt/elements1/nodered /mnt/elements1/influxdb /mnt/elements1/grafana
```

# JeeLink

Attach in USB port and check fi recognized: `lsusb`.
It should be something like `Future Technology Devices International, Ltd FT232 Serial (UART) IC`.

Check `dmesg` to find where it was mounted: `dmesg | grep tty`
Should print something like that: `[  303.711275] usb 1-1.4: FTDI USB Serial Device converter now attached to ttyUSB0`.

Check that `/dev/ttyUSB0` exists.

Check the id of `dialout` group and adjust `docker-compose.yaml` at the nodered service ( `group_add`).
