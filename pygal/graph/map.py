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

"""
pygal contains no map but a base class to create extension
see the pygal_maps_world package to get an exemple.
https://github.com/Kozea/pygal_maps_world
"""

from __future__ import division
from pygal.graph.graph import Graph
from pygal.util import cut, cached_property, decorate
from pygal.etree import etree


class BaseMap(Graph):

    """Base class for maps"""

    _dual = True

    @cached_property
    def _values(self):
        """Getter for series values (flattened)"""
        return [val[1]
                for serie in self.series
                for val in serie.values
                if val[1] is not None]

    def enumerate_values(self, serie):
        """Hook to replace default enumeration on values"""
        return enumerate(serie.values)

    def adapt_code(self, area_code):
        """Hook to change the area code"""
        return area_code

    def _plot(self):
        """Insert a map in the chart and apply data on it"""
        map = etree.fromstring(self.svg_map)
        map.set('width', str(self.view.width))
        map.set('height', str(self.view.height))

        for i, serie in enumerate(self.series):
            safe_vals = list(filter(
                lambda x: x is not None, cut(serie.values, 1)))
            if not safe_vals:
                continue
            min_ = min(safe_vals)
            max_ = max(safe_vals)
            for j, (area_code, value) in self.enumerate_values(serie):
                area_code = self.adapt_code(area_code)
                if value is None:
                    continue
                if max_ == min_:
                    ratio = 1
                else:
                    ratio = .3 + .7 * (value - min_) / (max_ - min_)

                try:
                    areae = map.findall(
                        ".//*[@class='%s%s %s map-element']" % (
                            self.area_prefix, area_code,
                            self.kind))
                except SyntaxError:
                    # Python 2.6 (you'd better install lxml)
                    raise ImportError('lxml is required under python 2.6')

                if not areae:
                    continue

                for area in areae:
                    cls = area.get('class', '').split(' ')
                    cls.append('color-%d' % i)
                    area.set('class', ' '.join(cls))
                    area.set('style', 'fill-opacity: %f' % (ratio))

                    metadata = serie.metadata.get(j)
                    if metadata:
                        node = decorate(self.svg, area, metadata)
                        if node != area:
                            area.remove(node)
                            for g in map:
                                if area not in g:
                                    continue
                                index = list(g).index(area)
                                g.remove(area)
                                node.append(area)
                                g.insert(index, node)

                    last_node = len(area) > 0 and area[-1]
                    if last_node is not None and last_node.tag == 'title':
                        title_node = last_node
                        text = title_node.text + '\n'
                    else:
                        title_node = self.svg.node(area, 'title')
                        text = ''

                    title_node.text = text + '[%s] %s: %s' % (
                        serie.title,
                        self.area_names[area_code], self._format(value))

        self.nodes['plot'].append(map)
