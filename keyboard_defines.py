# SPDX-FileCopyrightText: 2021 Jonas Aaberg
#
# SPDX-License-Identifier: MIT

import adafruit_hid.keycode

class kc(adafruit_hid.keycode.Keycode):
    special_events_start = 0x1000
    NONE                 = 0x1000

    mouse_range_start      = 0x1100
    mouse_move_range_start = 0x1100
    MOUSE_LEFT             = 0x1100
    MOUSE_RIGHT            = 0x1101
    MOUSE_UP               = 0x1102
    MOUSE_DOWN             = 0x1103
    mouse_move_range_end   = 0x1104
    MOUSE_WHEEL_UP         = 0x1104
    MOUSE_WHEEL_DOWN       = 0x1105
    MOUSE_BUTTON_LEFT      = 0x1106
    MOUSE_BUTTON_MIDDLE    = 0x1107
    MOUSE_BUTTON_RIGHT     = 0x1108
    mouse_range_end        = 0x1200

    layer_range_start = 0x1200
    LAYER_SET_0       = 0x1200
    LAYER_SET_1       = 0x1201
    LAYER_SET_2       = 0x1202
    LAYER_SET_3       = 0x1203
    LAYER_SET_4       = 0x1204
    LAYER_SET_5       = 0x1205
    LAYER_SET_6       = 0x1206
    LAYER_SET_7       = 0x1207
    LAYER_SET_8       = 0x1208
    LAYER_SET_9       = 0x1209
    LAYER_PREV        = 0x120A
    LAYER_NEXT        = 0x120B

    layer_range_end   = 0x1300
