# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`dial_gauge`
================================================================================

Dial gauge widget for displayio


* Author(s): Jose D. Montoya


"""
try:
    from displayio import Group
except ImportError:
    pass
from math import sin, cos, ceil, pi
import displayio
from ulab import numpy as np
from bitmaptools import draw_line
from vectorio import Polygon
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font
import terminalio

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_DIAL_GAUGE.git"


class DIAL_GAUGE(Group):
    """
    Dial Class
    """

    def __init__(
        self,
        x: int,
        y: int,
        r_ext: int,
        r_int: int,
        range_values: list = [0, 100],
        color: int = 0x00FF00,
        background_color: int = 0x000000,
        font_file=None,
    ) -> None:
        """
        :param int x: x position of the widget
        :param int r_ext: dial gauge's exterior radius
        :param int r_int: dial gauge's interior radius
        :prama list range_values: value range for the widget. Defaults [0-100]
        :param int color: dial color in hex. Defaults to :const:`0x00FF00`
        """
        super().__init__(x=x, y=y, scale=1)
        palette = displayio.Palette(3)
        palette[0] = background_color
        palette[1] = color
        bitmap = displayio.Bitmap(r_ext * 2 + 3, r_ext + 3, 3)
        self.append(displayio.TileGrid(bitmap, pixel_shader=palette))
        self._rangemin = range_values[0]
        self._rangemax = range_values[1]
        if font_file is None:
            self._font_to_use = terminalio.FONT
        else:
            self._font_to_use = bitmap_font.load_font(font_file)

        x0 = r_ext
        y0 = r_ext

        self._start_angle = 180
        self._end_angle = 360
        values = np.linspace(
            self._start_angle,
            self._end_angle,
            (self._end_angle - self._start_angle),
        )
        self._linepoints1 = []
        self._linepoints2 = []
        for t in values:
            x = ceil(x0 + r_ext * cos(t * pi / 180))
            y = ceil(y0 + r_ext * sin(t * pi / 180))
            bitmap[x, y] = 1
            self._linepoints1.append((x, y))

        for t in values:
            x = ceil(x0 + r_int * cos(t * pi / 180))
            y = ceil(y0 + r_int * sin(t * pi / 180))
            bitmap[x, y] = 1
            self._linepoints2.append((x, y))

        draw_line(
            bitmap,
            self._linepoints1[-1][0],
            self._linepoints1[-1][1],
            self._linepoints2[-1][0],
            self._linepoints2[-1][1],
            1,
        )
        self._linepoints2.reverse()

        arcpoints = self._linepoints1 + self._linepoints2

        self._p = Polygon(
            pixel_shader=palette, points=arcpoints, x=0, y=0, color_index=1
        )
        self.append(self._p)

        text_ini = str(self._rangemin)
        self.text = bitmap_label.Label(self._font_to_use, text=text_ini, color=color)
        self.text.x = r_ext
        self.text.y = y - self._font_to_use.get_bounding_box()[1] // 2

        self.append(self.text)

    def update(self, value: int) -> None:
        """
        Update the gauge
        :param int value: value to be updated
        """
        t = int(
            (
                ((value - self._rangemin) * (self._end_angle - self._start_angle))
                / (self._rangemax - self._rangemin)
            )
            + self._start_angle
        )
        if t <= self._start_angle + 2:
            t = self._start_angle + 2
        index = self._end_angle - t

        self._p.points = self._linepoints1[:-index] + self._linepoints2[index:]
        self.text.text = str(value)
