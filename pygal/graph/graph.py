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
from pygal.graph.base import BaseGraph
from pygal.view import View, LogView
from pygal.util import is_major


class Graph(BaseGraph):
    """Graph super class containing generic common functions"""

    def _decorate(self):
        self._set_view()
        self._make_graph()
        self._x_axis()
        self._y_axis()
        self._legend()
        self._title()

    def _set_view(self):
        self.view = (LogView if self.logarithmic else View)(
            self.width - self.margin.x,
            self.height - self.margin.y,
            self._box)

    def _make_graph(self):
        self.graph_node = self.svg.node(
            class_='graph %s-graph' % self.__class__.__name__.lower())
        self.svg.node(self.graph_node, 'rect',
                  class_='background',
                  x=0, y=0,
                  width=self.width,
                  height=self.height)
        self.plot = self.svg.node(
            self.graph_node, class_="plot",
            transform="translate(%d, %d)" % (
                self.margin.left, self.margin.top))
        self.svg.node(self.plot, 'rect',
                  class_='background',
                  x=0, y=0,
                  width=self.view.width,
                  height=self.view.height)
        self.overlay = self.svg.node(
            self.graph_node, class_="plot overlay",
            transform="translate(%d, %d)" % (
                self.margin.left, self.margin.top))
        self.text_overlay = self.svg.node(
            self.graph_node, class_="plot text-overlay",
            transform="translate(%d, %d)" % (
                self.margin.left, self.margin.top))
        tooltip_overlay = self.svg.node(
            self.graph_node, class_="plot tooltip-overlay",
            transform="translate(%d, %d)" % (
                self.margin.left, self.margin.top))
        self.tooltip_node = self.svg.node(tooltip_overlay, id="tooltip",
                                          transform='translate(0 0)')

        self.svg.node(self.tooltip_node, 'rect',
                      id="tooltip-box",
                      rx=5, ry=5,
        )
        self.svg.node(self.tooltip_node, 'text')

    def _x_axis(self):
        if not self._x_labels:
            return

        axis = self.svg.node(self.plot, class_="axis x")

        if 0 not in [label[1] for label in self._x_labels]:
            self.svg.node(axis, 'path',
                      d='M%f %f v%f' % (0, 0, self.view.height),
                      class_='line')
        for label, position in self._x_labels:
            guides = self.svg.node(axis, class_='guides')
            x = self.view.x(position)
            y = self.view.height + 5
            self.svg.node(guides, 'path',
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

    def _y_axis(self):
        if not self._y_labels:
            return

        axis = self.svg.node(self.plot, class_="axis y")

        if 0 not in [label[1] for label in self._y_labels]:
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
            self.svg.node(guides, 'path',
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
        if not self.show_legend:
            return
        legends = self.svg.node(
            self.graph_node, class_='legends',
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
        if self.title:
            self.svg.node(self.graph_node, 'text', class_='title',
                      x=self.margin.left + self.view.width / 2,
                      y=self.title_font_size + 10
            ).text = self.title

    def _serie(self, serie):
        return dict(
            plot=self.svg.node(
                self.plot,
                class_='series serie-%d color-%d' % (serie, serie)),
            overlay=self.svg.node(
                self.overlay,
                class_='series serie-%d color-%d' % (serie, serie)),
            text_overlay=self.svg.node(
                self.text_overlay,
                class_='series serie-%d color-%d' % (serie, serie)))
