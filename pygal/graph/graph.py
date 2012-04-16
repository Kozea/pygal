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
Commmon graphing functions

"""

from __future__ import division
from pygal.interpolate import interpolation
from pygal.graph.base import BaseGraph
from pygal.view import View, LogView
from pygal.util import is_major
from math import isnan, pi


class Graph(BaseGraph):
    """Graph super class containing generic common functions"""

    def _decorate(self):
        """Draw all decorations"""
        self._set_view()
        self._make_graph()
        self._axes()
        self._legend()
        self._title()

    def _axes(self):
        """Draw axes"""
        self._x_axis()
        self._y_axis()

    def _set_view(self):
        """Assign a view to current graph"""
        self.view = (LogView if self.logarithmic else View)(
            self.width - self.margin.x,
            self.height - self.margin.y,
            self._box)

    def _make_graph(self):
        """Init common graph svg structure"""
        self.nodes['graph'] = self.svg.node(
            class_='graph %s-graph %s' % (
                self.__class__.__name__.lower(),
            'horizontal' if self.horizontal else 'vertical'))
        self.svg.node(self.nodes['graph'], 'rect',
                  class_='background',
                  x=0, y=0,
                  width=self.width,
                  height=self.height)
        self.nodes['plot'] = self.svg.node(
            self.nodes['graph'], class_="plot",
            transform="translate(%d, %d)" % (
                self.margin.left, self.margin.top))
        self.svg.node(self.nodes['plot'], 'rect',
                  class_='background',
                  x=0, y=0,
                  width=self.view.width,
                  height=self.view.height)
        self.nodes['overlay'] = self.svg.node(
            self.nodes['graph'], class_="plot overlay",
            transform="translate(%d, %d)" % (
                self.margin.left, self.margin.top))
        self.nodes['text_overlay'] = self.svg.node(
            self.nodes['graph'], class_="plot text-overlay",
            transform="translate(%d, %d)" % (
                self.margin.left, self.margin.top))
        self.nodes['tooltip_overlay'] = self.svg.node(
            self.nodes['graph'], class_="plot tooltip-overlay",
            transform="translate(%d, %d)" % (
                self.margin.left, self.margin.top))
        self.nodes['tooltip'] = self.svg.node(
            self.nodes['tooltip_overlay'],
            id="tooltip",
            transform='translate(0 0)')

        a = self.svg.node(self.nodes['tooltip'], 'a')
        self.svg.node(a, 'rect',
                      id="tooltip-box",
                      rx=5, ry=5,
        )
        text = self.svg.node(a, 'text', class_='text')
        self.svg.node(text, 'tspan', class_='label')
        self.svg.node(text, 'tspan', class_='value')

    def _x_axis(self, draw_axes=True):
        """Make the x axis: labels and guides"""
        if not self._x_labels:
            return

        axis = self.svg.node(self.nodes['plot'], class_="axis x")

        if 0 not in [label[1] for label in self._x_labels] and draw_axes:
            self.svg.node(axis, 'path',
                      d='M%f %f v%f' % (0, 0, self.view.height),
                      class_='line')
        for label, position in self._x_labels:
            guides = self.svg.node(axis, class_='guides')
            x = self.view.x(position)
            y = self.view.height + 5
            if draw_axes:
                self.svg.node(
                    guides, 'path',
                    d='M%f %f v%f' % (x, 0, self.view.height),
                    class_='%sline' % (
                    'guide ' if position != 0 else ''))
            text = self.svg.node(guides, 'text',
                             x=x,
                             y=y + .5 * self.label_font_size + 5
            )
            text.text = label
            if self.x_label_rotation:
                text.attrib['transform'] = "rotate(%d %f %f)" % (
                    self.x_label_rotation, x, y)

    def _y_axis(self, draw_axes=True):
        """Make the y axis: labels and guides"""
        if not self._y_labels:
            return

        axis = self.svg.node(self.nodes['plot'], class_="axis y")

        if 0 not in [label[1] for label in self._y_labels] and draw_axes:
            self.svg.node(axis, 'path',
                      d='M%f %f h%f' % (0, self.view.height, self.view.width),
                      class_='line')
        for label, position in self._y_labels:
            major = is_major(position)
            guides = self.svg.node(axis, class_='%sguides' % (
                'logarithmic ' if self.logarithmic else ''
            ))
            x = -5
            y = self.view.y(position)
            if draw_axes:
                self.svg.node(
                    guides, 'path',
                    d='M%f %f h%f' % (0, y, self.view.width),
                    class_='%s%sline' % (
                        'major ' if major else '',
                        'guide ' if position != 0 else ''))
            text = self.svg.node(guides, 'text',
                                 x=x,
                                 y=y + .35 * self.label_font_size,
                                 class_='major' if major else ''
            )
            text.text = label
            if self.y_label_rotation:
                text.attrib['transform'] = "rotate(%d %f %f)" % (
                    self.y_label_rotation, x, y)

    def _legend(self):
        """Make the legend box"""
        if not self.show_legend:
            return
        legends = self.svg.node(
            self.nodes['graph'], class_='legends',
            transform='translate(%d, %d)' % (
                self.margin.left + self.view.width + 10,
                self.margin.top + 10))
        for i, title in enumerate(self._legends):
            legend = self.svg.node(
                legends, class_='legend reactive activate-serie',
                id="activate-serie-%d" % i)
            self.svg.node(
                legend, 'rect',
                x=0,
                y=1.5 * i * self.legend_box_size,
                width=self.legend_box_size,
                height=self.legend_box_size,
                class_="color-%d reactive" % i
            ).text = title
            # Serious magical numbers here
            self.svg.node(
                legend, 'text',
                x=self.legend_box_size + 5,
                y=1.5 * i * self.legend_box_size
                + .5 * self.legend_box_size
                + .3 * self.legend_font_size
            ).text = title

    def _title(self):
        """Make the title"""
        if self.title:
            self.svg.node(self.nodes['graph'], 'text', class_='title',
                      x=self.margin.left + self.view.width / 2,
                      y=self.title_font_size + 10
            ).text = self.title

    def _serie(self, serie):
        """Make serie node"""
        return dict(
            plot=self.svg.node(
                self.nodes['plot'],
                class_='series serie-%d color-%d' % (serie, serie)),
            overlay=self.svg.node(
                self.nodes['overlay'],
                class_='series serie-%d color-%d' % (serie, serie)),
            text_overlay=self.svg.node(
                self.nodes['text_overlay'],
                class_='series serie-%d color-%d' % (serie, serie)))

    def _interpolate(self, ys, xs,
                   polar=False, xy=False, xy_xmin=None, xy_rng=None):
        """Make the interpolation"""
        interpolate = interpolation(
            xs, ys, kind=self.interpolate)
        p = self.interpolation_precision
        xmin = min(xs)
        xmax = max(xs)
        interpolateds = []
        for i in range(int(p + 1)):
            x = i / p
            if polar:
                x = .5 * pi + 2 * pi * x
            elif xy:
                x = xy_xmin + xy_rng * x
            interpolated = float(interpolate(x))
            if not isnan(interpolated) and xmin <= x <= xmax:
                coord = (x, interpolated)
                if polar:
                    coord = tuple(reversed(coord))
                interpolateds.append(coord)
        return interpolateds

    def _tooltip_data(self, node, value, x, y, classes=None):
        self.svg.node(node, 'desc', class_="value").text = value
        if classes is None:
            classes = []
            if x > self.view.width / 2:
                classes.append('left')
            if y > self.view.height / 2:
                classes.append('top')
            classes = ' '.join(classes)

        self.svg.node(node, 'desc',
                      class_="x " + classes).text = str(x)
        self.svg.node(node, 'desc',
                      class_="y " + classes).text = str(y)

    def _static_value(self, serie_node, value, x, y):
        if self.print_values:
            self.svg.node(
                serie_node['text_overlay'], 'text',
                class_='centered',
                x=x,
                y=y + self.value_font_size / 3
            ).text = value if self.print_zeroes or value != '0' else ''
