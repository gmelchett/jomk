# SPDX-FileCopyrightText: 2021 Jonas Aaberg
#
# SPDX-License-Identifier: MIT

from keyboard_defines import kc
import board

layers = (
    ((kc.A, kc.B, kc.C, kc.D),
     (kc.E, kc.F, kc.G, kc.H),
     (kc.I, kc.J, kc.K, kc.L),
     (kc.M, kc.N, kc.O, kc.LAYER_NEXT)),

    (((kc.MOUSE_LEFT,kc.MOUSE_UP),    kc.MOUSE_UP,            (kc.MOUSE_RIGHT,kc.MOUSE_UP),    kc.MOUSE_WHEEL_UP),
     (kc.MOUSE_LEFT,                  kc.NONE,                kc.MOUSE_RIGHT,                  kc.MOUSE_WHEEL_DOWN),
     ((kc.MOUSE_LEFT, kc.MOUSE_DOWN), kc.MOUSE_DOWN,          (kc.MOUSE_DOWN, kc.MOUSE_RIGHT), kc.NONE),
     (kc.MOUSE_BUTTON_LEFT,           kc.MOUSE_BUTTON_MIDDLE, kc.MOUSE_BUTTON_RIGHT,           kc.LAYER_PREV)),

)

matrix_row_pins = (board.GP10, board.GP11, board.GP12,board.GP13)
matrix_col_pins = (board.GP21, board.GP20, board.GP19,board.GP18)
