# SPDX-FileCopyrightText: 2021 Jonas Aaberg
#
# SPDX-License-Identifier: MIT

import time
import os
import board
import digitalio
import busio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from keyboard_defines import kc

class event:
    NONE = 0
    PRESS = 1
    RELEASE = 2
    def __init__(self, event=NONE, foreign=False):
        self.event = event
        self.foreign = foreign

class state:
    def __init__(self, timestamp=0.0, foreign=False):
        self.timestamp = timestamp
        self.foreign = foreign

class keyboardBase:

    def __init__(self, layers, matrix_row_pins, matrix_col_pins, debug=False):
        self.matrix_row = []
        self.matrix_col = []
        self.states = {}
        self.layers = layers
        self.curr_layer = 0
        self.debug = debug

        if self.debug:
            print("base debug")
            self.led = digitalio.DigitalInOut(board.LED)
            self.led.direction = digitalio.Direction.OUTPUT

        self.uart = busio.UART(tx=board.GP0, rx=board.GP1, parity=busio.UART.Parity.EVEN, baudrate=115200)

        for pin in matrix_row_pins:
            io_pin = digitalio.DigitalInOut(pin)
            io_pin.direction = digitalio.Direction.INPUT
            io_pin.pull = digitalio.Pull.DOWN
            self.matrix_row += [io_pin]

        for pin in matrix_col_pins:
            io_pin = digitalio.DigitalInOut(pin)
            io_pin.direction = digitalio.Direction.OUTPUT
            io_pin.value = False
            self.matrix_col += [io_pin]

    def handle_layer(self, v):
        if v < kc.layer_range_start or v >= kc.layer_range_end:
            return

        if v >= kc.LAYER_SET_0 and v <= kc.LAYER_SET_9:
            self.curr_layer = v - kc.layer_range_start
        elif v == kc.LAYER_PREV:
            self.curr_layer -= 1
            if self.curr_layer < 0:
                self.curr_layer = len(self.layers)-1
        elif v == kc.LAYER_NEXT:
            self.curr_layer += 1
            if self.curr_layer == len(self.layers):
                self.curr_layer = 0
        if self.debug:
            print("new layer %d" % self.curr_layer)

    def scan_matrix(self):
        events = {}

        for col_pin in range(len(self.matrix_col)):
            self.matrix_col[col_pin].value = True
            time.sleep(0.01)

            for row_pin in range(len(self.matrix_row)):

                v = self.layers[self.curr_layer][col_pin][row_pin]
                if v == kc.NONE:
                    continue

                if type(v) == tuple:
                    for i in v:
                        if self.matrix_row[row_pin].value:
                            events[i] = event(event.PRESS)
                        elif i in self.states:
                            events[i] = event(event.RELEASE)
                else:
                    if self.matrix_row[row_pin].value:
                        events[v] = event(event.PRESS)
                    elif v in self.states and not self.states[v].foreign:
                        events[v] = event(event.RELEASE)

            self.matrix_col[col_pin].value = False

        return events

class keyboardSlave(keyboardBase):
    def __init__(self, layers, matrix_row_pins, matrix_col_pins, debug=False):
        super().__init__(layers, matrix_row_pins, matrix_col_pins, debug)

    def handle_events(self, events):
        writeQueue = {}

        while self.uart.in_waiting >= 4:
            e = int.from_bytes(self.uart.read(2), 'little')
            v = int.from_bytes(self.uart.read(2), 'little')
            events[v] = event(event=e, foreign=True)

        for v in events:
            if v not in self.states and events[v].event == event.PRESS:
                self.handle_layer(v)

                if self.debug:
                    self.led.value = True
                writeQueue[v] = events[v]
                self.states[v] = state()

            elif v in self.states and events[v].event == event.PRESS:
                if v >= kc.mouse_move_range_start and v < kc.mouse_move_range_end:
                    writeQueue[v] = events[v]

            elif events[v].event == event.RELEASE:
                if self.debug:
                    self.led.value = False

                writeQueue[v] = events[v]
                self.states.pop(v)

        for v in writeQueue:
            if not events[v].foreign:
                self.uart.write(writeQueue[v].event.to_bytes(2, 'little'))
                self.uart.write(v.to_bytes(2, 'little'))

    def run(self):
        while True:
            events = self.scan_matrix()
            self.handle_events(events)


