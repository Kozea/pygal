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
Little helpers for series

"""
from pygal.util import cached_property, cut
from math import fsum, sqrt


class Serie(object):
    """Serie containing title, values and the graph serie index"""
    def __init__(self, title, values, metadata=None, parent=None, dual=False):
        self.title = title
        self._values = values
        self.metadata = metadata or {}
        self.parent = parent
        self.dual = dual


    @cached_property
    def values(self):
        if self.dual:
            return cut(self._values)
        return self._values

    @cached_property
    def safe_values(self):
        return list(filter(lambda x: x is not None, self.values))

    @cached_property
    def min(self):
        """Returns the lowest value of the serie."""
        return min([val.min if isinstance(val, NestedSerie) else val
                    for val in self.values if val is not None] or [None])

    @cached_property
    def max(self):
        """Returns the lowest value of the serie."""
        return max([val.max if isinstance(val, NestedSerie) else val
                    for val in self.values if val is not None] or [None])

    @cached_property
    def length(self):
        """Returns the serie size."""
        return len(self.values)

    @cached_property
    def has_data(self):
        """True if data is provided."""
        datalen = len(self.safe_values)
        total = 0
        for v in self.safe_values:
            if v:
                if isinstance(v, NestedSerie):
                    total += v.abs
                elif isinstance(v, tuple):
                    total += any([abs(v[0] or 0) != 0, abs(v[1] or 0) != 0])
                else:
                    total += abs(v)
        return datalen and total != 0


class NestedSerie(Serie):
    """Class that handles nested series."""
    @cached_property
    def mean(self):
        """Returns the average on the serie (mean)."""
        return fsum([v for v in self.values]) / self.length

    @cached_property
    def variance(self):
        """Returns the variance for the serie."""
        return 1/self.length * fsum((v-self.mean) ** 2 for v in self.values)

    @cached_property
    def deviation(self):
        """Returns the deviation for the serie."""
        return sqrt(self.variance)

    @cached_property
    def min(self):
        """Returns the lowest value of the serie."""
        return self.mean - self.deviation

    @cached_property
    def max(self):
        """Returns the lowest value of the serie."""
        return self.mean + self.deviation

    @cached_property
    def abs(self):
        """Returns the absolute value of the serie."""
        return abs(self.mean)


class Label(object):
    """A label with his position"""
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
