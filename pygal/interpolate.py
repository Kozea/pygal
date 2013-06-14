# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2013 Kozea
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
Interpolation

TODO: Implement more interpolations (cosine, lagrange...)

"""
from __future__ import division


def quadratic_interpolate(x, y, precision=250):
    n = len(x) - 1
    delta_x = [x2 - x1 for x1, x2 in zip(x, x[1:])]
    delta_y = [y2 - y1 for y1, y2 in zip(y, y[1:])]
    slope = [delta_y[i] / delta_x[i] if delta_x[i] else 1 for i in range(n)]

    # Quadratic spline: a + bx + cx²
    a = y
    b = [0] * (n + 1)
    c = [0] * (n + 1)

    for i in range(1, n):
        b[i] = 2 * slope[i - 1] - b[i - 1]

    c = [(slope[i] - b[i]) / delta_x[i] for i in range(n)]

    for i in range(n + 1):
        yield x[i], a[i]
        if i == n or delta_x[i] == 0:
            continue
        for s in range(1, precision):
            X = s * delta_x[i] / precision
            X2 = X * X
            yield x[i] + X, a[i] + b[i] * X + c[i] * X2


def cubic_interpolate(x, y, precision=250):
    """Takes a list of (x, y) and returns an iterator over
    the natural cubic spline of points with `precision` points between them"""
    n = len(x) - 1
    # Spline equation is a + bx + cx² + dx³
    # ie: Spline part i equation is a[i] + b[i]x + c[i]x² + d[i]x³
    a = y
    b = [0] * (n + 1)
    c = [0] * (n + 1)
    d = [0] * (n + 1)
    m = [0] * (n + 1)
    z = [0] * (n + 1)

    h = [x2 - x1 for x1, x2 in zip(x, x[1:])]
    k = [a2 - a1 for a1, a2 in zip(a, a[1:])]
    g = [k[i] / h[i] if h[i] else 1 for i in range(n)]

    for i in range(1, n):
        j = i - 1
        l = 1 / (2 * (x[i + 1] - x[j]) - h[j] * m[j])
        m[i] = h[i] * l
        z[i] = (3 * (g[i] - g[j]) - h[j] * z[j]) * l

    for j in reversed(range(n)):
        if h[j] == 0:
            continue
        c[j] = z[j] - (m[j] * c[j + 1])
        b[j] = g[j] - (h[j] * (c[j + 1] + 2 * c[j])) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])

    for i in range(n + 1):
        yield x[i], a[i]
        if i == n or h[i] == 0:
            continue
        for s in range(1, precision):
            X = s * h[i] / precision
            X2 = X * X
            X3 = X2 * X
            yield x[i] + X, a[i] + b[i] * X + c[i] * X2 + d[i] * X3


if __name__ == '__main__':
    from pygal import XY
    points = [(.1, 7), (.3, -4), (.6, 10), (.9, 8), (1.4, 3), (1.7, 1)]
    xy = XY(show_dots=False)
    xy.add('normal', points)
    xy.add('quadratic', quadratic_interpolate(*zip(*points)))
    xy.add('cubic', cubic_interpolate(*zip(*points)))
    xy.render_in_browser()
