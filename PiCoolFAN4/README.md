# PiCoolFAN4

After getting a Raspberry PI 4 I recognized its temperature in idle was pretty high compared to the Raspberry Pi 2 I used before: 60 °C instead of 40 °C.

Time for some cooling!

I reviewed the [PiCoolFAN4](https://pimodules.com/product/picoolfan4) and bought it. Installation was pretty easy, if you use a case with enough space (I use the [JOY-IT aluminium case](https://joy-it.net/en/products/RB-AlucaseP4+01B)). I'm not (yet) using any passive coolers.

The PiCoolFAN4 comes with a PDF manual and I scripted away the requirements to have it set up as follows:

- use the Raspberry PI temperature instead of its own sensor
- set the mild profile with a maximum temperature and the smoothest temperature stepping

Just run the `setup.sh`.

If you want to change the temperature threshold afterwards, run `sudo i2cset -y 1 0x60 0x0f 0xaa && sudo i2cset -y 1 0x60 0x01 <temp>`
