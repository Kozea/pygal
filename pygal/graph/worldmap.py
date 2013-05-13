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
from pygal.util import cut
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
    _adapters = [positive, none_to_zero]

    def _plot(self):
        map = etree.fromstring(MAP)
        map.set('width', str(self.view.width))
        map.set('height', str(self.view.height))
        sum_ = sum(cut(cut(self.series, 'values')))

        for i, serie in enumerate(self.series):
            ratio = serie.values[0] / self._max
            perc = serie.values[0] / sum_ if sum_ != 0 else 0
            country = map.find('.//*[@id="%s"]' % serie.title)
            if country is None:
                continue
            country.set(
                'style', 'fill-opacity: %f' % (
                    ratio))
            title = country[0]
            title.text = (title.text or '?') + ': %d (%s)' % (
                serie.values[0], '{0:.2%}'.format(perc))

        self.nodes['plot'].append(map)
