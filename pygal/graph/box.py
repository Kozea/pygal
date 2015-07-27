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
Box plot: a convenient way to display series as box with whiskers and outliers
Different types are available throught the box_mode option
"""

from __future__ import division

from bisect import bisect_left, bisect_right

from pygal._compat import is_list_like
from pygal.graph.graph import Graph
from pygal.util import alter, decorate


class Box(Graph):

    """
    Box plot
    For each series, shows the median value, the 25th and 75th percentiles,
    and the values within
    1.5 times the interquartile range of the 25th and 75th percentiles.

    See http://en.wikipedia.org/wiki/Box_plot
    """

    _series_margin = .06

    @property
    def _format(self):
        """Return the value formatter for this graph"""
        sup = super(Box, self)._format

        def format_maybe_quartile(x):
            if is_list_like(x):
                if self.box_mode == "extremes":
                    return (
                        'Min: %s\nQ1 : %s\nQ2 : %s\nQ3 : %s\nMax: %s' %
                        tuple(map(sup, x[1:6])))
                elif self.box_mode in ["tukey", "stdev", "pstdev"]:
                    return (
                        'Min: %s\nLower Whisker: %s\nQ1: %s\nQ2: %s\nQ3: %s\n'
                        'Upper Whisker: %s\nMax: %s' % tuple(map(sup, x)))
                elif self.box_mode == '1.5IQR':
                    # 1.5IQR mode
                    return 'Q1: %s\nQ2: %s\nQ3: %s' % tuple(map(sup, x[2:5]))
            else:
                return sup(x)
        return format_maybe_quartile

    def _compute(self):
        """
        Compute parameters necessary for later steps
        within the rendering process
        """
        for serie in self.series:
            serie.values, serie.outliers = \
                self._box_points(serie.values, self.box_mode)

        self._x_pos = [
            (i + .5) / self._order for i in range(self._order)]

        if self._min:
            self._box.ymin = min(self._min, self.zero)
        if self._max:
            self._box.ymax = max(self._max, self.zero)

    def _plot(self):
        """Plot the series data"""
        for serie in self.series:
            self._boxf(serie)

    @property
    def _len(self):
        """Len is always 7 here"""
        return 7

    def _boxf(self, serie):
        """For a specific series, draw the box plot."""
        serie_node = self.svg.serie(serie)
        # Note: q0 and q4 do not literally mean the zero-th quartile
        # and the fourth quartile, but rather the distance from 1.5 times
        # the inter-quartile range to Q1 and Q3, respectively.
        boxes = self.svg.node(serie_node['plot'], class_="boxes")

        metadata = serie.metadata.get(0)

        box = decorate(
            self.svg,
            self.svg.node(boxes, class_='box'),
            metadata)
        val = self._format(serie.values)

        x_center, y_center = self._draw_box(
            box, serie.values[1:6], serie.outliers, serie.index, metadata)
        self._tooltip_data(box, val, x_center, y_center, "centered",
                           self._get_x_label(serie.index))
        self._static_value(serie_node, val, x_center, y_center, metadata)

    def _draw_box(self, parent_node, quartiles, outliers, box_index, metadata):
        """
        Return the center of a bounding box defined by a box plot.
        Draws a box plot on self.svg.
        """
        width = (self.view.x(1) - self.view.x(0)) / self._order
        series_margin = width * self._series_margin
        left_edge = self.view.x(0) + width * box_index + series_margin
        width -= 2 * series_margin

        # draw lines for whiskers - bottom, median, and top
        for i, whisker in enumerate(
                (quartiles[0], quartiles[2], quartiles[4])):
            whisker_width = width if i == 1 else width / 2
            shift = (width - whisker_width) / 2
            xs = left_edge + shift
            xe = left_edge + width - shift
            alter(self.svg.line(
                parent_node,
                coords=[(xs, self.view.y(whisker)),
                        (xe, self.view.y(whisker))],
                class_='reactive tooltip-trigger',
                attrib={'stroke-width': 3}), metadata)

        # draw lines connecting whiskers to box (Q1 and Q3)
        alter(self.svg.line(
            parent_node,
            coords=[(left_edge + width / 2, self.view.y(quartiles[0])),
                    (left_edge + width / 2, self.view.y(quartiles[1]))],
            class_='reactive tooltip-trigger',
            attrib={'stroke-width': 2}), metadata)
        alter(self.svg.line(
            parent_node,
            coords=[(left_edge + width / 2, self.view.y(quartiles[4])),
                    (left_edge + width / 2, self.view.y(quartiles[3]))],
            class_='reactive tooltip-trigger',
            attrib={'stroke-width': 2}), metadata)

        # box, bounded by Q1 and Q3
        alter(self.svg.node(
            parent_node,
            tag='rect',
            x=left_edge,
            y=self.view.y(quartiles[1]),
            height=self.view.y(quartiles[3]) - self.view.y(quartiles[1]),
            width=width,
            class_='subtle-fill reactive tooltip-trigger'), metadata)

        # draw outliers
        for o in outliers:
            alter(self.svg.node(
                parent_node,
                tag='circle',
                cx=left_edge+width/2,
                cy=self.view.y(o),
                r=3,
                class_='subtle-fill reactive tooltip-trigger'), metadata)

        return (left_edge + width / 2, self.view.y(
            sum(quartiles) / len(quartiles)))

    @staticmethod
    def _box_points(values, mode='extremes'):
        """
        Default mode: (mode='extremes' or unset)
            Return a 7-tuple of 2x minimum, Q1, Median, Q3,
        and 2x maximum for a list of numeric values.
        1.5IQR mode: (mode='1.5IQR')
            Return a 7-tuple of min, Q1 - 1.5 * IQR, Q1, Median, Q3,
        Q3 + 1.5 * IQR and max for a list of numeric values.
        Tukey mode: (mode='tukey')
            Return a 7-tuple of min, q[0..4], max and a list of outliers
        Outliers are considered values x: x < q1 - IQR or x > q3 + IQR
        SD mode: (mode='stdev')
            Return a 7-tuple of min, q[0..4], max and a list of outliers
        Outliers are considered values x: x < q2 - SD or x > q2 + SD
        SDp mode: (mode='pstdev')
            Return a 7-tuple of min, q[0..4], max and a list of outliers
        Outliers are considered values x: x < q2 - SDp or x > q2 + SDp

        The iterator values may include None values.

        Uses quartile definition from  Mendenhall, W. and
        Sincich, T. L. Statistics for Engineering and the
        Sciences, 4th ed. Prentice-Hall, 1995.
        """
        def median(seq):
            n = len(seq)
            if n % 2 == 0:  # seq has an even length
                return (seq[n // 2] + seq[n // 2 - 1]) / 2
            else:  # seq has an odd length
                return seq[n // 2]

        def mean(seq):
            return sum(seq) / len(seq)

        def stdev(seq):
            m = mean(seq)
            l = len(seq)
            v = sum((n - m)**2 for n in seq) / (l - 1)  # variance
            return v**0.5  # sqrt

        def pstdev(seq):
            m = mean(seq)
            l = len(seq)
            v = sum((n - m)**2 for n in seq) / l  # variance
            return v**0.5  # sqrt

        outliers = []
        # sort the copy in case the originals must stay in original order
        s = sorted([x for x in values if x is not None])
        n = len(s)
        if not n:
            return (0, 0, 0, 0, 0, 0, 0), []
        elif n == 1:
            return (s[0], s[0], s[0], s[0], s[0], s[0], s[0]), []
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
                    q3 = 0.75 * s[3*m] + 0.25 * s[3*m+1]
                else:  # n is of form 4n + 3 where n >= 1
                    m = (n - 3) // 4
                    q1 = 0.75 * s[m] + 0.25 * s[m+1]
                    q3 = 0.25 * s[3*m+1] + 0.75 * s[3*m+2]

            iqr = q3 - q1
            min_s = s[0]
            max_s = s[-1]
            if mode == 'extremes':
                q0 = min_s
                q4 = max_s
            elif mode == 'tukey':
                # the lowest datum still within 1.5 IQR of the lower quartile,
                # and the highest datum still within 1.5 IQR of the upper
                # quartile [Tukey box plot, Wikipedia ]
                b0 = bisect_left(s, q1 - 1.5 * iqr)
                b4 = bisect_right(s, q3 + 1.5 * iqr)
                q0 = s[b0]
                q4 = s[b4-1]
                outliers = s[:b0] + s[b4:]
            elif mode == 'stdev':
                # one standard deviation above and below the mean of the data
                sd = stdev(s)
                b0 = bisect_left(s, q2 - sd)
                b4 = bisect_right(s, q2 + sd)
                q0 = s[b0]
                q4 = s[b4-1]
                outliers = s[:b0] + s[b4:]
            elif mode == 'pstdev':
                # one population standard deviation above and below
                # the mean of the data
                sdp = pstdev(s)
                b0 = bisect_left(s, q2 - sdp)
                b4 = bisect_right(s, q2 + sdp)
                q0 = s[b0]
                q4 = s[b4-1]
                outliers = s[:b0] + s[b4:]
            elif mode == '1.5IQR':
                # 1.5IQR mode
                q0 = q1 - 1.5 * iqr
                q4 = q3 + 1.5 * iqr
            return (min_s, q0, q1, q2, q3, q4, max_s), outliers
