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
from math import floor, pi, log, log10, ceil
from itertools import cycle
ORDERS = u"yzafpnµm kMGTPEZY"


def get_value(val):
    if isinstance(val, dict):
        return val['value']
    return val


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


def compute_logarithmic_scale(min_, max_):
    """Compute an optimal scale for logarithmic"""
    if max_ <= 0 or min_ <= 0:
        return []
    min_order = int(floor(log10(min_)))
    max_order = int(ceil(log10(max_)))
    positions = []
    amplitude = max_order - min_order
    if amplitude <= 1:
        return []
    detail = 10.
    while amplitude * detail < 20:
        detail *= 2
    while amplitude * detail > 50:
        detail /= 2
    for order in range(min_order, max_order + 1):
        for i in range(int(detail)):
            tick = (10 * i / detail or 1) * 10 ** order
            tick = round_to_scale(tick, tick)
            if min_ <= tick <= max_ and tick not in positions:
                positions.append(tick)
    return positions


def compute_scale(min_, max_, logarithmic=False, min_scale=4, max_scale=20):
    """Compute an optimal scale between min and max"""
    if min_ == 0 and max_ == 0:
        return [0]
    if max_ - min_ == 0:
        return [min_]
    if logarithmic:
        log_scale = compute_logarithmic_scale(min_, max_)
        if log_scale:
            return log_scale
            # else we fallback to normal scalling
    order = round(log10(max(abs(min_), abs(max_)))) - 1
    while (max_ - min_) / (10 ** order) < min_scale:
        order -= 1
    step = float(10 ** order)
    while (max_ - min_) / step > max_scale:
        step *= 2.
    positions = []
    position = round_to_scale(min_, step)
    while position < (max_ + step):
        rounded = round_to_scale(position, step)
        if min_ <= rounded <= max_:
            if rounded not in positions:
                positions.append(rounded)
        position += step
    if len(positions) < 2:
        return [min_, max_]
    return positions


def text_len(lenght, fs):
    """Approximation of text length"""
    return lenght * 0.6 * fs


def get_text_box(text, fs):
    """Approximation of text bounds"""
    return (fs, text_len(len(text), fs))


def get_texts_box(texts, fs):
    """Approximation of multiple texts bounds"""
    max_len = max(map(len, texts))
    return (fs, text_len(max_len, fs))


def decorate(svg, node, metadata):
    """Add metedata next to a node"""
    if hasattr(metadata, 'xlink'):
        xlink = metadata.xlink
        if not isinstance(xlink, dict):
            xlink = {'href': xlink, 'target': '_blank'}
        node = svg.node(node, 'a', **xlink)
    for key in dir(metadata):
        if key not in ('value') and not key.startswith('_'):
            value = getattr(metadata, key)
            if key == 'xlink' and isinstance(value, dict):
                value = value.get('href', value)
            if value:
                svg.node(node, 'desc', class_=key).text = str(value)
    return node


def cycle_fill(short_list, max_len):
    """Fill a list to max_len using a cycle of it"""
    short_list = list(short_list)
    list_cycle = cycle(short_list)
    while len(short_list) < 16:
        short_list.append(list_cycle.next())
    return short_list


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
