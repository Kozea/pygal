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
XY Line graph

"""

from __future__ import division
from pygal.util import compute_scale
from pygal.graph.line import Line


class XY(Line):
    """XY Line graph"""

    def _get_value(self, values, i):
        return 'x=%s, y=%s' % tuple(map(self._format, values[i]))

    def _compute(self):
        xvals = [val[0]
                 for serie in self.series
                 for val in serie.values
                 if val[0] is not None]
        yvals = [val[1]
                 for serie in self.series
                 for val in serie.values
                 if val[1] is not None]
        xmin = min(xvals)
        xmax = max(xvals)
        rng = (xmax - xmin)

        for serie in self.series:
            serie.points = serie.values
            if self.interpolate:
                vals = zip(*sorted(
                    filter(lambda t: None not in t,
                           serie.points), key=lambda x: x[0]))
                serie.interpolated = self._interpolate(
                    vals[1], vals[0], xy=True, xy_xmin=xmin, xy_rng=rng)

        if self.interpolate:
            xvals = [val[0]
                     for serie in self.series
                     for val in serie.interpolated]
            yvals = [val[1]
                     for serie in self.series
                     for val in serie.interpolated]

        self._box.xmin, self._box.xmax = min(xvals), max(xvals)
        self._box.ymin, self._box.ymax = min(yvals), max(yvals)
        x_pos = compute_scale(
            self._box.xmin, self._box.xmax, self.logarithmic, self.order_min)
        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min)

        self._x_labels = zip(map(self._format, x_pos), x_pos)
        self._y_labels = zip(map(self._format, y_pos), y_pos)
