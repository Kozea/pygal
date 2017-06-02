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
"""Value adapters to use when a chart doesn't accept all value types"""
from decimal import Decimal

from pygal._compat import is_str


def positive(x):
    """Return zero if value is negative"""
    if x is None:
        return
    if is_str(x):
        return x
    if x < 0:
        return 0
    return x


def not_zero(x):
    """Return None if value is zero"""
    if x == 0:
        return
    return x


def none_to_zero(x):
    """Return 0 if value is None"""
    if x is None:
        return 0
    return x


def decimal_to_float(x):
    """Cast Decimal values to float"""
    if isinstance(x, Decimal):
        return float(x)
    return x
