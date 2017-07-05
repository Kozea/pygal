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
Line chart: Display series of data as markers (dots)
connected by straight segments
"""

from __future__ import division

from pygal.graph.graph import Graph
from pygal.util import alter, cached_property, decorate


class Line(Graph):

    """Line graph class"""

    def __init__(self, *args, **kwargs):
        """Set _self_close as False, it's True for Radar like Line"""
        self._self_close = False
        super(Line, self).__init__(*args, **kwargs)

    @cached_property
    def _values(self):
        """Getter for series values (flattened)"""
        return [
            val[1]
            for serie in self.series
            for val in (serie.interpolated
                        if self.interpolate else serie.points)
            if val[1] is not None and (not self.logarithmic or val[1] > 0)]

    @cached_property
    def _secondary_values(self):
        """Getter for secondary series values (flattened)"""
        return [
            val[1]
            for serie in self.secondary_series
            for val in (serie.interpolated
                        if self.interpolate else serie.points)
            if val[1] is not None and (not self.logarithmic or val[1] > 0)]

    def _fill(self, values):
        """Add extra values to fill the line"""
        zero = self.view.y(min(max(self.zero, self._box.ymin), self._box.ymax))

        # Check to see if the data has been padded with "none's"
        # Fill doesn't work correctly otherwise
        end = len(values) - 1
        while end > 0:
            x, y = values[end]
            if self.missing_value_fill_truncation == "either":
                if x is not None and y is not None:
                    break
            elif self.missing_value_fill_truncation == "x":
                if x is not None:
                    break
            elif self.missing_value_fill_truncation == "y":
                if y is not None:
                    break
            else:
                raise ValueError(
                    "Invalid value ({}) for config key "
                    "'missing_value_fill_truncation';"
                    " Use 'x', 'y' or 'either'".format(
                        self.missing_value_fill_truncation))
            end -= 1

        return ([(values[0][0], zero)] +
                values +
                [(values[end][0], zero)])

    def line(self, serie, rescale=False):
        """Draw the line serie"""
        serie_node = self.svg.serie(serie)
        if rescale and self.secondary_series:
            points = self._rescale(serie.points)
        else:
            points = serie.points
        view_values = list(map(self.view, points))
        if serie.show_dots:
            for i, (x, y) in enumerate(view_values):
                if None in (x, y):
                    continue
                if self.logarithmic:
                    if points[i][1] is None or points[i][1] <= 0:
                        continue
                if (serie.show_only_major_dots and
                        self.x_labels and i < len(self.x_labels) and
                        self.x_labels[i] not in self._x_labels_major):
                    continue

                metadata = serie.metadata.get(i)
                classes = []
                if x > self.view.width / 2:
                    classes.append('left')
                if y > self.view.height / 2:
                    classes.append('top')
                classes = ' '.join(classes)

                self._confidence_interval(
                    serie_node['overlay'], x, y, serie.values[i], metadata)

                dots = decorate(
                    self.svg,
                    self.svg.node(serie_node['overlay'], class_="dots"),
                    metadata)

                val = self._format(serie, i)
                alter(self.svg.transposable_node(
                    dots, 'circle', cx=x, cy=y, r=serie.dots_size,
                    class_='dot reactive tooltip-trigger'), metadata)
                self._tooltip_data(
                    dots, val, x, y,
                    xlabel=self._get_x_label(i))
                self._static_value(
                    serie_node, val,
                    x + self.style.value_font_size,
                    y + self.style.value_font_size,
                    metadata)

        if serie.stroke:
            if self.interpolate:
                points = serie.interpolated
                if rescale and self.secondary_series:
                    points = self._rescale(points)
                view_values = list(map(self.view, points))
            if serie.fill:
                view_values = self._fill(view_values)

            if serie.allow_interruptions:
                # view_values are in form [(x1, y1), (x2, y2)]. We
                # need to split that into multiple sequences if a
                # None is present here

                sequences = []
                cur_sequence = []
                for x, y in view_values:
                    if y is None and len(cur_sequence) > 0:
                        # emit current subsequence
                        sequences.append(cur_sequence)
                        cur_sequence = []
                    elif y is None:       # just discard
                        continue
                    else:
                        cur_sequence.append((x, y))   # append the element

                if len(cur_sequence) > 0:      # emit last possible sequence
                    sequences.append(cur_sequence)
            else:
                # plain vanilla rendering
                sequences = [view_values]
            if self.logarithmic:
                for seq in sequences:
                    for ele in seq[::-1]:
                        y = points[seq.index(ele)][1]
                        if y is None or y <= 0:
                            del seq[seq.index(ele)]
            for seq in sequences:
                self.svg.line(
                    serie_node['plot'], seq, close=self._self_close,
                    class_='line reactive' +
                           (' nofill' if not serie.fill else ''))

    def _compute(self):
        """Compute y min and max and y scale and set labels"""
        # X Labels
        if self.horizontal:
            self._x_pos = [
                x / (self._len - 1) for x in range(self._len)
            ][::-1] if self._len != 1 else [.5]  # Center if only one value
        else:
            self._x_pos = [
                x / (self._len - 1) for x in range(self._len)
            ] if self._len != 1 else [.5]  # Center if only one value

        self._points(self._x_pos)

        if self.include_x_axis:
            # Y Label
            self._box.ymin = min(self._min or 0, 0)
            self._box.ymax = max(self._max or 0, 0)
        else:
            self._box.ymin = self._min
            self._box.ymax = self._max

    def _plot(self):
        """Plot the serie lines and secondary serie lines"""
        for serie in self.series:
            self.line(serie)

        for serie in self.secondary_series:
            self.line(serie, True)
