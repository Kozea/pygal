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
XY Line graph

"""

from __future__ import division
from functools import reduce
from pygal.util import compute_scale, cached_property, compose
from pygal.graph.line import Line


class XY(Line):
    """XY Line graph"""
    _dual = True
    _x_adapters = []

    @cached_property
    def xvals(self):
        return [val[0]
                for serie in self.all_series
                for val in serie.values
                if val[0] is not None]

    @cached_property
    def yvals(self):
        return [val[1]
                for serie in self.series
                for val in serie.values
                if val[1] is not None]

    @cached_property
    def _min(self):
        return (self.range[0] if (self.range and self.range[0] is not None)
                else (min(self.yvals) if self.yvals else None))

    @cached_property
    def _max(self):
        return (self.range[1] if (self.range and self.range[1] is not None)
                else (max(self.yvals) if self.yvals else None))

    def _has_data(self):
        """Check if there is any data"""
        return sum(
            map(len, map(lambda s: s.safe_values, self.series))) != 0 and any((
                sum(map(abs, self.xvals)) != 0,
                sum(map(abs, self.yvals)) != 0))

    def _compute(self):
        if self.xvals:
            if self.xrange:
                x_adapter = reduce(
                    compose, self._x_adapters) if getattr(
                        self, '_x_adapters', None) else None

                xmin = x_adapter(self.xrange[0])
                xmax = x_adapter(self.xrange[1])

            else:
                xmin = min(self.xvals)
                xmax = max(self.xvals)
            xrng = (xmax - xmin)
        else:
            xrng = None

        if self.yvals:
            ymin = self._min
            ymax = self._max

            if self.include_x_axis:
                ymin = min(ymin or 0, 0)
                ymax = max(ymax or 0, 0)

            yrng = (ymax - ymin)
        else:
            yrng = None

        for serie in self.all_series:
            serie.points = serie.values
            if self.interpolate:
                vals = list(zip(*sorted(
                    filter(lambda t: None not in t,
                           serie.points), key=lambda x: x[0])))
                serie.interpolated = self._interpolate(vals[0], vals[1])

        if self.interpolate:
            self.xvals = [val[0]
                          for serie in self.all_series
                          for val in serie.interpolated]
            self.yvals = [val[1]
                          for serie in self.series
                          for val in serie.interpolated]
            if self.xvals:
                xmin = min(self.xvals)
                xmax = max(self.xvals)
                xrng = (xmax - xmin)
            else:
                xrng = None

        if xrng:
            self._box.xmin, self._box.xmax = xmin, xmax
        if yrng:
            self._box.ymin, self._box.ymax = ymin, ymax

        x_pos = compute_scale(
            self._box.xmin, self._box.xmax, self.logarithmic,
            self.order_min)
        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min)

        self._x_labels = list(zip(map(self._x_format, x_pos), x_pos))
        self._y_labels = list(zip(map(self._format, y_pos), y_pos))
