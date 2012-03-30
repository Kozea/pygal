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
from __future__ import division
from pygal.graph.graph import Graph
from math import cos, sin, pi
project = lambda rho, alpha: (
    rho * sin(-alpha), rho * cos(-alpha))
diff = lambda x, y: (x[0] - y[0], x[1] - y[1])
fmt = lambda x: '%f %f' % x
get_radius = lambda r: fmt(tuple([r] * 2))


class Pie(Graph):
    """Pie graph"""

    def slice(self, serie_node, start_angle, angle, perc,
            small=False):
        val = '{0:.2%}'.format(perc)
        slices = self.svg.node(serie_node['plot'], class_="slices")
        slice_ = self.svg.node(slices, class_="slice")
        center = ((self.width - self.margin.x) / 2.,
                  (self.height - self.margin.y) / 2.)
        r = min(center)
        if small:
            small_r = r * .9
        else:
            r = r * .9
            small_r = 0
        if perc == 1:
            self.svg.node(slice_, 'circle',
                          cx=center[0],
                          cy=center[1],
                          r=r,
                          class_='slice reactive tooltip-trigger')
        else:
            absolute_project = lambda rho, theta: fmt(
                diff(center, project(rho, theta)))
            to1 = absolute_project(r, start_angle)
            to2 = absolute_project(r, start_angle + angle)
            to3 = absolute_project(small_r, start_angle + angle)
            to4 = absolute_project(small_r, start_angle)
            self.svg.node(slice_, 'path',
                          d='M%s A%s 0 %d 1 %s L%s A%s 0 %d 0 %s z' % (
                              to1,
                              get_radius(r), int(angle > pi), to2,
                              to3,
                              get_radius(small_r), int(angle > pi), to4),
                          class_='slice reactive tooltip-trigger')
        self.svg.node(slice_, 'desc', class_="value").text = val
        tooltip_position = map(
            str, diff(center, project(
                (r + small_r) / 2, start_angle + angle / 2)))
        self.svg.node(slice_, 'desc',
                      class_="x centered").text = tooltip_position[0]
        self.svg.node(slice_, 'desc',
                      class_="y centered").text = tooltip_position[1]
        if self.print_values:
            self.svg.node(
                serie_node['text_overlay'], 'text',
                class_='centered',
                x=tooltip_position[0],
                y=tooltip_position[1]
            ).text = val if self.print_zeroes or val != '0%' else ''

    def _compute(self):
        for serie in self.series:
            serie.values = map(lambda x: max(x, 0), serie.values)
        return super(Pie, self)._compute()

    def _plot(self):
        total = float(sum(map(sum, map(lambda x: x.values, self.series))))

        if total == 0:
            return
        current_angle = 0
        for serie in self.series:
            angle = 2 * pi * sum(serie.values) / total
            self.slice(
                self._serie(serie.index),
                current_angle,
                angle, sum(serie.values) / total)
            if len(serie.values) > 1:
                small_current_angle = current_angle
                for i, val in enumerate(serie.values):
                    small_angle = 2 * pi * val / total
                    self.slice(
                        self._serie(serie.index),
                        small_current_angle,
                        small_angle, val / total,
                        True)
                    small_current_angle += small_angle
            current_angle += angle
