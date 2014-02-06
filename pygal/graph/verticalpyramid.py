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
Pyramid chart

"""

from __future__ import division
from pygal.adapters import positive
from pygal.graph.stackedbar import StackedBar


class VerticalPyramid(StackedBar):
    """Pyramid graph"""

    _adapters = [positive]

    def _format(self, value):
        value = value and abs(value)
        return super(VerticalPyramid, self)._format(value)

    def _get_separated_values(self, secondary=False):
        series = self.secondary_series if secondary else self.series
        positive_vals = zip(*[serie.safe_values
                              for index, serie in enumerate(series)
                              if index % 2])
        negative_vals = zip(*[serie.safe_values
                              for index, serie in enumerate(series)
                              if not index % 2])
        return list(positive_vals), list(negative_vals)

    def _compute_box(self, positive_vals, negative_vals):
        positive_sum = list(map(sum, positive_vals)) or [self.zero]
        negative_sum = list(map(sum, negative_vals)) or [self.zero]
        self._box.ymax = max(max(positive_sum), max(negative_sum))
        self._box.ymin = - self._box.ymax

    def _compute_secondary(self):
        # Need refactoring
        if self.secondary_series:
            y_pos = list(zip(*self._y_labels))[1]
            positive_vals, negative_vals = self._get_separated_values(True)
            positive_sum = map(sum, positive_vals) or [self.zero]
            negative_sum = map(sum, negative_vals) or [self.zero]
            ymax = max(max(positive_sum), max(negative_sum))
            ymin = -ymax

            min_0_ratio = (self.zero - self._box.ymin) / self._box.height
            max_0_ratio = (self._box.ymax - self.zero) / self._box.height

            new_ymax = (self.zero - ymin) * (1 / min_0_ratio - 1)
            new_ymin = -(ymax - self.zero) * (1 / max_0_ratio - 1)
            if ymax > self._box.ymax:
                ymin = new_ymin
            else:
                ymax = new_ymax

            left_range = abs(self._box.ymax - self._box.ymin)
            right_range = abs(ymax - ymin)
            self._scale = left_range / right_range
            self._scale_diff = self._box.ymin
            self._scale_min_2nd = ymin
            self._y_2nd_labels = [
                (self._format(self._box.xmin + y * right_range / left_range),
                 y)
                for y in y_pos]

    def _bar(self, parent, x, y, index, i, zero, shift=True, secondary=False):
        if index % 2:
            y = -y
        return super(VerticalPyramid, self)._bar(
            parent, x, y, index, i, zero, False, secondary)
