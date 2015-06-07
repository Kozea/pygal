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
Worldmap chart

"""

from __future__ import division
from pygal.util import cached_property
from pygal.graph.map import BaseMap
from pygal.i18n import COUNTRIES, SUPRANATIONAL
import os

from .maps.worldmap_svg import data as WORLD_MAP

class Worldmap(BaseMap):
    """Worldmap graph"""
    x_labels = list(COUNTRIES.keys())
    area_names = COUNTRIES
    area_prefix = ''
    svg_map = WORLD_MAP
    kind = 'country'

    @cached_property
    def countries(self):
        return [val[0]
                for serie in self.all_series
                for val in serie.values
                if val[0] is not None]

    @cached_property
    def _values(self):
        """Getter for series values (flattened)"""
        return [val[1]
                for serie in self.series
                for val in serie.values
                if val[1] is not None]


class SupranationalWorldmap(Worldmap):
    """SupranationalWorldmap graph"""
    x_labels = list(SUPRANATIONAL.keys())

    def enumerate_values(self, serie):
        """Replaces the values if it contains a supranational code."""
        for i, (code, value) in enumerate(serie.values):
            for subcode in SUPRANATIONAL.get(code, []):
                yield i, (subcode, value)
