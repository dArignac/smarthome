# Jeelink with LaCrosse Sensors

The following is from https://flows.nodered.org/flow/05a76b25495eb8fd8d3082343f56c645.
Just in case it is removed, keep it here for reference.

See the Jeelink flow for the function to convert the values.


```
# Temperature sensor - Format:
#      0   1   2   3   4
# -------------------------
# OK 9 56  1   4   156 37     ID = 56  T: 18.0  H: 37  no NewBatt
# OK 9 49  1   4   182 54     ID = 49  T: 20.6  H: 54  no NewBatt
# OK 9 55  129 4   192 56     ID = 55  T: 21.6  H: 56  WITH NewBatt

# OK 9 2   1   4 212 106       ID = 2   T: 23.6  H: -- Channel: 1
# OK 9 2   130 4 225 125       ID = 2   T: 24.9  H: -- Channel: 2

# OK 9 ID XXX XXX XXX XXX
# |  | |  |   |   |   |
# |  | |  |   |   |   --- Humidity incl. WeakBatteryFlag
# |  | |  |   |   |------ Temp * 10 + 1000 LSB
# |  | |  |   |---------- Temp * 10 + 1000 MSB
# |  | |  |-------------- Sensor type (1 or 2) +128 if NewBatteryFlag
# |  | |----------------- Sensor ID
# |  |------------------- fix "9"
# |---------------------- fix "OK"
```
