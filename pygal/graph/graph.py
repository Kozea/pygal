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
Commmon graphing functions

"""

from __future__ import division
from pygal.interpolate import INTERPOLATIONS
from pygal.graph.base import BaseGraph
from pygal.view import View, LogView, XYLogView
from pygal.util import (
    truncate, reverse_text_len, get_texts_box, cut, rad, decorate)
from math import sqrt, ceil, cos
from itertools import repeat, chain


class Graph(BaseGraph):
    """Graph super class containing generic common functions"""
    _dual = False

    def _decorate(self):
        """Draw all decorations"""
        self._set_view()
        self._make_graph()
        self._axes()
        self._legend()
        self._title()
        self._x_title()
        self._y_title()

    def _axes(self):
        """Draw axes"""
        self._y_axis()
        self._x_axis()

    def _set_view(self):
        """Assign a view to current graph"""
        if self.logarithmic:
            if self._dual:
                view_class = XYLogView
            else:
                view_class = LogView
        else:
            view_class = View

        self.view = view_class(
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
        self.nodes['title'] = self.svg.node(
            self.nodes['graph'],
            class_="titles")
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
            transform='translate(0 0)',
            style="opacity: 0",
            **{'class': 'tooltip'})

        a = self.svg.node(self.nodes['tooltip'], 'a')
        self.svg.node(a, 'rect',
                      rx=self.tooltip_border_radius,
                      ry=self.tooltip_border_radius,
                      width=0, height=0,
                      **{'class': 'tooltip-box'})
        text = self.svg.node(a, 'text', class_='text')
        self.svg.node(text, 'tspan', class_='label')
        self.svg.node(text, 'tspan', class_='value')

    def _x_axis(self):
        """Make the x axis: labels and guides"""
        if not self._x_labels or not self.show_x_labels:
            return
        axis = self.svg.node(self.nodes['plot'], class_="axis x%s" % (
            ' always_show' if self.show_x_guides else ''
        ))
        truncation = self.truncate_label
        if not truncation:
            if self.x_label_rotation or len(self._x_labels) <= 1:
                truncation = 25
            else:
                first_label_position = self.view.x(self._x_labels[0][1]) or 0
                last_label_position = self.view.x(self._x_labels[-1][1]) or 0
                available_space = (
                    last_label_position - first_label_position) / (
                    len(self._x_labels) - 1)
                truncation = reverse_text_len(
                    available_space, self.label_font_size)
                truncation = max(truncation, 1)

        if 0 not in [label[1] for label in self._x_labels]:
            self.svg.node(axis, 'path',
                          d='M%f %f v%f' % (0, 0, self.view.height),
                          class_='line')
        lastlabel = self._x_labels[-1][0]

        for label, position in self._x_labels:
            major = label in self._x_major_labels
            if not (self.show_minor_x_labels or major):
                continue
            guides = self.svg.node(axis, class_='guides')
            x = self.view.x(position)
            y = self.view.height + 5
            last_guide = (self._y_2nd_labels and label == lastlabel)
            self.svg.node(
                guides, 'path',
                d='M%f %f v%f' % (x or 0, 0, self.view.height),
                class_='%s%s%sline' % (
                    'axis ' if label == "0" else '',
                    'major ' if major else '',
                    'guide ' if position != 0 and not last_guide else ''))
            y += .5 * self.label_font_size + 5
            text = self.svg.node(
                guides, 'text',
                x=x,
                y=y,
                class_='major' if major else ''
            )

            if isinstance(label, dict):
                label = label['title']

            text.text = truncate(label, truncation)
            if text.text != label:
                self.svg.node(guides, 'title').text = label
            if self.x_label_rotation:
                text.attrib['transform'] = "rotate(%d %f %f)" % (
                    self.x_label_rotation, x, y)

        if self._x_2nd_labels:
            secondary_ax = self.svg.node(
                self.nodes['plot'], class_="axis x x2%s" % (
                    ' always_show' if self.show_x_guides else ''
                ))
            for label, position in self._x_2nd_labels:
                major = label in self._x_major_labels
                if not (self.show_minor_x_labels or major):
                    continue
                # it is needed, to have the same structure as primary axis
                guides = self.svg.node(secondary_ax, class_='guides')
                x = self.view.x(position)
                y = -5
                text = self.svg.node(
                    guides, 'text',
                    x=x,
                    y=y,
                    class_='major' if major else ''
                )
                text.text = label
                if self.x_label_rotation:
                    text.attrib['transform'] = "rotate(%d %f %f)" % (
                        -self.x_label_rotation, x, y)

    def _y_axis(self):
        """Make the y axis: labels and guides"""
        if not self._y_labels or not self.show_y_labels:
            return

        axis = self.svg.node(self.nodes['plot'], class_="axis y")

        if (0 not in [label[1] for label in self._y_labels] and
                self.show_y_guides):
            self.svg.node(
                axis, 'path',
                d='M%f %f h%f' % (0, self.view.height, self.view.width),
                class_='line'
            )

        for label, position in self._y_labels:
            major = position in self._y_major_labels
            if not (self.show_minor_y_labels or major):
                continue
            guides = self.svg.node(axis, class_='%sguides' % (
                'logarithmic ' if self.logarithmic else ''
            ))
            x = -5
            y = self.view.y(position)
            if not y:
                continue
            if self.show_y_guides:
                self.svg.node(
                    guides, 'path',
                    d='M%f %f h%f' % (0, y, self.view.width),
                    class_='%s%s%sline' % (
                        'axis ' if label == "0" else '',
                        'major ' if major else '',
                        'guide ' if position != 0 else ''))
            text = self.svg.node(
                guides, 'text',
                x=x,
                y=y + .35 * self.label_font_size,
                class_='major' if major else ''
            )

            if isinstance(label, dict):
                label = label['title']
            text.text = label

            if self.y_label_rotation:
                text.attrib['transform'] = "rotate(%d %f %f)" % (
                    self.y_label_rotation, x, y)

        if self._y_2nd_labels:
            secondary_ax = self.svg.node(
                self.nodes['plot'], class_="axis y2")
            for label, position in self._y_2nd_labels:
                major = position in self._y_major_labels
                if not (self.show_minor_y_labels or major):
                    continue
                # it is needed, to have the same structure as primary axis
                guides = self.svg.node(secondary_ax, class_='guides')
                x = self.view.width + 5
                y = self.view.y(position)
                text = self.svg.node(
                    guides, 'text',
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
        truncation = self.truncate_legend
        if self.legend_at_bottom:
            x = self.margin.left + self.spacing
            y = (self.margin.top + self.view.height +
                 self._x_title_height +
                 self._x_labels_height + self.spacing)
            cols = self.legend_at_bottom_columns or ceil(
                sqrt(self._order)) or 1

            if not truncation:
                available_space = self.view.width / cols - (
                    self.legend_box_size + 5)
                truncation = reverse_text_len(
                    available_space, self.legend_font_size)
        else:
            x = self.spacing
            y = self.margin.top + self.spacing
            cols = 1
            if not truncation:
                truncation = 15

        legends = self.svg.node(
            self.nodes['graph'], class_='legends',
            transform='translate(%d, %d)' % (x, y))

        h = max(self.legend_box_size, self.legend_font_size)
        x_step = self.view.width / cols
        if self.legend_at_bottom:
            # if legends at the bottom, we dont split the windows
            # gen structure - (i, (j, (l, tf)))
            # i - global serie number - used for coloring and identification
            # j - position within current legend box
            # l - label
            # tf - whether it is secondary label
            gen = enumerate(enumerate(chain(
                zip(self._legends, repeat(False)),
                zip(self._secondary_legends, repeat(True)))))
            secondary_legends = legends  # svg node is the same
        else:
            gen = enumerate(chain(
                enumerate(zip(self._legends, repeat(False))),
                enumerate(zip(self._secondary_legends, repeat(True)))))

            # draw secondary axis on right
            x = self.margin.left + self.view.width + self.spacing
            if self._y_2nd_labels:
                h, w = get_texts_box(
                    cut(self._y_2nd_labels), self.label_font_size)
                x += self.spacing + max(w * cos(rad(self.y_label_rotation)), h)

            y = self.margin.top + self.spacing

            secondary_legends = self.svg.node(
                self.nodes['graph'], class_='legends',
                transform='translate(%d, %d)' % (x, y))

        for (global_serie_number, (i, (title, is_secondary))) in gen:

            col = i % cols
            row = i // cols

            legend = self.svg.node(
                secondary_legends if is_secondary else legends,
                class_='legend reactive activate-serie',
                id="activate-serie-%d" % global_serie_number)
            self.svg.node(
                legend, 'rect',
                x=col * x_step,
                y=1.5 * row * h + (
                    self.legend_font_size - self.legend_box_size
                    if self.legend_font_size > self.legend_box_size else 0
                ) / 2,
                width=self.legend_box_size,
                height=self.legend_box_size,
                class_="color-%d reactive" % (
                    global_serie_number % len(self.style['colors']))
            )

            if isinstance(title, dict):
                node = decorate(self.svg, legend, title)
                title = title['title']
            else:
                node = legend

            truncated = truncate(title, truncation)
            self.svg.node(
                node, 'text',
                x=col * x_step + self.legend_box_size + 5,
                y=1.5 * row * h + .5 * h + .3 * self.legend_font_size
            ).text = truncated

            if truncated != title:
                self.svg.node(legend, 'title').text = title

    def _title(self):
        """Make the title"""
        if self.title:
            for i, title_line in enumerate(self.title, 1):
                self.svg.node(
                    self.nodes['title'], 'text', class_='title plot_title',
                    x=self.width / 2,
                    y=i * (self.title_font_size + self.spacing)
                ).text = title_line

    def _x_title(self):
        """Make the X-Axis title"""
        y = (self.height - self.margin.bottom +
             self._x_labels_height)
        if self.x_title:
            for i, title_line in enumerate(self.x_title, 1):
                text = self.svg.node(
                    self.nodes['title'], 'text', class_='title',
                    x=self.margin.left + self.view.width / 2,
                    y=y + i * (self.title_font_size + self.spacing)
                )
                text.text = title_line

    def _y_title(self):
        """Make the Y-Axis title"""
        if self.y_title:
            yc = self.margin.top + self.view.height / 2
            for i, title_line in enumerate(self.y_title, 1):
                text = self.svg.node(
                    self.nodes['title'], 'text', class_='title',
                    x=self._legend_at_left_width,
                    y=i * (self.title_font_size + self.spacing) + yc
                )
                text.attrib['transform'] = "rotate(%d %f %f)" % (
                    -90, self._legend_at_left_width, yc)
                text.text = title_line

    def _interpolate(self, xs, ys):
        """Make the interpolation"""
        x = []
        y = []
        for i in range(len(ys)):
            if ys[i] is not None:
                x.append(xs[i])
                y.append(ys[i])

        interpolate = INTERPOLATIONS[self.interpolate]

        return list(interpolate(
            x, y, self.interpolation_precision,
            **self.interpolation_parameters))

    def _rescale(self, points):
        return [
            (x, self._scale_diff + (y - self._scale_min_2nd) * self._scale
             if y is not None else None)
            for x, y in points]

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

    def _get_value(self, values, i):
        """Get the value formatted for tooltip"""
        return self._format(values[i][1])

    def _points(self, x_pos):
        for serie in self.all_series:
            serie.points = [
                (x_pos[i], v)
                for i, v in enumerate(serie.values)]
            if serie.points and self.interpolate:
                serie.interpolated = self._interpolate(x_pos, serie.values)
            else:
                serie.interpolated = []

    def _compute_secondary(self):
        # secondary y axis support
        if self.secondary_series and self._y_labels:
            y_pos = list(zip(*self._y_labels))[1]
            if self.include_x_axis:
                ymin = min(self._secondary_min, 0)
                ymax = max(self._secondary_max, 0)
            else:
                ymin = self._secondary_min
                ymax = self._secondary_max
            steps = len(y_pos)
            left_range = abs(y_pos[-1] - y_pos[0])
            right_range = abs(ymax - ymin) or 1
            scale = right_range / ((steps - 1) or 1)
            self._y_2nd_labels = [(self._format(ymin + i * scale), pos)
                                  for i, pos in enumerate(y_pos)]

            self._scale = left_range / right_range
            self._scale_diff = y_pos[0]
            self._scale_min_2nd = ymin

    def _post_compute(self):
        pass
