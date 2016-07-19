# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2016 Kozea
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

"""Gauge chart representing values as needles on a polar scale"""

from __future__ import division

from pygal._compat import is_str
from pygal.graph.graph import Graph
from pygal.util import alter, compute_scale, cut, decorate
from pygal.view import PolarThetaLogView, PolarThetaView


class Gauge(Graph):

    """Gauge graph class"""

    needle_width = 1 / 20

    def _set_view(self):
        """Assign a view to current graph"""
        if self.logarithmic:
            view_class = PolarThetaLogView
        else:
            view_class = PolarThetaView

        self.view = view_class(
            self.width - self.margin_box.x,
            self.height - self.margin_box.y,
            self._box)

    def needle(self, serie):
        """Draw a needle for each value"""
        serie_node = self.svg.serie(serie)
        for i, theta in enumerate(serie.values):
            if theta is None:
                continue

            def point(x, y):
                return '%f %f' % self.view((x, y))

            val = self._format(serie, i)
            metadata = serie.metadata.get(i)
            gauges = decorate(
                self.svg,
                self.svg.node(serie_node['plot'], class_="dots"),
                metadata)

            tolerance = 1.15

            if theta < self._min:
                theta = self._min * tolerance

            if theta > self._max:
                theta = self._max * tolerance

            w = (self._box._tmax - self._box._tmin + self.view.aperture) / 4

            if self.logarithmic:
                w = min(w, self._min - self._min * 10 ** -10)

            alter(
                self.svg.node(
                    gauges, 'path', d='M %s L %s A %s 1 0 1 %s Z' % (
                        point(.85, theta),
                        point(self.needle_width, theta - w),
                        '%f %f' % (self.needle_width, self.needle_width),
                        point(self.needle_width, theta + w),
                    ),
                    class_='line reactive tooltip-trigger'),
                metadata)

            x, y = self.view((.75, theta))
            self._tooltip_data(
                gauges, val, x, y,
                xlabel=self._get_x_label(i))
            self._static_value(serie_node, val, x, y, metadata)

    def _y_axis(self, draw_axes=True):
        """Override y axis to plot a polar axis"""
        axis = self.svg.node(self.nodes['plot'], class_="axis x gauge")

        for i, (label, theta) in enumerate(self._y_labels):
            guides = self.svg.node(axis, class_='guides')

            self.svg.line(
                guides, [self.view((.95, theta)), self.view((1, theta))],
                close=True,
                class_='line')

            self.svg.line(
                guides, [self.view((0, theta)), self.view((.95, theta))],
                close=True,
                class_='guide line %s' % (
                    'major' if i in (0, len(self._y_labels) - 1)
                    else ''))

            x, y = self.view((.9, theta))
            self.svg.node(
                guides, 'text',
                x=x,
                y=y
            ).text = label

            self.svg.node(
                guides, 'title',
            ).text = self._y_format(theta)

    def _x_axis(self, draw_axes=True):
        """Override x axis to put a center circle in center"""
        axis = self.svg.node(self.nodes['plot'], class_="axis y gauge")
        x, y = self.view((0, 0))
        self.svg.node(axis, 'circle', cx=x, cy=y, r=4)

    def _compute(self):
        """Compute y min and max and y scale and set labels"""
        self.min_ = self._min or 0
        self.max_ = self._max or 0
        if self.max_ - self.min_ == 0:
            self.min_ -= 1
            self.max_ += 1

        self._box.set_polar_box(
            0, 1,
            self.min_,
            self.max_)

    def _compute_x_labels(self):
        pass

    def _compute_y_labels(self):
        y_pos = compute_scale(
            self.min_, self.max_, self.logarithmic,
            self.order_min, self.min_scale, self.max_scale
        )
        if self.y_labels:
            self._y_labels = []
            for i, y_label in enumerate(self.y_labels):
                if isinstance(y_label, dict):
                    pos = self._adapt(y_label.get('value'))
                    title = y_label.get('label', self._y_format(pos))
                elif is_str(y_label):
                    pos = self._adapt(y_pos[i])
                    title = y_label
                else:
                    pos = self._adapt(y_label)
                    title = self._y_format(pos)
                self._y_labels.append((title, pos))
            self.min_ = min(self.min_, min(cut(self._y_labels, 1)))
            self.max_ = max(self.max_, max(cut(self._y_labels, 1)))
            self._box.set_polar_box(
                0, 1,
                self.min_,
                self.max_)
        else:
            self._y_labels = list(zip(map(self._y_format, y_pos), y_pos))

    def _plot(self):
        """Plot all needles"""
        for serie in self.series:
            self.needle(serie)
