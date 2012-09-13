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
Stacked Bar chart

"""

from __future__ import division
from pygal.graph.bar import Bar
from pygal.util import compute_scale


class StackedBar(Bar):
    """Stacked Bar graph"""

    def _compute(self):
        transposed = zip(*[serie.values for serie in self.series])
        positive_vals = [
            sum([val if val is not None and val > 0 else 0 for val in vals])
            for vals in transposed]
        negative_vals = [
            sum([val if val is not None and val < 0 else 0 for val in vals])
            for vals in transposed]

        self._box.ymin, self._box.ymax = (
            min(min(negative_vals), 0), max(max(positive_vals), 0))

        x_pos = [
            x / self._len for x in range(self._len + 1)
        ] if self._len > 1 else [0, 1]  # Center if only one value
        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min
        ) if not self.y_labels else map(float, self.y_labels)
        self._x_ranges = zip(x_pos, x_pos[1:])

        self._x_labels = self.x_labels and zip(self.x_labels, [
            sum(x_range) / 2 for x_range in self._x_ranges])
        self._y_labels = zip(map(self._format, y_pos), y_pos)

    def _plot(self):
        stack_vals = [[0, 0] for i in range(self._len)]
        for index, serie in enumerate(self.series):
            serie_node = self._serie(index)
            stack_vals = self.bar(
                serie_node, serie, [
                    tuple((self._x_ranges[i][j], v) for j in range(2))
                    for i, v in enumerate(serie.values)], index,
                stack_vals)
