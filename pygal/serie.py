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
Little helpers for series
"""


class Serie(object):
    """Serie containing title, values and the graph serie index"""
    def __init__(self, title, values, index):
        self.title = title
        if isinstance(values, dict) or not hasattr(values, '__iter__'):
            values = [values]
        self.metadata = map(Value, values)
        self.values = [value.value for value in self.metadata]
        self.index = index


class Value(object):
    def __init__(self, value):
        if not isinstance(value, dict):
            value = {'value': value}
        self.__dict__.update(value)


class Label(object):
    """A label with his position"""
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
