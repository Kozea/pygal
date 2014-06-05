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
from pygal.util import cut, cached_property, decorate
from pygal.graph.graph import Graph
from pygal.i18n import COUNTRIES
from pygal.etree import etree
import os

with open(os.path.join(
        os.path.dirname(__file__),
        'worldmap.svg')) as file:
    MAP = file.read()


class Worldmap(Graph):
    """Worldmap graph"""
    _dual = True
    x_labels = list(COUNTRIES.keys())
    country_names = COUNTRIES

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
            safe_vals = list(filter(
                lambda x: x is not None, cut(serie.values, 1)))
            if not safe_vals:
                continue
            min_ = min(safe_vals)
            max_ = max(safe_vals)
            for j, (country_code, value) in enumerate(serie.values):
                if value is None:
                    continue
                if max_ == min_:
                    ratio = 1
                else:
                    ratio = .3 + .7 * (value - min_) / (max_ - min_)

                try:
                    country = map.find('.//*[@id="%s"]' % country_code)
                except SyntaxError:
                    # Python 2.6 (you'd better install lxml)
                    country = None
                    for e in map:
                        if e.attrib.get('id', '') == country_code:
                            country = e

                if country is None:
                    continue
                cls = country.get('class', '').split(' ')
                cls.append('color-%d' % i)
                country.set('class', ' '.join(cls))
                country.set(
                    'style', 'fill-opacity: %f' % (
                        ratio))

                metadata = serie.metadata.get(j)
                if metadata:
                    node = decorate(self.svg, country, metadata)
                    if node != country:
                        country.remove(node)
                        index = list(map).index(country)
                        map.remove(country)
                        node.append(country)
                        map.insert(index, node)

                last_node = len(country) > 0 and country[-1]
                if last_node is not None and last_node.tag == 'title':
                    title_node = last_node
                    text = title_node.text + '\n'
                else:
                    title_node = self.svg.node(country, 'title')
                    text = ''
                title_node.text = text + '[%s] %s: %s' % (
                    serie.title,
                    self.country_names[country_code], self._format(value))

        self.nodes['plot'].append(map)
