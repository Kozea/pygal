# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2015 Kozea
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
Interpolation functions

These functions takes two lists of points x and y and
returns an iterator over the interpolation between all these points
with `precision` interpolated points between each of them

"""
from __future__ import division

from math import sin


def quadratic_interpolate(x, y, precision=250, **kwargs):
    """
    Interpolate x, y using a quadratic algorithm
    https://en.wikipedia.org/wiki/Spline_(mathematics)
    """
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

    c = [(slope[i] - b[i]) / delta_x[i] if delta_x[i] else 0 for i in range(n)]

    for i in range(n + 1):
        yield x[i], a[i]
        if i == n or delta_x[i] == 0:
            continue
        for s in range(1, precision):
            X = s * delta_x[i] / precision
            X2 = X * X
            yield x[i] + X, a[i] + b[i] * X + c[i] * X2


def cubic_interpolate(x, y, precision=250, **kwargs):
    """
    Interpolate x, y using a cubic algorithm
    https://en.wikipedia.org/wiki/Spline_interpolation
    """
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
        l = 1 / (2 * (x[i + 1] - x[j]) - h[j] * m[j]) if x[i + 1] - x[j] else 0
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


def hermite_interpolate(x, y, precision=250,
                        type='cardinal', c=None, b=None, t=None):
    """
    Interpolate x, y using the hermite method.
    See https://en.wikipedia.org/wiki/Cubic_Hermite_spline

    This interpolation is configurable and contain 4 subtypes:
      * Catmull Rom
      * Finite Difference
      * Cardinal
      * Kochanek Bartels

    The cardinal subtype is customizable with a parameter:
      * c: tension (0, 1)

    This last type is also customizable using 3 parameters:
      * c: continuity (-1, 1)
      * b: bias       (-1, 1)
      * t: tension    (-1, 1)

    """
    n = len(x) - 1
    m = [1] * (n + 1)
    w = [1] * (n + 1)
    delta_x = [x2 - x1 for x1, x2 in zip(x, x[1:])]
    if type == 'catmull_rom':
        type = 'cardinal'
        c = 0
    if type == 'finite_difference':
        for i in range(1, n):
            m[i] = w[i] = .5 * (
                (y[i + 1] - y[i]) / (x[i + 1] - x[i]) +
                (y[i] - y[i - 1]) / (
                    x[i] - x[i - 1])
            ) if x[i + 1] - x[i] and x[i] - x[i - 1] else 0

    elif type == 'kochanek_bartels':
        c = c or 0
        b = b or 0
        t = t or 0
        for i in range(1, n):
            m[i] = .5 * ((1 - t) * (1 + b) * (1 + c) * (y[i] - y[i - 1]) +
                         (1 - t) * (1 - b) * (1 - c) * (y[i + 1] - y[i]))
            w[i] = .5 * ((1 - t) * (1 + b) * (1 - c) * (y[i] - y[i - 1]) +
                         (1 - t) * (1 - b) * (1 + c) * (y[i + 1] - y[i]))

    if type == 'cardinal':
        c = c or 0
        for i in range(1, n):
            m[i] = w[i] = (1 - c) * (
                y[i + 1] - y[i - 1]) / (
                    x[i + 1] - x[i - 1]) if x[i + 1] - x[i - 1] else 0

    def p(i, x_):
        t = (x_ - x[i]) / delta_x[i]
        t2 = t * t
        t3 = t2 * t

        h00 = 2 * t3 - 3 * t2 + 1
        h10 = t3 - 2 * t2 + t
        h01 = - 2 * t3 + 3 * t2
        h11 = t3 - t2

        return (h00 * y[i] +
                h10 * m[i] * delta_x[i] +
                h01 * y[i + 1] +
                h11 * w[i + 1] * delta_x[i])

    for i in range(n + 1):
        yield x[i], y[i]
        if i == n or delta_x[i] == 0:
            continue
        for s in range(1, precision):
            X = x[i] + s * delta_x[i] / precision
            yield X, p(i, X)


def lagrange_interpolate(x, y, precision=250, **kwargs):
    """
    Interpolate x, y using Lagrange polynomials
    https://en.wikipedia.org/wiki/Lagrange_polynomial
    """
    n = len(x) - 1
    delta_x = [x2 - x1 for x1, x2 in zip(x, x[1:])]
    for i in range(n + 1):
        yield x[i], y[i]
        if i == n or delta_x[i] == 0:
            continue

        for s in range(1, precision):
            X = x[i] + s * delta_x[i] / precision
            s = 0
            for k in range(n + 1):
                p = 1
                for m in range(n + 1):
                    if m == k:
                        continue
                    if x[k] - x[m]:
                        p *= (X - x[m]) / (x[k] - x[m])
                s += y[k] * p
            yield X, s


def trigonometric_interpolate(x, y, precision=250, **kwargs):
    """
    Interpolate x, y using trigonometric
    As per http://en.wikipedia.org/wiki/Trigonometric_interpolation
    """
    n = len(x) - 1
    delta_x = [x2 - x1 for x1, x2 in zip(x, x[1:])]
    for i in range(n + 1):
        yield x[i], y[i]
        if i == n or delta_x[i] == 0:
            continue

        for s in range(1, precision):
            X = x[i] + s * delta_x[i] / precision
            s = 0
            for k in range(n + 1):
                p = 1
                for m in range(n + 1):
                    if m == k:
                        continue
                    if sin(0.5 * (x[k] - x[m])):
                        p *= sin(0.5 * (X - x[m])) / sin(0.5 * (x[k] - x[m]))
                s += y[k] * p
            yield X, s

INTERPOLATIONS = {
    'quadratic': quadratic_interpolate,
    'cubic': cubic_interpolate,
    'hermite': hermite_interpolate,
    'lagrange': lagrange_interpolate,
    'trigonometric': trigonometric_interpolate
}


if __name__ == '__main__':
    from pygal import XY
    points = [(.1, 7), (.3, -4), (.6, 10), (.9, 8), (1.4, 3), (1.7, 1)]
    xy = XY(show_dots=False)
    xy.add('normal', points)
    xy.add('quadratic', quadratic_interpolate(*zip(*points)))
    xy.add('cubic', cubic_interpolate(*zip(*points)))
    xy.add('lagrange', lagrange_interpolate(*zip(*points)))
    xy.add('trigonometric', trigonometric_interpolate(*zip(*points)))
    xy.add('hermite catmul_rom', hermite_interpolate(
        *zip(*points), type='catmul_rom'))
    xy.add('hermite finite_difference', hermite_interpolate(
        *zip(*points), type='finite_difference'))
    xy.add('hermite cardinal -.5', hermite_interpolate(
        *zip(*points), type='cardinal', c=-.5))
    xy.add('hermite cardinal .5', hermite_interpolate(
        *zip(*points), type='cardinal', c=.5))
    xy.add('hermite kochanek_bartels .5 .75 -.25', hermite_interpolate(
        *zip(*points), type='kochanek_bartels', c=.5, b=.75, t=-.25))
    xy.add('hermite kochanek_bartels .25 -.75 .5', hermite_interpolate(
        *zip(*points), type='kochanek_bartels', c=.25, b=-.75, t=.5))
    xy.render_in_browser()
