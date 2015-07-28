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

"""Various utility functions"""

from __future__ import division

import re
from decimal import Decimal

from math import ceil, floor, log, log10, pi

from pygal._compat import is_list_like, to_unicode, u


ORDERS = u("yzafpnµm kMGTPEZY")


def float_format(number):
    """Format a float to a precision of 3, without zeroes or dots"""
    return ("%.3f" % number).rstrip('0').rstrip('.')


def humanize(number):
    """Format a number to engineer scale"""
    if is_list_like(number):
        return', '.join(map(humanize, number))
    if number is None:
        return u('∅')
    order = number and int(floor(log(abs(number)) / log(1000)))
    human_readable = ORDERS.split(" ")[int(order > 0)]
    if order == 0 or order > len(human_readable):
        return float_format(number / (1000 ** int(order)))
    return (
        float_format(number / (1000 ** int(order))) +
        human_readable[int(order) - int(order > 0)])


def majorize(values):
    """Filter sequence to return only major considered numbers"""
    sorted_values = sorted(values)
    if len(values) <= 3 or (
            abs(2 * sorted_values[1] - sorted_values[0] - sorted_values[2]) >
            abs(1.5 * (sorted_values[1] - sorted_values[0]))):
        return []
    values_step = sorted_values[1] - sorted_values[0]
    full_range = sorted_values[-1] - sorted_values[0]
    step = 10 ** int(log10(full_range))
    if step == values_step:
        step *= 10
    step_factor = 10 ** (int(log10(step)) + 1)
    if round(step * step_factor) % (round(values_step * step_factor) or 1):
        # TODO: Find lower common multiple instead
        step *= values_step
    if full_range <= 2 * step:
        step *= .5
    elif full_range >= 5 * step:
        step *= 5
    major_values = [
        value for value in values if value / step == round(value / step)]
    return [value for value in sorted_values if value in major_values]


def round_to_int(number, precision):
    """Round a number to a precision"""
    precision = int(precision)
    rounded = (int(number) + precision / 2) // precision * precision
    return rounded


