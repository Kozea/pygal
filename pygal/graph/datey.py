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
    return datetime(year=2013,month=1,day=1)+timedelta(days=n)
    
x=(1,20,35,54,345,898)
x=tuple(map(jour,x))
y=(1,3,4,2,3,1)
graph=pygal.DateY(x_label_rotation=20)
graph.add("graph1",list(zip(x,y))+[None,None])
graph.render_in_browser()   
"""


from pygal.util import compute_scale
from pygal.graph.line import Line
from pygal.graph.xy import XY 
import datetime

class DateY(XY):
    """ DateY Graph """
    _offset=datetime.datetime(year=2000,month=1,day=1)
    def _todate(self, d) :
        """ Converts  a number to a date """
        return str(self._offset+datetime.timedelta(seconds=d))
    def _tonumber(self,d) :
        """ Converts a date to a number """
        if d==None: return None
        return  (d-self._offset).total_seconds()

    def _get_value(self, values, i):
        return 'x=%s, y=%s' % (self._todate(values[i][0]),self._format(values[i][1]))

    def _compute(self):
        # Approximatively the same code as in XY.
        # The only difference is the transformation of dates to numbers
        # (beginning) and the reversed transforamtion to dates (end)
        self._offset = min([val[0]
                 for serie in self.series
                 for val in serie.values
                 if val[0] is not None])
        for serie in self.series :
            serie.values=[(self._tonumber(v[0]),v[1]) for v in serie.values]
        
        xvals = [val[0]
                 for serie in self.series
                 for val in serie.values
                 if val[0] is not None]
        yvals = [val[1]
                 for serie in self.series
                 for val in serie.values
                 if val[1] is not None]
        if xvals:
            xmin = min(xvals)
            xmax = max(xvals)
            rng = (xmax - xmin)
        else:
            rng = None

        for serie in self.series:
            serie.points = serie.values
            if self.interpolate and rng:
                vals = list(zip(*sorted(
                    [t for t in serie.points if None not in t], key=lambda x: x[0])))
                serie.interpolated = self._interpolate(
                    vals[1], vals[0], xy=True, xy_xmin=xmin, xy_rng=rng)

        if self.interpolate and rng:
            xvals = [val[0]
                     for serie in self.series
                     for val in serie.interpolated]
            yvals = [val[1]
                     for serie in self.series
                     for val in serie.interpolated]
            if xvals:
                xmin = min(xvals)
                xmax = max(xvals)
                rng = (xmax - xmin)
            else:
                rng = None

        if rng:
            self._box.xmin, self._box.xmax = min(xvals), max(xvals)
            self._box.ymin, self._box.ymax = min(yvals), max(yvals)

        x_pos = compute_scale(
            self._box.xmin, self._box.xmax, self.logarithmic, self.order_min)
        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min)

        self._x_labels = list(zip(list(map(self._todate, x_pos)), x_pos))
        self._y_labels = list(zip(list(map(self._format, y_pos)), y_pos))
