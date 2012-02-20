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
from pygal.graph.graph import Graph
from math import cos, sin, pi


class Pie(Graph):
    """Pie graph"""

    def slice(self, serie_node, start_angle, angle, perc,
            small=False):
        slices = self.svg.node(serie_node, class_="slices")
        slice_ = self.svg.node(slices, class_="slice")
        center = ((self.width - self.margin.x) / 2.,
                  (self.height - self.margin.y) / 2.)
        r = min(center)
        if small:
            r *= .9
        center_str = '%f %f' % center
        if perc == 1:
            self.svg.node(slice_, 'circle',
                          cx=center[0],
                          cy=center[1],
                          r=r,
                          class_='slice')
        else:
            rxy = '%f %f' % tuple([r] * 2)
            to = '%f %f' % (r * sin(angle), r * (1 - cos(angle)))
            self.svg.node(slice_, 'path',
                          d='M%s v%f a%s 0 %d 1 %s z' % (
                              center_str, -r,
                              rxy,
                              1 if angle > pi else 0,
                              to),
                          transform='rotate(%f %s)' % (
                              start_angle * 180 / pi, center_str),
                          class_='slice')
        text_angle = pi / 2. - (start_angle + angle / 2.)
        text_r = min(center) * .8
        self.svg.node(slice_, 'text',
                  x=center[0] + text_r * cos(text_angle),
                  y=center[1] - text_r * sin(text_angle),
              ).text = '{:.2%}'.format(perc)

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
                for val in serie.values:
                    small_angle = 2 * pi * val / total
                    self.slice(
                        self._serie(serie.index),
                        small_current_angle,
                        small_angle, val / total, True)
                    small_current_angle += small_angle
            current_angle += angle
