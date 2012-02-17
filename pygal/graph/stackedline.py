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
from pygal.graph.line import Line
from pygal.interpolate import interpolation


class StackedLine(Line):
    """Stacked Line graph"""

    def _fill(self, values):
        if not hasattr(self, '_previous_line'):
            self._previous_line = values
            return super(StackedLine, self)._fill(values)
        new_values = values + list(reversed(self._previous_line))
        self._previous_line = values
        return new_values

    def _compute(self):
        self._x_pos = [x / float(self._len - 1) for x in range(self._len)
        ] if self._len != 1 else [.5]  # Center if only one value
        accumulation = [0] * self._len
        for serie in self.series:
            accumulation = map(sum, zip(accumulation, serie.values))
            serie.points = [
                (self._x_pos[i], v)
                for i, v in enumerate(accumulation)]
            if self.interpolate:
                interpolate = interpolation(
                    self._x_pos, accumulation, kind=self.interpolate)
                p = float(self.interpolation_precision)
                serie.interpolated = [(x / p, float(interpolate(x / p)))
                                      for x in range(int(p + 1))]
        return super(StackedLine, self)._compute()
