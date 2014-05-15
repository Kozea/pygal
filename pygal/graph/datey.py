# -*- coding: utf-8 -*-
# This file is proposed as a part of pygal
# A python svg graph plotting library
#
# A python svg graph plotting library
# Copyright © 2012 Snarkturne  (modified from Kozea XY class)
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
DateY graph

Example :
import pygal
from datetime import datetime,timedelta

def jour(n) :
    return datetime(year=2014,month=1,day=1)+timedelta(days=n)

x=(1,20,35,54,345,898)
x=tuple(map(jour,x))
x_label=(0,100,200,300,400,500,600,700,800,900,1000)
x_label=map(jour,x_label)
y=(1,3,4,2,3,1)
graph=pygal.DateY(x_label_rotation=20)
graph.x_label_format = "%Y-%m-%d"
graph.x_labels = x_label
graph.add("graph1",list(zip(x,y))+[None,None])
graph.render_in_browser()
"""

from pygal._compat import total_seconds
from pygal.adapters import date
from pygal.util import compute_scale
from pygal.graph.xy import XY
import datetime


class DateY(XY):
    """ DateY Graph """
    _offset = datetime.datetime(year=2000, month=1, day=1)
    _adapters = [date]

    def _todate(self, d):
        """ Converts a number to a date """
        currDateTime = self._offset + datetime.timedelta(seconds=d or 0)
        return currDateTime.strftime(self.x_label_format)

    def _tonumber(self, d):
        """ Converts a date to a number """
        if d is None:
            return None
        return total_seconds(d - self._offset)

    def _get_value(self, values, i):
        return 'x=%s, y=%s' % (
            self._todate(values[i][0]), self._format(values[i][1]))

    def _compute(self):
        # Approximatively the same code as in XY.
        # The only difference is the transformation of dates to numbers
        # (beginning) and the reversed transformation to dates (end)
        self._offset = min([val[0]
                            for serie in self.series
                            for val in serie.values
                            if val[0] is not None]
                           or [datetime.datetime.fromtimestamp(0)])
        for serie in self.all_series:
            serie.values = [(self._tonumber(v[0]), v[1]) for v in serie.values]

        if self.xvals:
            xmin = min(self.xvals)
            xmax = max(self.xvals)
            rng = (xmax - xmin)
        else:
            rng = None

        if self.yvals:
            ymin = self._min
            ymax = self._max
            if self.include_x_axis:
                ymin = min(self._min or 0, 0)
                ymax = max(self._max or 0, 0)

        for serie in self.all_series:
            serie.points = serie.values
            if self.interpolate and rng:
                vals = list(zip(*sorted(
                    [t for t in serie.points if None not in t],
                    key=lambda x: x[0])))
                serie.interpolated = self._interpolate(vals[0], vals[1])

        if self.interpolate and rng:
            self.xvals = [val[0]
                          for serie in self.all_series
                          for val in serie.interpolated]
            self.yvals = [val[1]
                          for serie in self.all_series
                          for val in serie.interpolated]

            xmin = min(self.xvals)
            xmax = max(self.xvals)
            rng = (xmax - xmin)

        # Calculate/prcoess the x_labels
        if self.x_labels and all(
                map(lambda x: isinstance(
                    x, (datetime.datetime, datetime.date)), self.x_labels)):
            # Process the given x_labels
            x_labels_num = []
            for label in self.x_labels:
                x_labels_num.append(self._tonumber(label))
            x_pos = x_labels_num

            # Update the xmin/xmax to fit all of the x_labels and the data
            xmin = min(xmin, min(x_pos))
            xmax = max(xmax, max(x_pos))

            self._box.xmin, self._box.xmax = xmin, xmax
            self._box.ymin, self._box.ymax = ymin, ymax
        else:
            # Automatically generate the x_labels
            if rng:
                self._box.xmin, self._box.xmax = xmin, xmax
                self._box.ymin, self._box.ymax = ymin, ymax

            x_pos = compute_scale(
                self._box.xmin, self._box.xmax, self.logarithmic,
                self.order_min)

        # Always auto-generate the y labels
        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min)

        self._x_labels = list(zip(list(map(self._todate, x_pos)), x_pos))
        self._y_labels = list(zip(list(map(self._format, y_pos)), y_pos))
