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
Gauge chart

"""

from __future__ import division
from pygal.util import decorate, compute_scale
from pygal.view import PolarThetaView, PolarThetaLogView
from pygal.graph.graph import Graph


class Gauge(Graph):
    """Gauge graph"""

    def _set_view(self):
        if self.logarithmic:
            view_class = PolarThetaLogView
        else:
            view_class = PolarThetaView

        self.view = view_class(
            self.width - self.margin.x,
            self.height - self.margin.y,
            self._box)

    def needle(self, serie):
        serie_node = self.svg.serie(serie)
        for i, theta in enumerate(serie.values):
            if theta is None:
                continue
            fmt = lambda x: '%f %f' % x
            value = self._format(serie.values[i])
            metadata = serie.metadata.get(i)
            gauges = decorate(
                self.svg,
                self.svg.node(serie_node['plot'], class_="dots"),
                metadata)

            self.svg.node(
                gauges, 'polygon', points=' '.join([
                    fmt(self.view((0, 0))),
                    fmt(self.view((.75, theta))),
                    fmt(self.view((.8, theta))),
                    fmt(self.view((.75, theta)))]),
                class_='line reactive tooltip-trigger')

            x, y = self.view((.75, theta))
            self._tooltip_data(gauges, value, x, y)
            self._static_value(serie_node, value, x, y)

    def _x_axis(self, draw_axes=True):
        axis = self.svg.node(self.nodes['plot'], class_="axis x gauge")

        for i, (label, theta) in enumerate(self._x_labels):
            guides = self.svg.node(axis, class_='guides')

            self.svg.line(
                guides, [self.view((.95, theta)), self.view((1, theta))],
                close=True,
                class_='line')

            self.svg.line(
                guides, [self.view((0, theta)), self.view((.95, theta))],
                close=True,
                class_='guide line %s' % (
                    'major' if i in (0, len(self._x_labels) - 1)
                    else ''))

            x, y = self.view((.9, theta))
            self.svg.node(
                guides, 'text',
                x=x,
                y=y
            ).text = label

    def _y_axis(self, draw_axes=True):
        axis = self.svg.node(self.nodes['plot'], class_="axis y gauge")
        x, y = self.view((0, 0))
        self.svg.node(axis, 'circle', cx=x, cy=y, r=4)

    def _compute(self):
        self.min_ = self._min or 0
        self.max_ = self._max or 0
        if self.max_ - self.min_ == 0:
            self.min_ -= 1
            self.max_ += 1

        self._box.set_polar_box(
            0, 1,
            self.min_,
            self.max_)
        x_pos = compute_scale(
            self.min_, self.max_, self.logarithmic, self.order_min
        )
        self._x_labels = list(zip(map(self._format, x_pos), x_pos))

    def _plot(self):
        for serie in self.series:
            self.needle(serie)
