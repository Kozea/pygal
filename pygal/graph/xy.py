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


class XY(Line):
    """XY Line graph"""

    def _get_value(self, values, i):
        return str(values[i])

    def _compute(self):
        for serie in self.series:
            serie.values = sorted(serie.values, key=lambda x: x[0])
        xvals = [val[0] for serie in self.series for val in serie.values]
        yvals = [val[1] for serie in self.series for val in serie.values]
        self._box.xmin, self._box.xmax = min(xvals), max(xvals)
        self._box.ymin, self._box.ymax = min(yvals), max(yvals)

        x_pos = self._pos(self._box.xmin, self._box.xmax, self.x_scale)
        y_pos = self._pos(self._box.ymin, self._box.ymax, self.y_scale)

        self._x_labels = zip(map(str, x_pos), x_pos)
        self._y_labels = zip(map(str, y_pos), y_pos)

    def _plot(self):
        for serie in self.series:
            self.line(
                self._serie(serie.index), serie.values)
