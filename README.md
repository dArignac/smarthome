# Smart Home?

We're going to use the following tools to tie together a smart home of some sorts on a Raspberry Pi:

* [Nodered](https://nodered.org/)
* [Mosquitto](https://https://mosquitto.org/)
* [influxdb](https://www.influxdata.com/products/influxdb-overview/)
* [Grafana](https://grafana.com/)

## Open Tasks aka Roadmap

* script the pi setup mentioned in this readme
  * user and group ids via env (here in readme and compose file)
  * credentials in compose can be overwritten with `docker-compose.override.yaml`
* setup influxdb
  * create retention policy https://docs.influxdata.com/influxdb/v1.8/query_language/manage-database/
* create some smart stuff
  * fritzbox stats
    * power usage on plugs
  * gather raspberry sensors and display them in grafana
    * task count
    * sdcard used|free space
    * sdcard used|free space
    * hdd free space in relation to size
    * smart stats for external hdd and sdcard?
    * influxdb stats?
    * https://www.elektronik-kompendium.de/sites/raspberry-pi/1911251.htm
    * https://www.elektronik-kompendium.de/sites/raspberry-pi/2006071.htm
    * https://learn.adafruit.com/an-illustrated-shell-command-primer/checking-file-space-usage-du-and-df
  * collect and display the temperature of tmp sensors via jeelink - https://flows.nodered.org/flow/05a76b25495eb8fd8d3082343f56c645
  * display weather forecast (based on regional weather station data?)
  * gather plant sensor data
    * must see how to assign to a special plant to have alerts based on requirements of the plant
  * integrate the fritz smart plugs into nodered dashboard and get rid of the android app
  * if in homeoffice (calendar?) switch on the plug for the office desk

## Setup of Raspberry Pi and tooling

See [SETUP.md](SETUP.md).

### Nodered

Additionally install the following packages:

```
node-red-dashboard
node-red-contrib-influxdb
```

## Influxdb shell

Run `docker-compose exec influxdb influx -precision rfc3339 -database db0`

## MQTT Topics

```
# topic for all raspberry pis data
/home/pis/<pi-name>/health
```

## Publish RPi health data

As everything runs in Docker but we want to gather the health data of the Raspberry Pi that runs all the services, we need to publish the data via MQTT and then handle in nodered.

There we use a small script that gathers all the information and publishes them to the MQTT topic via cronjob every minute. Therefore we need to install some libs:

```
pip3 install paho-mqtt
sudo apt-get install sysstat
```

And setup the crontab:

```
echo "* * * * * python3 /home/pi/smarthome/nodered-health.py" | crontab -
```

## Flows
Rough overview what is currently done with the setup:

* (INPROGRESS) `nodered` pi health data (via script) -> mqtt -> nodered (normalization) -> influxdb -> grafana dashboard

## Sources used for creating this (loose order)

* https://www.docker.com/blog/happy-pi-day-docker-raspberry-pi/
* https://nodered.org/docs/getting-started/docker
* https://hub.docker.com/_/eclipse-mosquitto
* https://www.raspberrypi.org/documentation/configuration/external-storage.md
* https://github.com/eclipse/mosquitto/issues/1078#issuecomment-489438907
* http://nilhcem.com/iot/home-monitoring-with-mqtt-influxdb-grafana
* https://hub.docker.com/_/influxdb
* https://docs.influxdata.com/influxdb/v1.8/concepts/key_concepts/
* https://grafana.com/docs/grafana/latest/installation/configure-docker/
