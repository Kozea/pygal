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
Line chart

"""
from __future__ import division
from pygal.graph.graph import Graph
from pygal.util import cached_property, compute_scale, decorate


class Line(Graph):
    """Line graph"""

    def __init__(self, *args, **kwargs):
        self._self_close = False
        super(Line, self).__init__(*args, **kwargs)

    @cached_property
    def _values(self):
        return [
            val[1]
            for serie in self.series
            for val in (serie.interpolated
                        if self.interpolate else serie.points)
            if val[1] is not None and (not self.logarithmic or val[1] > 0)]

    @cached_property
    def _secondary_values(self):
        return [
            val[1]
            for serie in self.secondary_series
            for val in (serie.interpolated
                        if self.interpolate else serie.points)
            if val[1] is not None and (not self.logarithmic or val[1] > 0)]

    def _fill(self, values):
        """Add extra values to fill the line"""
        zero = self.view.y(min(max(self.zero, self._box.ymin), self._box.ymax))
        return ([(values[0][0], zero)] +
                values +
                [(values[-1][0], zero)])

    def line(self, serie_node, serie, rescale=False):
        """Draw the line serie"""
        if rescale and self.secondary_series:
            points = [
                (x, self._scale_diff + (y - self._scale_min_2nd) * self._scale)
                for x, y in serie.points if y is not None]
        else:
            points = serie.points
        view_values = list(map(self.view, points))
        if self.show_dots:
            for i, (x, y) in enumerate(view_values):
                if None in (x, y):
                    continue

                metadata = serie.metadata.get(i)
                classes = []
                if x > self.view.width / 2:
                    classes.append('left')
                if y > self.view.height / 2:
                    classes.append('top')
                classes = ' '.join(classes)
                dots = decorate(
                    self.svg,
                    self.svg.node(serie_node['overlay'], class_="dots"),
                    metadata)
                val = self._get_value(serie.points, i)
                self.svg.node(dots, 'circle', cx=x, cy=y, r=self.dots_size,
                              class_='dot reactive tooltip-trigger')
                self._tooltip_data(
                    dots, val, x, y)
                self._static_value(
                    serie_node, val,
                    x + self.value_font_size,
                    y + self.value_font_size)

        if self.stroke:
            if self.interpolate:
                view_values = list(map(self.view, serie.interpolated))
            if self.fill:
                view_values = self._fill(view_values)
            self.svg.line(
                serie_node['plot'], view_values, close=self._self_close,
                class_='line reactive' + (' nofill' if not self.fill else ''))

    def _compute(self):
        # X Labels
        x_pos = [
            x / (self._len - 1) for x in range(self._len)
        ] if self._len != 1 else [.5]  # Center if only one value

        self._points(x_pos)

        if self.x_labels:
            label_len = len(self.x_labels)
            if label_len != self._len:
                label_pos = [0.5] if label_len == 1 else [
                    x / (label_len - 1) for x in range(label_len)
                ]
                self._x_labels = list(zip(self.x_labels, label_pos))
            else:
                self._x_labels = list(zip(self.x_labels, x_pos))
        else:
            self._x_labels = None

        if self.include_x_axis:
        # Y Label
            self._box.ymin = min(self._min or 0, 0)
            self._box.ymax = max(self._max or 0, 0)
        else:
            self._box.ymin = self._min
            self._box.ymax = self._max

        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min
        ) if not self.y_labels else map(float, self.y_labels)

        self._y_labels = list(zip(map(self._format, y_pos), y_pos))

    def _plot(self):
        for index, serie in enumerate(self.series):
            self.line(self._serie(index), serie)

        for index, serie in enumerate(self.secondary_series, len(self.series)):
            self.line(self._serie(index), serie, True)
