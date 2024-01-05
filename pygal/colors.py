# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2016 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
"""
This package is an utility package oriented on color alteration.
This is used by the :py:mod:`pygal.style` package to generate
parametric styles.

"""
from __future__ import division


def normalize_float(f):
    """Round float errors"""
    if abs(f - round(f)) < .0000000000001:
        return round(f)
    return f


def rgb_to_hsl(r, g, b):
    """Convert a color in r, g, b to a color in h, s, l"""
    r = r or 0
    g = g or 0
    b = b or 0
    r /= 255
    g /= 255
    b /= 255
    max_ = max((r, g, b))
    min_ = min((r, g, b))
    d = max_ - min_

    if not d:
        h = 0
    elif r is max_:
        h = 60 * (g - b) / d
    elif g is max_:
        h = 60 * (b - r) / d + 120
    else:
        h = 60 * (r - g) / d + 240

    l = .5 * (max_ + min_)
    if not d:
        s = 0
    elif l < 0.5:
        s = .5 * d / l
    else:
        s = .5 * d / (1 - l)
    return tuple(map(normalize_float, (h % 360, s * 100, l * 100)))


def hsl_to_rgb(h, s, l):
    """Convert a color in h, s, l to a color in r, g, b"""
    h /= 360
    s /= 100
    l /= 100

    m2 = l * (s + 1) if l <= .5 else l + s - l * s
    m1 = 2 * l - m2

    def h_to_rgb(h):
        h = h % 1
        if 6 * h < 1:
            return m1 + 6 * h * (m2 - m1)
        if 2 * h < 1:
            return m2
        if 3 * h < 2:
            return m1 + 6 * (2 / 3 - h) * (m2 - m1)
        return m1
    r, g, b = map(lambda x: round(x * 255),
                  map(h_to_rgb, (h + 1 / 3, h, h - 1 / 3)))

    return r, g, b


def parse_color(color):
    """Take any css color definition and give back a tuple containing the
    r, g, b, a values along with a type which can be: #rgb, #rgba, #rrggbb,
    #rrggbbaa, rgb, rgba
    """
    r = g = b = a = type = None
    if color.startswith('#'):
        color = color[1:]
        if len(color) == 3:
            type = '#rgb'
            color = color + 'f'
        if len(color) == 4:
            type = type or '#rgba'
            color = ''.join([c * 2 for c in color])
        if len(color) == 6:
            type = type or '#rrggbb'
            color = color + 'ff'
        assert len(color) == 8
        type = type or '#rrggbbaa'
        r, g, b, a = [
            int(''.join(c), 16) for c in zip(color[::2], color[1::2])]
        a /= 255
    elif color.startswith('rgb('):
        type = 'rgb'
        color = color[4:-1]
        r, g, b, a = [int(c) for c in color.split(',')] + [1]
    elif color.startswith('rgba('):
        type = 'rgba'
        color = color[5:-1]
        r, g, b, a = [int(c) for c in color.split(',')[:-1]] + [
            float(color.split(',')[-1])]
    return r, g, b, a, type


def unparse_color(r, g, b, a, type):
    """
    Take the r, g, b, a color values and give back
    a type css color string. This is the inverse function of parse_color
    """
    if type == '#rgb':
        # Don't lose precision on rgb shortcut
        if r % 17 == 0 and g % 17 == 0 and b % 17 == 0:
            return '#%x%x%x' % (int(r / 17), int(g / 17), int(b / 17))
        type = '#rrggbb'

    if type == '#rgba':
        if r % 17 == 0 and g % 17 == 0 and b % 17 == 0:
            return '#%x%x%x%x' % (int(r / 17), int(g / 17), int(b / 17),
                                  int(a * 15))
        type = '#rrggbbaa'

    if type == '#rrggbb':
        return '#%02x%02x%02x' % (r, g, b)

    if type == '#rrggbbaa':
        return '#%02x%02x%02x%02x' % (r, g, b, int(a * 255))

    if type == 'rgb':
        return 'rgb(%d, %d, %d)' % (r, g, b)

    if type == 'rgba':
        return 'rgba(%d, %d, %d, %g)' % (r, g, b, a)


def is_foreground_light(color):
    """
    Determine if the background color need a light or dark foreground color
    """
    return rgb_to_hsl(*parse_color(color)[:3])[2] < 17.9


_clamp = lambda x: max(0, min(100, x))


def _adjust(hsl, attribute, percent):
    """Internal adjust function"""
    hsl = list(hsl)
    if attribute > 0:
        hsl[attribute] = _clamp(hsl[attribute] + percent)
    else:
        hsl[attribute] += percent

    return hsl


def adjust(color, attribute, percent):
    """Adjust an attribute of color by a percent"""
    r, g, b, a, type = parse_color(color)
    r, g, b = hsl_to_rgb(*_adjust(rgb_to_hsl(r, g, b), attribute, percent))
    return unparse_color(r, g, b, a, type)


def rotate(color, percent):
    """Rotate a color by changing its hue value by percent"""
    return adjust(color, 0, percent)


def saturate(color, percent):
    """Saturate a color by increasing its saturation by percent"""
    return adjust(color, 1, percent)


def desaturate(color, percent):
    """Desaturate a color by decreasing its saturation by percent"""
    return adjust(color, 1, -percent)


def lighten(color, percent):
    """Lighten a color by increasing its lightness by percent"""
    return adjust(color, 2, percent)


def darken(color, percent):
    """Darken a color by decreasing its lightness by percent"""
    return adjust(color, 2, -percent)
