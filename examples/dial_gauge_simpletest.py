# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


import board
import time
from dial_gauge import DIAL_GAUGE


my_dial = DIAL_GAUGE(10, 10, 50, 40, color=0x440044)

display = board.DISPLAY
display.show(my_dial)

for i in range(0, 100):
    my_dial.update(i)
    time.sleep(0.1)
