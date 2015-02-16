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
Value adapters to use when a chart doesn't accept all value types

"""
from decimal import Decimal


def positive(x):
    if x is None:
        return
    if x < 0:
        return 0
    return x


def not_zero(x):
    if x == 0:
        return
    return x


def none_to_zero(x):
    return x or 0


def decimal_to_float(x):
    if isinstance(x, Decimal):
        return float(x)
    return x
