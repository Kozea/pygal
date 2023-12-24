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
"""Various hacks for former transparent python 2 / python 3 support"""

import datetime
from collections.abc import Iterable


def is_list_like(value):
    """Return whether value is an iterable but not a mapping / string"""
    return isinstance(value, Iterable) and not isinstance(value, (str, dict))


def timestamp(x):
    """Get a timestamp from a date"""
    if x.tzinfo is None:
        # Naive dates to utc
        x = x.replace(tzinfo=datetime.timezone.utc)

    return x.timestamp()
