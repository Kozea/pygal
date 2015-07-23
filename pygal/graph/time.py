# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2015 Kozea
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
XY time extensions: handle convertion of date, time, datetime, timedelta
into float for xy plot and back to their type for display
"""

from datetime import date, datetime, time, timedelta

from pygal._compat import is_str, timestamp, total_seconds
from pygal.adapters import positive
from pygal.graph.xy import XY


def datetime_to_timestamp(x):
    """Convert a datetime into a utc float timestamp"""
    if isinstance(x, datetime):
        return timestamp(x)
    return x


def datetime_to_time(x):
    """Convert a datetime into a time"""
    if isinstance(x, datetime):
        return x.time()
    return x


def date_to_datetime(x):
    """Convert a date into a datetime"""
    if not isinstance(x, datetime) and isinstance(x, date):
        return datetime.combine(x, time())
    return x


def time_to_datetime(x):
    """Convert a time into a datetime"""
    if isinstance(x, time):
        return datetime.combine(date(1970, 1, 1), x)
    return x


def timedelta_to_seconds(x):
    """Convert a timedelta into an amount of seconds"""
    if isinstance(x, timedelta):
        return total_seconds(x)
    return x


def time_to_seconds(x):
    """Convert a time in a seconds sum"""
    if isinstance(x, time):
        return ((
            ((x.hour * 60) + x.minute) * 60 + x.second
        ) * 10 ** 6 + x.microsecond) / 10 ** 6

    if is_str(x):
        return x
    # Clamp to valid time
    return x and max(0, min(x, 24 * 3600 - 10 ** -6))


def seconds_to_time(x):
    """Convert a number of second into a time"""
    t = int(x * 10 ** 6)
    ms = t % 10 ** 6
    t = t // 10 ** 6
    s = t % 60
    t = t // 60
    m = t % 60
    t = t // 60
    h = t
    return time(h, m, s, ms)


class DateTimeLine(XY):

    """DateTime abscissa xy graph class"""

    _x_adapters = [datetime_to_timestamp, date_to_datetime]

    @property
    def _x_format(self):
        """Return the value formatter for this graph"""
        def datetime_to_str(x):
            dt = datetime.utcfromtimestamp(x)
            if self.x_value_formatter:
                return self.x_value_formatter(dt)
            return dt.isoformat()
        return datetime_to_str


class DateLine(DateTimeLine):

    """Date abscissa xy graph class"""

    @property
    def _x_format(self):
        """Return the value formatter for this graph"""
        def date_to_str(x):
            d = date.fromtimestamp(x)
            if self.x_value_formatter:
                return self.x_value_formatter(d)
            return d.isoformat()
        return date_to_str


class TimeLine(DateTimeLine):

    """Time abscissa xy graph class"""

    _x_adapters = [positive, time_to_seconds, datetime_to_time]

    @property
    def _x_format(self):
        """Return the value formatter for this graph"""
        def date_to_str(x):
            t = seconds_to_time(x)
            if self.x_value_formatter:
                return self.x_value_formatter(t)
            return t.isoformat()
        return date_to_str


class TimeDeltaLine(XY):

    """TimeDelta abscissa xy graph class"""

    _x_adapters = [timedelta_to_seconds]

    @property
    def _x_format(self):
        """Return the value formatter for this graph"""
        def timedelta_to_str(x):
            td = timedelta(seconds=x)
            if self.x_value_formatter:
                return self.x_value_formatter(td)
            return str(td)

        return timedelta_to_str
