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
        return  [
            val[1]
            for serie in self.series
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
            points = list ((x, self._scale_diff+(y - self._scale_min_2nd) * self._scale) for x, y in serie.points)
        else:
            points = serie.points
        view_values = map(self.view, points)
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
                self._tooltip_data(dots, 
                        "%s: %s" % (self.x_labels[i], val) if self.x_labels and 
                                                self.x_labels_num_limit 
                                                else val, 
                        x, y)
                self._static_value(
                    serie_node, val,
                    x + self.value_font_size,
                    y + self.value_font_size)

        if self.stroke:
            if self.interpolate:
                view_values = map(self.view, serie.interpolated)
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

        x_labels = zip(self.x_labels, x_pos)

        if self.x_labels_num_limit and len(x_labels)>self.x_labels_num_limit:
            step = (len(x_labels)-1)/(self.x_labels_num_limit-1)
            x_labels = list(x_labels[int(i*step)] for i in range(self.x_labels_num_limit))

        self._x_labels = self.x_labels and x_labels
        # Y Label

        if self.include_x_axis:
            self._box.ymin = min(self._min, 0)
            self._box.ymax = max(self._max, 0)
        else:
            self._box.ymin = self._min
            self._box.ymax = self._max

        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min
        ) if not self.y_labels else map(float, self.y_labels)

        self._y_labels = zip(map(self._format, y_pos), y_pos)
        # secondary y axis support
        if self.secondary_series:
            if self.include_x_axis:
                ymin = min(self._secondary_min, 0)
                ymax = max(self._secondary_max, 0)
            else:
                ymin = self._secondary_min
                ymax = self._secondary_max
            steps = len(y_pos)
            left_range = abs(y_pos[-1] -  y_pos[0])
            right_range = abs(ymax - ymin)
            scale = right_range / (steps-1)
            self._y_2nd_labels = list((self._format(ymin+i*scale), pos) for i, pos in enumerate(y_pos))

            min_2nd = float(self._y_2nd_labels[0][0])
            self._scale = left_range / right_range
            self._scale_diff = y_pos[0]
            self._scale_min_2nd = min_2nd

    def _plot(self):
        for index, serie in enumerate(self.series):
            self.line(self._serie(index), serie)
        for index, serie in enumerate(self.secondary_series, len(self.series)):
            self.line(self._serie(index), serie, True)
