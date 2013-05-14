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
Worldmap chart

"""

from __future__ import division
from pygal.util import cut, cached_property
from pygal.graph.graph import Graph
from pygal.adapters import positive, none_to_zero
from lxml import etree
import os

with open(os.path.join(
        os.path.dirname(__file__),
        'worldmap.svg')) as file:
    MAP = file.read()


class Worldmap(Graph):
    """Worldmap graph"""
    _dual = True

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

    def _plot(self):
        map = etree.fromstring(MAP)
        map.set('width', str(self.view.width))
        map.set('height', str(self.view.height))

        for i, serie in enumerate(self.series):
            min_ = min(cut(serie.values, 1))
            max_ = max(cut(serie.values, 1))
            for country, value in serie.values:
                if value is None:
                    continue
                ratio = value / (max_ - min_)
                country = map.find('.//*[@id="%s"]' % country)
                if country is None:
                    continue
                cls = country.get('class', '').split(' ')
                cls.append('color-%d' % i)
                country.set('class', ' '.join(cls))
                country.set(
                    'style', 'fill-opacity: %f' % (
                        ratio))
                title = country[0]
                title.text = (title.text or '?') + ': %d' % value

        self.nodes['plot'].append(map)
