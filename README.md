# Smart Home?

## Prepare Raspberry Image

Use the Github project https://github.com/RPi-Distro/pi-gen to generate a proper Raspberry Pi image.

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

## Initialize Raspberry Pi

Log in, change password and grab Bash aliases: `curl -s https://raw.githubusercontent.com/darignac/fx/master/.bash_aliases > ~/.bash_aliases && source ~/.bash_aliases`.

## Install Docker

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

## Attach Hard Disk

Ensure it has `etx4` file system. Plug it in. Ensure it can be found with `sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL`.

If found, create a new mount folder: `sudo mkdir /mnt/elements1`

With `sudo blkid` check the path of the disk and mount it accordingly: `sudo mount /dev/sda1 /mnt/elements1`

### Auto mounting

Grab the partition UUID `PARTUUID` with `sudo blkid`.

Edit `fstab` (`sudo nano /etc/fstab`) and add the line (replace the `UUID` with the partition id):

```
PARTUUID=14ec74ef-01  /mnt/elements1  ext4    defaults,auto,users,rw,nofail 0 0
```

## Mosquitto

Will be run by `docker-compose`, but there are some prerequisites:

Create a folder where to store the mosquitto data: `sudo mkdir -P /mnt/elements/mosquitto/data /mnt/elements/mosquitto/log`.

Find your `pi` user id (usually `1000`) and the id of the docker group:

```
$ id pi
uid=1000(pi) gid=1000(pi) groups=1000(pi),4(adm),20(dialout),24(cdrom),27(sudo),29(audio),44(video),46(plugdev),60(games),100(users),105(input),109(netdev),999(spi),998(i2c),997(gpio),995(docker)
```

In this case it's `1000` for `pi`, and `995` for `docker`. If they are different from the `user` value in the `docker-compose.yaml`, then adjust it there.


## Sources

* https://www.docker.com/blog/happy-pi-day-docker-raspberry-pi/
* http://nilhcem.com/iot/home-monitoring-with-mqtt-influxdb-grafana
* https://www.raspberrypi.org/documentation/configuration/external-storage.md