def round_to_float(number, precision):
    """Round a float to a precision"""
    rounded = Decimal(
        str(floor((number + precision / 2) // precision))
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
    return list(map(cut_, list_))


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


swap = lambda tuple_: tuple(reversed(tuple_))
ident = lambda x: x


def compute_logarithmic_scale(min_, max_, min_scale, max_scale):
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
    while amplitude * detail < min_scale * 5:
        detail *= 2
    while amplitude * detail > max_scale * 3:
        detail /= 2
    for order in range(min_order, max_order + 1):
        for i in range(int(detail)):
            tick = (10 * i / detail or 1) * 10 ** order
            tick = round_to_scale(tick, tick)
            if min_ <= tick <= max_ and tick not in positions:
                positions.append(tick)
    return positions


def compute_scale(
        min_, max_, logarithmic, order_min,
        min_scale, max_scale):
    """Compute an optimal scale between min and max"""
    if min_ == 0 and max_ == 0:
        return [0]
    if max_ - min_ == 0:
        return [min_]
    if logarithmic:
        log_scale = compute_logarithmic_scale(
            min_, max_, min_scale, max_scale)
        if log_scale:
            return log_scale
            # else we fallback to normal scalling

    order = round(log10(max(abs(min_), abs(max_)))) - 1
    if order_min is not None and order < order_min:
        order = order_min
    else:
        while ((max_ - min_) / (10 ** order) < min_scale and
               (order_min is None or order > order_min)):
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


def text_len(length, fs):
    """Approximation of text width"""
    return length * 0.6 * fs


def reverse_text_len(width, fs):
    """Approximation of text length"""
    return int(width / (0.6 * fs))


def get_text_box(text, fs):
    """Approximation of text bounds"""
    return (fs, text_len(len(text), fs))


def get_texts_box(texts, fs):
    """Approximation of multiple texts bounds"""
    max_len = max(map(len, texts))
    return (fs, text_len(max_len, fs))


def decorate(svg, node, metadata):
    """Add metedata next to a node"""
    if not metadata:
        return node
    xlink = metadata.get('xlink')
    if xlink:
        if not isinstance(xlink, dict):
            xlink = {'href': xlink, 'target': '_blank'}
        node = svg.node(node, 'a', **xlink)
        svg.node(node, 'desc', class_='xlink').text = to_unicode(
            xlink.get('href'))

    if 'tooltip' in metadata:
        svg.node(node, 'title').text = to_unicode(
            metadata['tooltip'])

    if 'color' in metadata:
        color = metadata.pop('color')
        node.attrib['style'] = 'fill: %s; stroke: %s' % (
            color, color)

    if 'style' in metadata:
        node.attrib['style'] = metadata.pop('style')

    if 'label' in metadata:
        svg.node(node, 'desc', class_='label').text = to_unicode(
            metadata['label'])

    return node


def alter(node, metadata):
    """Override nodes attributes from metadata node mapping"""
    if node is not None and metadata and 'node' in metadata:
        node.attrib.update(
            dict((k, str(v)) for k, v in metadata['node'].items()))


def truncate(string, index):
    """Truncate a string at index and add ..."""
    if len(string) > index and index > 0:
        string = string[:index - 1] + u('…')
    return string


# # Stolen partly from brownie http://packages.python.org/Brownie/
class cached_property(object):

    """Memoize a property"""

    def __init__(self, getter, doc=None):
        """Initialize the decorator"""
        self.getter = getter
        self.__module__ = getter.__module__
        self.__name__ = getter.__name__
        self.__doc__ = doc or getter.__doc__

    def __get__(self, obj, type_=None):
        """
        Get descriptor calling the property function and replacing it with
        its value or on state if we are in the transient state.
        """
        if obj is None:
            return self
        value = self.getter(obj)
        if hasattr(obj, 'state'):
            setattr(obj.state, self.__name__, value)
        else:
            obj.__dict__[self.__name__] = self.getter(obj)
        return value

css_comments = re.compile(r'/\*.*?\*/', re.MULTILINE | re.DOTALL)


def minify_css(css):
    """Little css minifier"""
    # Inspired by slimmer by Peter Bengtsson
    remove_next_comment = 1
    for css_comment in css_comments.findall(css):
        if css_comment[-3:] == '\*/':
            remove_next_comment = 0
            continue
        if remove_next_comment:
            css = css.replace(css_comment, '')
        else:
            remove_next_comment = 1

    # >= 2 whitespace becomes one whitespace
    css = re.sub(r'\s\s+', ' ', css)
    # no whitespace before end of line
    css = re.sub(r'\s+\n', '', css)
    # Remove space before and after certain chars
    for char in ('{', '}', ':', ';', ','):
        css = re.sub(char + r'\s', char, css)
        css = re.sub(r'\s' + char, char, css)
    css = re.sub(r'}\s(#|\w)', r'}\1', css)
    # no need for the ; before end of attributes
    css = re.sub(r';}', r'}', css)
    css = re.sub(r'}//-->', r'}\n//-->', css)
    return css.strip()


def compose(f, g):
    """Chain functions"""
    fun = lambda *args, **kwargs: f(g(*args, **kwargs))
    fun.__name__ = "%s o %s" % (f.__name__, g.__name__)
    return fun


def safe_enumerate(iterable):
    """Enumerate which does not yield None values"""
    for i, v in enumerate(iterable):
        if v is not None:
            yield i, v


def split_title(title, width, title_fs):
    """Split a string for a specified width and font size"""
    titles = []
    if not title:
        return titles
    size = reverse_text_len(width, title_fs * 1.1)
    title_lines = title.split("\n")
    for title_line in title_lines:
        while len(title_line) > size:
            title_part = title_line[:size]
            i = title_part.rfind(' ')
            if i == -1:
                i = len(title_part)
            titles.append(title_part[:i])
            title_line = title_line[i:].strip()
        titles.append(title_line)
    return titles
