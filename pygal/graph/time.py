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
Various datetime line plot
"""

from pygal.graph.xy import XY
from datetime import datetime, date, time, timedelta
from pygal._compat import timestamp, total_seconds


def datetime_to_timestamp(x):
    if isinstance(x, datetime):
        return timestamp(x)
    return x


def date_to_datetime(x):
    if isinstance(x, date):
        return datetime.combine(x, time())
    return x


def time_to_datetime(x):
    if isinstance(x, time):
        return datetime.combine(date(1970, 1, 1), x)
    return x


def timedelta_to_seconds(x):
    if isinstance(x, timedelta):
        return total_seconds(x)
    return x


class DateTimeLine(XY):
    _x_adapters = [datetime_to_timestamp, date_to_datetime]

    @property
    def _x_format(self):
        """Return the value formatter for this graph"""
        def datetime_to_str(x):
            dt = datetime.fromtimestamp(x)
            if self.config.x_value_formatter:
                return self.config.x_value_formatter(dt)
            return dt.isoformat()
        return datetime_to_str


class DateLine(DateTimeLine):

    @property
    def _x_format(self):
        """Return the value formatter for this graph"""
        def date_to_str(x):
            d = date.fromtimestamp(x)
            if self.config.x_value_formatter:
                return self.config.x_value_formatter(d)
            return d.isoformat()
        return date_to_str


class TimeLine(DateTimeLine):
    _x_adapters = [datetime_to_timestamp, time_to_datetime]

    @property
    def _x_format(self):
        """Return the value formatter for this graph"""
        def date_to_str(x):
            t = datetime.fromtimestamp(x).time()
            if self.config.x_value_formatter:
                return self.config.x_value_formatter(t)
            return t.isoformat()
        return date_to_str


class TimeDeltaLine(XY):
    _x_adapters = [timedelta_to_seconds]

    @property
    def _x_format(self):
        """Return the value formatter for this graph"""
        def timedelta_to_str(x):
            td = timedelta(seconds=x)
            if self.config.x_value_formatter:
                return self.config.x_value_formatter(td)
            return str(td)

        return timedelta_to_str

# Old pygal compat
DateY = DateTimeLine
