# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2014 Kozea
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
Color utils

"""
from __future__ import division


def normalize_float(f):
    if abs(f - round(f)) < .0000000000001:
        return round(f)
    return f


def rgb_to_hsl(r, g, b):
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


def adjust(color, attribute, percent):
    assert color[0] == '#', '#rrggbb and #rgb format are supported'
    color = color[1:]
    assert len(color) in (3, 6), '#rrggbb and #rgb format are supported'
    if len(color) == 3:
        color = [a for b in zip(color, color) for a in b]

    bound = lambda x: max(0, min(100, x))

    def _adjust(hsl):
        hsl = list(hsl)
        if attribute > 0:
            hsl[attribute] = bound(hsl[attribute] + percent)
        else:
            hsl[attribute] += percent

        return hsl
    return '#%02x%02x%02x' % hsl_to_rgb(
        *_adjust(
            rgb_to_hsl(*map(lambda x: int(''.join(x), 16),
                            zip(color[::2], color[1::2])))))


def rotate(color, percent):
    return adjust(color, 0, percent)


def saturate(color, percent):
    return adjust(color, 1, percent)


def desaturate(color, percent):
    return adjust(color, 1, -percent)


def lighten(color, percent):
    return adjust(color, 2, percent)


def darken(color, percent):
    return adjust(color, 2, -percent)