class keyboardMaster(keyboardBase):
    def __init__(self, layers, matrix_row_pins, matrix_col_pins, debug=False):
        super().__init__(layers, matrix_row_pins, matrix_col_pins, debug)

    def handle_events(self, events):

        while self.uart.in_waiting >= 4:
            e = int.from_bytes(self.uart.read(2), 'little')
            v = int.from_bytes(self.uart.read(2), 'little')
            events[v] = event(event=e, foreign=True)

        for v in events:

            # none -> press
            # press -> press
            # press -> release
            # none -> none

            if v not in self.states and events[v].event == event.PRESS:
                if self.debug:
                    self.led.value = True
                    print("Press", v, events[v].foreign)

                self.states[v] = state(foreign=events[v].foreign)

                self.handle_layer(v)

                # none & press -> key press
                if v < kc.special_events_start:
                    self.kbd.press(v)
                elif v >= kc.mouse_move_range_start and v < kc.mouse_move_range_end:
                    self.states[v].timestamp = time.monotonic()
                elif v == kc.MOUSE_WHEEL_UP:
                    self.mouse.move(wheel=1)
                elif v == kc.MOUSE_WHEEL_DOWN:
                    self.mouse.move(wheel=-1)
                elif v == kc.MOUSE_BUTTON_LEFT:
                    self.mouse.click(Mouse.LEFT_BUTTON)
                elif v == kc.MOUSE_BUTTON_MIDDLE:
                    self.mouse.click(Mouse.MIDDLE_BUTTON)
                elif v == kc.MOUSE_BUTTON_RIGHT:
                    self.mouse.click(Mouse.RIGHT_BUTTON)
                elif v >= kc.layer_range_start and v < kc.layer_range_end:
                    if not events[v].foreign:
                        self.uart.write(events[v].event.to_bytes(2, 'little'))
                        self.uart.write(v.to_bytes(2, 'little'))


            elif v in self.states and events[v].event == event.PRESS:
                # press & press -> move mouse
                if v >= kc.mouse_move_range_start and v < kc.mouse_move_range_end:
                    now = time.monotonic()
                    if self.states[v].timestamp != now:
                        if v == kc.MOUSE_LEFT:
                            self.mouse.move(x=-5)
                        elif v == kc.MOUSE_RIGHT:
                            self.mouse.move(x=5)
                        elif v == kc.MOUSE_UP:
                            self.mouse.move(y=-5)
                        elif v == kc.MOUSE_DOWN:
                            self.mouse.move(y=5)

            elif events[v].event == event.RELEASE:
                if self.debug:
                    self.led.value = False
                    print("Release", v, events[v].foreign)

                if v < kc.special_events_start:
                    self.kbd.release(v)
                elif v >= kc.layer_range_start and v < kc.layer_range_end:
                    if not events[v].foreign:
                        self.uart.write(events[v].event.to_bytes(2, 'little'))
                        self.uart.write(v.to_bytes(2, 'little'))
                self.states.pop(v)

    def run(self):
        self.kbd = Keyboard(usb_hid.devices)
        self.mouse = Mouse(usb_hid.devices)

        while True:
            events = self.scan_matrix()
            self.handle_events(events)

if __name__ == "__main__":
    config_loaded = False

    try:
        from config import layers, matrix_row_pins, matrix_col_pins
        config_loaded = True
    except ImportError:
        pass

    if not config_loaded:
        try:
            from config_right import layers, matrix_row_pins, matrix_col_pins
            config_loaded = True
        except ImportError:
            pass

    if not config_loaded:
        try:
            from config_left import layers, matrix_row_pins, matrix_col_pins
        except ImportError:
            print("ERROR: No configuration file found!")
            raise ImportError

    usb_powered = digitalio.DigitalInOut(board.GP24)
    usb_powered.direction = digitalio.Direction.INPUT

    dbg = False
    try:
        os.stat("debug")
        print(" * Debug enabled")
        dbg = True
    except OSError:
        pass

    time.sleep(1)

    if usb_powered.value:
        # TODO: Fix for bios
        #usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE, usb_hid.Device.CONSUMER_CONTROL), 2)
        #usb_cdc.enable()
        kb = keyboardMaster(layers, matrix_row_pins, matrix_col_pins, debug=dbg)
    else:
        #usb_cdc.enable()
        kb = keyboardSlave(layers, matrix_row_pins, matrix_col_pins, debug=dbg)

    kb.run()
