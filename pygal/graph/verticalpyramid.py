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
Pyramid chart

"""

from __future__ import division
from pygal.util import compute_scale, safe_enumerate
from pygal.adapters import positive
from pygal.graph.stackedbar import StackedBar


class VerticalPyramid(StackedBar):
    """Pyramid graph"""

    _adapters = [positive]

    def _format(self, value):
        return super(VerticalPyramid, self)._format(abs(value))

    def _get_separated_values(self):
        positive_vals = zip(*[serie.safe_values
                              for index, serie in enumerate(self.series)
                              if index % 2])
        negative_vals = zip(*[serie.safe_values
                              for index, serie in enumerate(self.series)
                              if not index % 2])
        return positive_vals, negative_vals

    def _compute_box(self, positive_vals, negative_vals):
        positive_sum = map(sum, positive_vals) or [self.zero]
        negative_sum = map(sum, negative_vals) or [self.zero]
        self._box.ymax = max(max(positive_sum), max(negative_sum))
        self._box.ymin = - self._box.ymax

    def _bar(self, parent, x, y, index, i, zero, shift=True):
        if index % 2:
            y = -y
        return super(VerticalPyramid, self)._bar(
            parent, x, y, index, i, zero, False)
