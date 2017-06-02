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
Formatters to use with `value_formatter` and `x_value_formatter` configs

"""
from __future__ import division

from datetime import date, datetime, time
from math import floor, log

from pygal._compat import to_str, u
from pygal.util import float_format


class Formatter(object):
    pass


class HumanReadable(Formatter):
    """Format a number to engineer scale"""
    ORDERS = u("yzafpnµm kMGTPEZY")

    def __init__(self, none_char=u('∅')):
        self.none_char = none_char

    def __call__(self, val):
        if val is None:
            return self.none_char
        order = val and int(floor(log(abs(val)) / log(1000)))
        orders = self.ORDERS.split(" ")[int(order > 0)]
        if order == 0 or order > len(orders):
            return float_format(val / (1000 ** int(order)))
        return (
            float_format(val / (1000 ** int(order))) +
            orders[int(order) - int(order > 0)])


class Significant(Formatter):
    """Show precision significant digit of float"""
    def __init__(self, precision=10):
        self.format = '%%.%dg' % precision

    def __call__(self, val):
        if val is None:
            return ''
        return self.format % val


class Integer(Formatter):
    """Cast number to integer"""

    def __call__(self, val):
        if val is None:
            return ''
        return '%d' % val


class Raw(Formatter):
    """Cast everything to string"""

    def __call__(self, val):
        if val is None:
            return ''
        return to_str(val)


class IsoDateTime(Formatter):
    """Iso format datetimes"""

    def __call__(self, val):
        if val is None:
            return ''
        return val.isoformat()


class Default(Significant, IsoDateTime, Raw):
    """Try to guess best format from type"""

    def __call__(self, val):
        if val is None:
            return ''
        if isinstance(val, (int, float)):
            return Significant.__call__(self, val)
        if isinstance(val, (date, time, datetime)):
            return IsoDateTime.__call__(self, val)
        return Raw.__call__(self, val)


# Formatters with default options
human_readable = HumanReadable()
significant = Significant()
integer = Integer()
raw = Raw()

# Default config formatter
default = Default()
