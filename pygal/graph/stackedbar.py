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
from pygal.adapters import none_to_zero


class StackedBar(Bar):
    """Stacked Bar graph"""

    _adapters = [none_to_zero]

    def _get_separated_values(self):
        transposed = zip(*[serie.values for serie in self.series])
        positive_vals = [sum([
            val for val in vals
            if val is not None and val >= self.zero])
            for vals in transposed]
        negative_vals = [sum([
            val
            for val in vals
            if val is not None and val < self.zero])
            for vals in transposed]
        return positive_vals, negative_vals

    def _compute_box(self, positive_vals, negative_vals):
        self._box.ymin = negative_vals and min(min(negative_vals), self.zero)
        self._box.ymax = positive_vals and max(max(positive_vals), self.zero)

    def _compute(self):
        positive_vals, negative_vals = self._get_separated_values()
        self._compute_box(positive_vals, negative_vals)

        if self.logarithmic:
            positive_vals = filter(lambda x: x > 0, positive_vals)
            negative_vals = filter(lambda x: x > 0, negative_vals)

        positive_vals = positive_vals or [self.zero]
        negative_vals = negative_vals or [self.zero]

        x_pos = [
            x / self._len for x in range(self._len + 1)
        ] if self._len > 1 else [0, 1]  # Center if only one value

        self._points(x_pos)
        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min
        ) if not self.y_labels else map(float, self.y_labels)
        self._x_ranges = zip(x_pos, x_pos[1:])

        self._x_labels = self.x_labels and zip(self.x_labels, [
            sum(x_range) / 2 for x_range in self._x_ranges])
        self._y_labels = zip(map(self._format, y_pos), y_pos)

        self.negative_cumulation = [0] * self._len
        self.positive_cumulation = [0] * self._len

    def _bar(self, parent, x, y, index, i, zero, shift=True):
        cumulation = (self.negative_cumulation if y < self.zero else
                      self.positive_cumulation)
        zero = cumulation[i]
        cumulation[i] = zero + y
        if zero == 0:
            zero = self.zero
            y -= self.zero
        return super(StackedBar, self)._bar(
            parent, x, zero + y, index, i, zero, False)
