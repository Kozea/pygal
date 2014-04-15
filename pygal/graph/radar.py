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
Radar chart

"""

from __future__ import division
from pygal.graph.line import Line
from pygal.adapters import positive, none_to_zero
from pygal.view import PolarView, PolarLogView
from pygal.util import deg, cached_property, compute_scale, majorize, cut
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
        if self.logarithmic:
            view_class = PolarLogView
        else:
            view_class = PolarView

        self.view = view_class(
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
        if self.x_labels_major:
            x_labels_major = self.x_labels_major
        elif self.x_labels_major_every:
            x_labels_major = [self._x_labels[i][0] for i in range(
                0, len(self._x_labels), self.x_labels_major_every)]
        elif self.x_labels_major_count:
            label_count = len(self._x_labels)
            major_count = self.x_labels_major_count
            if (major_count >= label_count):
                x_labels_major = [label[0] for label in self._x_labels]
            else:
                x_labels_major = [self._x_labels[
                    int(i * label_count / major_count)][0]
                    for i in range(major_count)]
        else:
            x_labels_major = []

        for label, theta in self._x_labels:
            major = label in x_labels_major
            if not (self.show_minor_x_labels or major):
                continue
            guides = self.svg.node(axis, class_='guides')
            end = self.view((r, theta))
            self.svg.node(
                guides, 'path',
                d='M%s L%s' % (format_(center), format_(end)),
                class_='%sline' % ('major ' if major else ''))
            r_txt = (1 - self._box.__class__.margin) * self._box.ymax
            pos_text = self.view((r_txt, theta))
            text = self.svg.node(
                guides, 'text',
                x=pos_text[0],
                y=pos_text[1],
                class_='major' if major else '')
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

        if self.y_labels_major:
            y_labels_major = self.y_labels_major
        elif self.y_labels_major_every:
            y_labels_major = [self._y_labels[i][1] for i in range(
                0, len(self._y_labels), self.y_labels_major_every)]
        elif self.y_labels_major_count:
            label_count = len(self._y_labels)
            major_count = self.y_labels_major_count
            if (major_count >= label_count):
                y_labels_major = [label[1] for label in self._y_labels]
            else:
                y_labels_major = [self._y_labels[
                    int(i * (label_count - 1) / (major_count - 1))][1]
                    for i in range(major_count)]
        else:
            y_labels_major = majorize(
                cut(self._y_labels, 1)
            )
        for label, r in reversed(self._y_labels):
            major = r in y_labels_major
            if not (self.show_minor_y_labels or major):
                continue
            guides = self.svg.node(axis, class_='guides')
            self.svg.line(
                guides, [self.view((r, theta)) for theta in self.x_pos],
                close=True,
                class_='%sguide line' % (
                    'major ' if major else ''))
            x, y = self.view((r, self.x_pos[0]))
            self.svg.node(
                guides, 'text',
                x=x - 5,
                y=y,
                class_='major' if major else ''
            ).text = label

    def _compute(self):
        delta = 2 * pi / self._len if self._len else 0
        x_pos = [.5 * pi + i * delta for i in range(self._len + 1)]
        for serie in self.all_series:
            serie.points = [
                (v, x_pos[i])
                for i, v in enumerate(serie.values)]
            if self.interpolate:
                extended_x_pos = (
                    [.5 * pi - delta] + x_pos)
                extended_vals = (serie.values[-1:] +
                                 serie.values)
                serie.interpolated = list(
                    map(tuple,
                        map(reversed,
                            self._interpolate(
                                extended_x_pos, extended_vals))))

        # x labels space
        self._box.margin *= 2
        self._rmin = self.zero
        self._rmax = self._max or 1
        self._box.set_polar_box(self._rmin, self._rmax)

        y_pos = compute_scale(
            self._rmin, self._rmax, self.logarithmic, self.order_min,
            max_scale=8
        ) if not self.y_labels else list(map(int, self.y_labels))

        self._x_labels = self.x_labels and list(zip(self.x_labels, x_pos))
        self._y_labels = list(zip(map(self._format, y_pos), y_pos))

        self.x_pos = x_pos
        self._self_close = True
