# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2016 Kozea
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
XY Line graph: Plot a set of couple data points (x, y) connected by
straight segments.
"""

from __future__ import division

from functools import reduce

from pygal.graph.dual import Dual
from pygal.graph.line import Line
from pygal.util import cached_property, compose, ident


class XY(Line, Dual):

    """XY Line graph class"""

    _x_adapters = []

    @cached_property
    def xvals(self):
        """All x values"""
        return [val[0]
                for serie in self.all_series
                for val in serie.values
                if val[0] is not None]

    @cached_property
    def yvals(self):
        """All y values"""
        return [val[1]
                for serie in self.series
                for val in serie.values
                if val[1] is not None]

    @cached_property
    def _min(self):
        """Getter for the minimum series value"""
        return (self.range[0] if (self.range and self.range[0] is not None)
                else (min(self.yvals) if self.yvals else None))

    @cached_property
    def _max(self):
        """Getter for the maximum series value"""
        return (self.range[1] if (self.range and self.range[1] is not None)
                else (max(self.yvals) if self.yvals else None))

    def _compute(self):
        """Compute x/y min and max and x/y scale and set labels"""
        if self.xvals:
            if self.xrange:
                x_adapter = reduce(
                    compose, self._x_adapters) if getattr(
                        self, '_x_adapters', None) else ident

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

        # these values can also be 0 (zero), so testing explicitly for None
        if xrng is not None:
            self._box.xmin, self._box.xmax = xmin, xmax

        if yrng is not None:
            self._box.ymin, self._box.ymax = ymin, ymax
