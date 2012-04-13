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
Stacked Line chart

"""

from pygal.graph.line import Line
from itertools import izip_longest


class StackedLine(Line):
    """Stacked Line graph"""

    def __init__(self, *args, **kwargs):
        self._previous_line = None
        super(StackedLine, self).__init__(*args, **kwargs)

    def _fill(self, values):
        if not self._previous_line:
            self._previous_line = values
            return super(StackedLine, self)._fill(values)
        new_values = values + list(reversed(self._previous_line))
        self._previous_line = values
        return new_values

    def _compute(self):
        self._uniformize_data()
        x_pos = [x / float(self._len - 1) for x in range(self._len)
        ] if self._len != 1 else [.5]  # Center if only one value
        accumulation = [0] * self._len
        for serie in self.series:
            accumulation = map(sum, izip_longest(
                accumulation, [val
                               if val != None else 0
                               for val in serie.values], fillvalue=0))
            serie.points = [
                (x_pos[i], v)
                for i, v in enumerate(accumulation)]
            if self.interpolate:
                serie.interpolated = self._interpolate(accumulation, x_pos)
        return super(StackedLine, self)._compute()
