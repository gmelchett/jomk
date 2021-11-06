# jomk - Jonas Matrix Keyboard

## TL;DR;

Simple matrix keyboard driver written in python running on raspberry pi pico. Split keyboards supported.
Currently in beta status.


## Background

I wanted to try if it would be possible to write a matrix keyboard driver in python. And yes, it seems like it is possible
since the raspberry pi pico is quite fast for a microcontroller - 133 Mhz.
Adafruit's [circuitpython](https://circuitpython.org/) comes with USB HID support and it was very easy to get a matrix keyboard driver up and running.


## Features
  * Layers
  * Mouse support
  * Multikeys - one key on keyboard results in several keys being send
  * Split keyboard via UART (Four cables needed)
  * Split keyboard autodetetion of master/slave half


## Hardware setup
### Normal keyboard
 * Connect rows and columns wires to GPIOs like any other home-made keyboard. You can use all exposed GPIOS _except_ GPIO1 and GPIO2.
### Split keyboard
 * Connect GND between the picos - For example pin 38
 * Connect VSYS between the picos - Pin 39
 * Connect UART TX Pin 1 to UART RX Pin 2 on the other pico
 * Connect UART RX Pin 2 to UART TX Pin 1 on the other pico


## Installation
 * Create your own layout by editing ``config-left.py`` (or ``config-right.py``) jomk will first try to load ``config.py``, then ``config-right.py``, and last ``config-left.py``
 * Install [circuitpython](https://circuitpython.org/board/raspberry_pi_pico/) on one (or two for split keyboard) raspberry pi pico. I use version 7.0.0
 * Download the [circuitpython libaries](https://circuitpython.org/libraries) and copy the folder ``adafruit_hid`` including all files to ``lib`` on your pico(s).
 * copy ``keyboard_defines.py``, ``main.py`` and either ``config-left.py`` or ``config-right.py`` to the pico(s)
   Only one config file per pico.


## TODO
  * Multimedia keys
  * Hold down for temporary layer change + tap for another key
  * Switch layer for one keypress
  * Macro recording and playback
  * Mouse acceleration
  * Check pin config vs layout config at start


## Short commings
  * You can't use a jomk based keyboard in BIOS.
    Some additional code is (needed](https://circuitpython.readthedocs.io/en/latest/shared-bindings/usb_hid/index.html) I have not bothered to add it.
  * The USB HID descriptor is circuitpythons default. I've not yet seen any reason for writing my own.
  * circuitpython does not support the usage of the second core. It would have been very nice to have the matrix scanning on one core and the USB handling on the other.

## License
MIT
