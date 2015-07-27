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
Pie chart: A circular chart divided into slice to illustrate proportions
It can be made as a donut or a half pie.
"""

from __future__ import division

from math import pi

from pygal.adapters import none_to_zero, positive
from pygal.graph.graph import Graph
from pygal.util import alter, decorate


class Pie(Graph):

    """Pie graph class"""

    _adapters = [positive, none_to_zero]

    @property
    def _format(self):
        """Return the value formatter for this graph"""
        def percentage_formatter(y, self=self):
            total = sum(map(sum, map(lambda x: x.values, self.series)))
            perc = y/total
            return '{0:.2%}'.format(perc)
        return self.value_formatter or percentage_formatter

    def slice(self, serie, start_angle, total):
        """Make a serie slice"""
        serie_node = self.svg.serie(serie)
        dual = self._len > 1 and not self._order == 1

        slices = self.svg.node(serie_node['plot'], class_="slices")
        serie_angle = 0
        total_perc = 0
        original_start_angle = start_angle
        if self.half_pie:
            center = ((self.width - self.margin_box.x) / 2.,
                      (self.height - self.margin_box.y) / 1.25)
        else:
            center = ((self.width - self.margin_box.x) / 2.,
                      (self.height - self.margin_box.y) / 2.)

        radius = min(center)
        for i, val in enumerate(serie.values):
            perc = val / total
            if self.half_pie:
                angle = 2 * pi * perc / 2
            else:
                angle = 2 * pi * perc
            serie_angle += angle
            val = self._format(val)
            metadata = serie.metadata.get(i)
            slice_ = decorate(
                self.svg,
                self.svg.node(slices, class_="slice"),
                metadata)
            if dual:
                small_radius = radius * .9
                big_radius = radius
            else:
                big_radius = radius * .9
                small_radius = radius * serie.inner_radius

            alter(self.svg.slice(
                serie_node, slice_, big_radius, small_radius,
                angle, start_angle, center, val, i, metadata), metadata)
            start_angle += angle
            total_perc += perc

        if dual:
            val = self._format(total_perc*total)
            self.svg.slice(serie_node,
                           self.svg.node(slices, class_="big_slice"),
                           radius * .9, 0, serie_angle,
                           original_start_angle, center, val, i, metadata)
        return serie_angle

    def _compute_x_labels(self):
        pass

    def _compute_y_labels(self):
        pass

    def _plot(self):
        """Draw all the serie slices"""
        total = sum(map(sum, map(lambda x: x.values, self.series)))
        if total == 0:
            return
        if self.half_pie:
            current_angle = 3*pi/2
        else:
            current_angle = 0

        for index, serie in enumerate(self.series):
            angle = self.slice(serie, current_angle, total)
            current_angle += angle
