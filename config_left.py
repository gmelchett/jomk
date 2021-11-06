# SPDX-FileCopyrightText: 2021 Jonas Aaberg
#
# SPDX-License-Identifier: MIT

from keyboard_defines import kc
import board

layers = (
    ((kc.ONE, kc.TWO),
     (kc.THREE, kc.FOUR)),
)

matrix_row_pins = (board.GP14, board.GP15)
matrix_col_pins = (board.GP16, board.GP17)
