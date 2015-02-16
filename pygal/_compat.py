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
import sys
from collections import Iterable
import time


if sys.version_info[0] == 3:
    base = (str, bytes)
    coerce = str
else:
    base = basestring
    coerce = unicode


def is_list_like(value):
    return isinstance(value, Iterable) and not isinstance(value, (base, dict))


def is_str(string):
    return isinstance(string, base)


def to_str(string):
    if not is_str(string):
        return coerce(string)
    return string


def to_unicode(string):
    if not isinstance(string, coerce):
        return string.decode('utf-8')
    return string


def u(s):
    if sys.version_info[0] == 2:
        return s.decode('utf-8')
    return s


def total_seconds(td):
    if sys.version_info[:2] == (2, 6):
        return (
            (td.days * 86400 + td.seconds) * 10 ** 6 + td.microseconds
        ) / 10 ** 6
    return td.total_seconds()


def timestamp(x):
    if hasattr(x, 'timestamp'):
        return x.timestamp()
    else:
        if hasattr(x, 'utctimetuple'):
            t = x.utctimetuple()
        else:
            t = x.timetuple()
        return time.mktime(t)
