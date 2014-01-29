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
Box plot
"""

from __future__ import division
from pygal.graph.graph import Graph
from pygal.util import compute_scale, decorate
from math import floor


class Box(Graph):
    """
    Box plot
    For each series, shows the median value, the 25th and 75th percentiles, and the values within
    1.5 times the interquartile range of the 25th and 75th percentiles.

    See http://en.wikipedia.org/wiki/Box_plot
    """
    _series_margin = .06

    def __init__(self, *args, **kwargs):
        super(Box, self).__init__(*args, **kwargs)

    def _compute(self):
        """
        Compute parameters necessary for later steps within the rendering process
        """
        # Note: this code was copied from Bar graph
        if self._min:
            self._box.ymin = min(self._min, self.zero)
        if self._max:
            self._box.ymax = max(self._max, self.zero)

        x_pos = [
            x / self._len for x in range(self._len + 1)
        ] if self._len > 1 else [0, 1]  # Center if only one value

        self._points(x_pos)

        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min
        ) if not self.y_labels else map(float, self.y_labels)

        self._x_labels = self.x_labels and list(zip(self.x_labels, [
            (i + .5) / self._len for i in range(self._len)]))
        self._y_labels = list(zip(map(self._format, y_pos), y_pos))

    def _plot(self):
        """
        Plot the series data
        """
        for index, serie in enumerate(self.series):
            self._boxf(self._serie(index), serie, index)

    def _boxf(self, serie_node, serie, index):
        """
        For a specific series, draw the box plot.
        """
        # Note: q0 and q4 do not literally mean the zero-th quartile and the fourth quartile, but rather
        # the distance from 1.5 times the inter-quartile range to Q1 and Q3, respectively.
        q0, q1, q2, q3, q4 = self._box_points(serie.values)
        boxes = self.svg.node(serie_node['plot'], class_="boxes")

        metadata = serie.metadata.get(0)

        box = decorate(
            self.svg,
            self.svg.node(boxes, class_='box'),
            metadata)
        val = self._format(q2)

        x_center, y_center = self._draw_box(box, (q0, q1, q2, q3, q4), index)
        self._tooltip_data(box, val, x_center, y_center, classes="centered")
        #print(val)
        #self._static_value(box, val, x_center, y_center)

    def _draw_box(self, parent_node, quartiles, box_index):
        """
        Return the center of a bounding box defined by a box plot. Draws a box plot on self.svg.
        """
        width = (self.view.x(1) - self.view.x(0)) / self._len
        #x, y = self.view((x, y))
        series_margin = width * self._series_margin
        #x += series_margin
        width -= 2 * series_margin
        #height = self.view.y(y_zero) - y
        left_edge = self.view.x(0) + width * box_index

        # draw lines for whiskers - bottom, median, and top
        for whisker in (quartiles[0], quartiles[2], quartiles[4]):
            self.svg.line(parent_node,
                          coords=[(left_edge, self.view.y(whisker)), (left_edge + width, self.view.y(whisker))],
                          attrib={'stroke-width': 3})

        # box, bounded by Q1 and Q3
        self.svg.node(parent_node,
                      tag='rect',
                      x=left_edge,
                      y=self.view.y(quartiles[1]),
                      height=self.view.y(quartiles[3]) - self.view.y(quartiles[1]),
                      width=width,
                      attrib={'fill-opacity': 0.25})

        return (left_edge + width / 2, self.view.height / 2)

    @staticmethod
    def _box_points(values):
        """
        Return a 5-tuple of Q1 - 1.5 * IQR, Q1, Median, Q3, and Q3 + 1.5 * IQR for a list of numeric values.

        The iterator values may include None values.

        Uses quartile definition from  Mendenhall, W. and Sincich, T. L. Statistics for Engineering and the
        Sciences, 4th ed. Prentice-Hall, 1995.
        """
        def median(seq):
            n = len(seq)
            if n % 2 == 0:  # seq has an even length
                return (seq[n // 2] + s[n // 2 - 1]) / 2
            else:  # seq has an odd length
                return seq[n // 2]

        # sort the copy in case the originals must stay in original order
        s = sorted([x for x in values if x is not None])
        n = len(s)
        if not n:
            return 0, 0, 0, 0, 0
        else:
            q2 = median(s)
            # See 'Method 3' in http://en.wikipedia.org/wiki/Quartile
            if n % 2 == 0:  # even
                q1 = median(s[:n // 2])
                q3 = median(s[n // 2:])
            else:  # odd
                if n == 1:  # special case
                    q1 = s[0]
                    q3 = s[0]
                elif n % 4 == 1:  # n is of form 4n + 1 where n >= 1
                    m = (n - 1) // 4
                    q1 = 0.25 * s[m-1] + 0.75 * s[m]
                    q3 = 0.75 * s[3*m] + 0.25 * s[3*m + 1]
                else:  # n is of form 4n + 3 where n >= 1
                    m = (n - 3) // 4
                    q1 = 0.75 * s[m] + 0.25 * s[m+1]
                    q3 = 0.25 * s[3*m+1] + 0.75 * s[3*m+2]

            iqr = q3 - q1
            q0 = q1 - 1.5 * iqr
            q4 = q3 + 1.5 * iqr
            return q0, q1, q2, q3, q4
