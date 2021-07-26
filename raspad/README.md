# Raspad as kiosk

## Goals
- show current temperatures
- show weather forecase
- show weather warnings
- show water gauge of Elbe
- show Corona incidence

## Raspad adjustments
Should open Chromium in Kiosk mode on startup and hide the mouse cursor. Screen must be correctly aligned when standing in landscape mode.

- install `unclutter` for hiding the mouse cursor `sudo apt install unclutter xscreensaver`
- copy the `autostart` file to `~/.config/lxsession/LXDE-pi/autostart`
- edit `sudo nano /boot/config.txt` and add ([source](https://howchoo.com/pi/raspberry-pi-display-rotation))
  - `display_rotate=2`
  - `lcd_rotate=2`
- open screensaver settings and disable the screensaver
- disable browser cache

## Development TODO
- check if there is a dashboard framework or so that is up to date and does what we need or code yourself
  - should refresh every 30 minutes or so
- check how to embed Grafana Dashboards with preconfigured time values
- use OpenWeather for weather data - store to timeseries database?
