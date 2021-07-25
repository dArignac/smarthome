# Raspad as kiosk

## Goals
- show current temperatures
- show weather forecase
- show weather warnings
- show water gauge of Elbe
- show Corona incidence

## Raspad adjustments
Should open Chromium in Kiosk mode on startup and hide the mouse cursor.

- install `unclutter` for hiding the mouse cursor `sudo apt install unclutter`
- copy the `autostart` file to `~/.config/lxsession/LXDE-pi/autostart`

## Development TODO
- check if there is a dashboard framework or so that is up to date and does what we need or code yourself
  - should refresh every 30 minutes or so
- check how to embed Grafana Dashboards with preconfigured time values
- use OpenWeather for weather data - store to timeseries database?
