# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
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
Various utils

"""

from __future__ import division
from decimal import Decimal
from math import floor, pi, log, log10
ORDERS = u"yzafpnµm kMGTPEZY"


def float_format(number):
    """Format a float to a precision of 3, without zeroes or dots"""
    return ("%.3f" % number).rstrip('0').rstrip('.')


def humanize(number):
    """Format a number to engineer scale"""
    order = number and int(floor(log(abs(number)) / log(1000)))
    human_readable = ORDERS.split(" ")[int(order > 0)]
    if order == 0 or order > len(human_readable):
        return float_format(number / (1000 ** int(order)))
    return (
        float_format(number / (1000 ** int(order))) +
        human_readable[int(order) - int(order > 0)])


def is_major(number):
    """Returns True if number is a round order: 1, 100, 0.001"""
    return not number or 10 ** floor(log10(abs(number))) == abs(number)


def round_to_int(number, precision):
    """Round a number to a precision"""
    precision = int(precision)
    rounded = (int(number) + precision / 2) // precision * precision
    return rounded


def round_to_float(number, precision):
    """Round a float to a precision"""
    rounded = Decimal(str(floor((number + precision / 2) // precision))
    ) * Decimal(str(precision))
    return float(rounded)


def round_to_scale(number, precision):
    """Round a number or a float to a precision"""
    if precision < 1:
        return round_to_float(number, precision)
    return round_to_int(number, precision)


def cut(list_, index=0):
    """Cut a list by index or arg"""
    if isinstance(index, int):
        cut_ = lambda x: x[index]
    else:
        cut_ = lambda x: getattr(x, index)
    return map(cut_, list_)


def rad(degrees):
    """Convert degrees in radiants"""
    return pi * degrees / 180


def deg(radiants):
    """Convert radiants in degrees"""
    return 180 * radiants / pi


def _swap_curly(string):
    """Swap single and double curly brackets"""
    return (string
            .replace('{{ ', '{{')
            .replace('{{', '\x00')
            .replace('{', '{{')
            .replace('\x00', '{')
            .replace(' }}', '}}')
            .replace('}}', '\x00')
            .replace('}', '}}')
            .replace('\x00', '}'))


def template(string, **kwargs):
    """Format a string using double braces"""
    return _swap_curly(string).format(**kwargs)


def coord_format(xy):
    """Format x y coords to svg"""
    return '%f %f' % xy

swap = lambda tuple_: tuple(reversed(tuple_))
ident = lambda x: x


# Stolen from brownie http://packages.python.org/Brownie/
class cached_property(object):
    """Optimize a static property"""
    def __init__(self, getter, doc=None):
        self.getter = getter
        self.__module__ = getter.__module__
        self.__name__ = getter.__name__
        self.__doc__ = doc or getter.__doc__

    def __get__(self, obj, type_=None):
        if obj is None:
            return self
        value = obj.__dict__[self.__name__] = self.getter(obj)
        return value
