# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
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
Radar chart

"""

from __future__ import division
from pygal.graph.line import Line
from pygal.adapters import positive, none_to_zero
from pygal.view import PolarView
from pygal.util import deg, cached_property, compute_scale
from math import cos, pi


class Radar(Line):
    """Kiviat graph"""

    _adapters = [positive, none_to_zero]

    def __init__(self, *args, **kwargs):
        self.x_pos = None
        self._rmax = None
        super(Radar, self).__init__(*args, **kwargs)

    def _fill(self, values):
        return values

    def _get_value(self, values, i):
        return self._format(values[i][0])

    @cached_property
    def _values(self):
        if self.interpolate:
            return [val[0] for serie in self.series
                    for val in serie.interpolated]
        else:
            return super(Line, self)._values

    def _set_view(self):
        self.view = PolarView(
            self.width - self.margin.x,
            self.height - self.margin.y,
            self._box)

    def _x_axis(self, draw_axes=True):
        if not self._x_labels:
            return

        axis = self.svg.node(self.nodes['plot'], class_="axis x web")
        format_ = lambda x: '%f %f' % x
        center = self.view((0, 0))
        r = self._rmax
        for label, theta in self._x_labels:
            guides = self.svg.node(axis, class_='guides')
            end = self.view((r, theta))
            self.svg.node(
                guides, 'path',
                d='M%s L%s' % (format_(center), format_(end)),
                class_='line')
            r_txt = (1 - self._box.__class__.margin) * self._box.ymax
            pos_text = self.view((r_txt, theta))
            text = self.svg.node(
                guides, 'text',
                x=pos_text[0],
                y=pos_text[1])
            text.text = label
            angle = - theta + pi / 2
            if cos(angle) < 0:
                angle -= pi
            text.attrib['transform'] = 'rotate(%f %s)' % (
                deg(angle), format_(pos_text))

    def _y_axis(self, draw_axes=True):
        if not self._y_labels:
            return

        axis = self.svg.node(self.nodes['plot'], class_="axis y web")

        for label, r in reversed(self._y_labels):
            guides = self.svg.node(axis, class_='guides')
            self.svg.line(
                guides, [self.view((r, theta)) for theta in self.x_pos],
                close=True,
                class_='guide line')
            x, y = self.view((r, self.x_pos[0]))
            self.svg.node(
                guides, 'text',
                x=x - 5,
                y=y).text = label

    def _compute(self):
        delta = 2 * pi / self._len
        x_pos = [.5 * pi + i * delta for i in range(self._len + 1)]
        for serie in self.series:
            serie.points = [
                (v, x_pos[i])
                for i, v in enumerate(serie.values)]
            if self.interpolate:
                extend = 2
                extended_x_pos = (
                    [.5 * pi + i * delta for i in range(-extend, 0)] +
                    x_pos +
                    [.5 * pi + i * delta for i in range(
                        self._len + 1, self._len + 1 + extend)])
                extended_vals = (serie.values[-extend:] +
                                 serie.values +
                                 serie.values[:extend])
                serie.interpolated = self._interpolate(
                    extended_vals, extended_x_pos, polar=True)

        self._box.margin *= 2
        self._box.xmin = self._box.ymin = - self._max
        self._box.xmax = self._box.ymax = self._rmax = self._max

        y_pos = compute_scale(
            0, self._box.ymax, self.logarithmic, self.order_min, max_scale=8
        ) if not self.y_labels else map(int, self.y_labels)
        self._x_labels = self.x_labels and zip(self.x_labels, x_pos)
        self._y_labels = zip(map(self._format, y_pos), y_pos)

        self.x_pos = x_pos
        self._self_close = True
