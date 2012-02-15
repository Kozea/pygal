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


class StackedLine(Line):
    """Stacked Line graph"""

    @property
    def _values(self):
        sums = map(sum, zip(*[serie.values for serie in self.series]))
        return sums + super(StackedLine, self)._values

    def _plot(self):
        accumulation = map(sum, zip(*[serie.values for serie in self.series]))
        for serie in self.series:
            self.line(
                self._serie(serie.index), [
                (self._x_pos[i], v)
                for i, v in enumerate(accumulation)])
            accumulation = map(sum, zip(accumulation,
                                    [-v for v in serie.values]))
