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
"""Chart properties and drawing"""

from __future__ import division

from math import ceil, cos, sin, sqrt

from pygal import stats
from pygal._compat import is_list_like, is_str, to_str
from pygal.graph.public import PublicApi
from pygal.interpolate import INTERPOLATIONS
from pygal.util import (
    cached_property, compute_scale, cut, decorate, filter_kwargs, get_text_box,
    get_texts_box, majorize, rad, reverse_text_len, split_title, truncate)
from pygal.view import LogView, ReverseView, View, XYLogView


class Graph(PublicApi):

    """Graph super class containing generic common functions"""

    _dual = False

    def _decorate(self):
        """Draw all decorations"""
        self._set_view()
        self._make_graph()
        self._axes()
        self._legend()
        self._make_title()
        self._make_x_title()
        self._make_y_title()

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
            view_class = ReverseView if self.inverse_y_axis else View

        self.view = view_class(
            self.width - self.margin_box.x,
            self.height - self.margin_box.y,
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
                self.margin_box.left, self.margin_box.top))
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
                self.margin_box.left, self.margin_box.top))
        self.nodes['text_overlay'] = self.svg.node(
            self.nodes['graph'], class_="plot text-overlay",
            transform="translate(%d, %d)" % (
                self.margin_box.left, self.margin_box.top))
        self.nodes['tooltip_overlay'] = self.svg.node(
            self.nodes['graph'], class_="plot tooltip-overlay",
            transform="translate(%d, %d)" % (
                self.margin_box.left, self.margin_box.top))
        self.nodes['tooltip'] = self.svg.node(
            self.nodes['tooltip_overlay'],
            transform='translate(0 0)',
            style="opacity: 0",
            **{'class': 'tooltip'})

        self.svg.node(self.nodes['tooltip'], 'rect',
                      rx=self.tooltip_border_radius,
                      ry=self.tooltip_border_radius,
                      width=0, height=0,
                      **{'class': 'tooltip-box'})
        self.svg.node(self.nodes['tooltip'], 'g', class_='text')

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
                    available_space, self.style.label_font_size)
                truncation = max(truncation, 1)

        lastlabel = self._x_labels[-1][0]
        if 0 not in [label[1] for label in self._x_labels]:
            self.svg.node(axis, 'path',
                          d='M%f %f v%f' % (0, 0, self.view.height),
                          class_='line')
            lastlabel = None

        for label, position in self._x_labels:
            if self.horizontal:
                major = position in self._x_labels_major
            else:
                major = label in self._x_labels_major
            if not (self.show_minor_x_labels or major):
                continue
            guides = self.svg.node(axis, class_='guides')
            x = self.view.x(position)
            if x is None:
                continue
            y = self.view.height + 5
            last_guide = (self._y_2nd_labels and label == lastlabel)
            self.svg.node(
                guides, 'path',
                d='M%f %f v%f' % (x or 0, 0, self.view.height),
                class_='%s%s%sline' % (
                    'axis ' if label == "0" else '',
                    'major ' if major else '',
                    'guide ' if position != 0 and not last_guide else ''))
            y += .5 * self.style.label_font_size + 5
            text = self.svg.node(
                guides, 'text',
                x=x,
                y=y,
                class_='major' if major else ''
            )

            text.text = truncate(label, truncation)
            if text.text != label:
                self.svg.node(guides, 'title').text = label
            elif self._dual:
                self.svg.node(
                    guides, 'title',
                ).text = self._x_format(position)

            if self.x_label_rotation:
                text.attrib['transform'] = "rotate(%d %f %f)" % (
                    self.x_label_rotation, x, y)
                if self.x_label_rotation >= 180:
                    text.attrib['class'] = ' '.join(
                        (text.attrib['class'] and text.attrib['class'].split(
                            ' ') or []) + ['backwards'])

        if self._y_2nd_labels and 0 not in [
                label[1] for label in self._x_labels]:
            self.svg.node(axis, 'path',
                          d='M%f %f v%f' % (
                              self.view.width, 0, self.view.height),
                          class_='line')

        if self._x_2nd_labels:
            secondary_ax = self.svg.node(
                self.nodes['plot'], class_="axis x x2%s" % (
                    ' always_show' if self.show_x_guides else ''
                ))
            for label, position in self._x_2nd_labels:
                major = label in self._x_labels_major
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
                    if self.x_label_rotation >= 180:
                        text.attrib['class'] = ' '.join((
                            text.attrib['class'] and
                            text.attrib['class'].split(
                                ' ') or []) + ['backwards'])

    def _y_axis(self):
        """Make the y axis: labels and guides"""
        if not self._y_labels or not self.show_y_labels:
            return

        axis = self.svg.node(self.nodes['plot'], class_="axis y%s" % (
            ' always_show' if self.show_y_guides else ''
        ))

        if (0 not in [label[1] for label in self._y_labels] and
                self.show_y_guides):
            self.svg.node(
                axis, 'path',
                d='M%f %f h%f' % (
                    0, 0 if self.inverse_y_axis else self.view.height,
                    self.view.width),
                class_='line'
            )

        for label, position in self._y_labels:
            if self.horizontal:
                major = label in self._y_labels_major
            else:
                major = position in self._y_labels_major

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
                y=y + .35 * self.style.label_font_size,
                class_='major' if major else ''
            )

            text.text = label

            if self.y_label_rotation:
                text.attrib['transform'] = "rotate(%d %f %f)" % (
                    self.y_label_rotation, x, y)
                if 90 < self.y_label_rotation < 270:
                    text.attrib['class'] = ' '.join(
                        (text.attrib['class'] and text.attrib['class'].split(
                            ' ') or []) + ['backwards'])
            self.svg.node(
                guides, 'title',
            ).text = self._y_format(position)

        if self._y_2nd_labels:
            secondary_ax = self.svg.node(
                self.nodes['plot'], class_="axis y2")
            for label, position in self._y_2nd_labels:
                major = position in self._y_labels_major
                if not (self.show_minor_y_labels or major):
                    continue
                # it is needed, to have the same structure as primary axis
                guides = self.svg.node(secondary_ax, class_='guides')
                x = self.view.width + 5
                y = self.view.y(position)
                text = self.svg.node(
                    guides, 'text',
                    x=x,
                    y=y + .35 * self.style.label_font_size,
                    class_='major' if major else ''
                )
                text.text = label
                if self.y_label_rotation:
                    text.attrib['transform'] = "rotate(%d %f %f)" % (
                        self.y_label_rotation, x, y)
                    if 90 < self.y_label_rotation < 270:
                        text.attrib['class'] = ' '.join(
                            (text.attrib['class'] and
                             text.attrib['class'].split(
                                ' ') or []) + ['backwards'])

    def _legend(self):
        """Make the legend box"""
        if not self.show_legend:
            return
        truncation = self.truncate_legend
        if self.legend_at_bottom:
            x = self.margin_box.left + self.spacing
            y = (self.margin_box.top + self.view.height +
                 self._x_title_height +
                 self._x_labels_height + self.spacing)
            cols = self.legend_at_bottom_columns or ceil(
                sqrt(self._order)) or 1

            if not truncation:
                available_space = self.view.width / cols - (
                    self.legend_box_size + 5)
                truncation = reverse_text_len(
                    available_space, self.style.legend_font_size)
        else:
            x = self.spacing
            y = self.margin_box.top + self.spacing
            cols = 1
            if not truncation:
                truncation = 15

        legends = self.svg.node(
            self.nodes['graph'], class_='legends',
            transform='translate(%d, %d)' % (x, y))

        h = max(self.legend_box_size, self.style.legend_font_size)
        x_step = self.view.width / cols
        if self.legend_at_bottom:
            secondary_legends = legends  # svg node is the same
        else:

            # draw secondary axis on right
            x = self.margin_box.left + self.view.width + self.spacing
            if self._y_2nd_labels:
                h, w = get_texts_box(
                    cut(self._y_2nd_labels), self.style.label_font_size)
                x += self.spacing + max(w * abs(cos(rad(
                    self.y_label_rotation))), h)

            y = self.margin_box.top + self.spacing

            secondary_legends = self.svg.node(
                self.nodes['graph'], class_='legends',
                transform='translate(%d, %d)' % (x, y))

        serie_number = -1
        i = 0

        for titles, is_secondary in (
                (self._legends, False),
                (self._secondary_legends, True)):
            if not self.legend_at_bottom and is_secondary:
                i = 0

            for title in titles:
                serie_number += 1
                if title is None:
                    continue
                col = i % cols
                row = i // cols

                legend = self.svg.node(
                    secondary_legends if is_secondary else legends,
                    class_='legend reactive activate-serie',
                    id="activate-serie-%d" % serie_number)
                self.svg.node(
                    legend, 'rect',
                    x=col * x_step,
                    y=1.5 * row * h + (
                        self.style.legend_font_size - self.legend_box_size
                        if self.style.legend_font_size > self.legend_box_size
                        else 0
                    ) / 2,
                    width=self.legend_box_size,
                    height=self.legend_box_size,
                    class_="color-%d reactive" % serie_number
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
                    y=1.5 * row * h + .5 * h + .3 * self.style.legend_font_size
                ).text = truncated

                if truncated != title:
                    self.svg.node(legend, 'title').text = title

                i += 1

    def _make_title(self):
        """Make the title"""
        if self._title:
            for i, title_line in enumerate(self._title, 1):
                self.svg.node(
                    self.nodes['title'], 'text', class_='title plot_title',
                    x=self.width / 2,
                    y=i * (self.style.title_font_size + self.spacing)
                ).text = title_line

    def _make_x_title(self):
        """Make the X-Axis title"""
        y = (self.height - self.margin_box.bottom +
             self._x_labels_height)
        if self._x_title:
            for i, title_line in enumerate(self._x_title, 1):
                text = self.svg.node(
                    self.nodes['title'], 'text', class_='title',
                    x=self.margin_box.left + self.view.width / 2,
                    y=y + i * (self.style.title_font_size + self.spacing)
                )
                text.text = title_line

    def _make_y_title(self):
        """Make the Y-Axis title"""
        if self._y_title:
            yc = self.margin_box.top + self.view.height / 2
            for i, title_line in enumerate(self._y_title, 1):
                text = self.svg.node(
                    self.nodes['title'], 'text', class_='title',
                    x=self._legend_at_left_width,
                    y=i * (self.style.title_font_size + self.spacing) + yc
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
        """Scale for secondary"""
        return [
            (x, self._scale_diff + (y - self._scale_min_2nd) * self._scale
             if y is not None else None)
            for x, y in points]

    def _tooltip_data(self, node, value, x, y, classes=None, xlabel=None):
        """Insert in desc tags informations for the javascript tooltip"""
        self.svg.node(node, 'desc', class_="value").text = value
        if classes is None:
            classes = []
            if x > self.view.width / 2:
                classes.append('left')
            if y > self.view.height / 2:
                classes.append('top')
            classes = ' '.join(classes)

        self.svg.node(node, 'desc',
                      class_="x " + classes).text = to_str(x)
        self.svg.node(node, 'desc',
                      class_="y " + classes).text = to_str(y)
        if xlabel:
            self.svg.node(node, 'desc',
                          class_="x_label").text = to_str(xlabel)

    def _static_value(self, serie_node, value, x, y, metadata,
                      align_text='left', classes=None):
        """Write the print value"""
        label = metadata and metadata.get('label')
        classes = classes and [classes] or []

        if self.print_labels and label:
            label_cls = classes + ['label']
            if self.print_values:
                y -= self.style.value_font_size / 2
            self.svg.node(
                serie_node['text_overlay'], 'text',
                class_=' '.join(label_cls),
                x=x,
                y=y + self.style.value_font_size / 3
            ).text = label
            y += self.style.value_font_size

        if self.print_values or self.dynamic_print_values:
            val_cls = classes + ['value']
            if self.dynamic_print_values:
                val_cls.append('showable')

            self.svg.node(
                serie_node['text_overlay'], 'text',
                class_=' '.join(val_cls),
                x=x,
                y=y + self.style.value_font_size / 3,
                attrib={'text-anchor': align_text}
            ).text = value if self.print_zeroes or value != '0' else ''

    def _points(self, x_pos):
        """
        Convert given data values into drawable points (x, y)
        and interpolated points if interpolate option is specified
        """
        for serie in self.all_series:
            serie.points = [
                (x_pos[i], v)
                for i, v in enumerate(serie.values)]
            if serie.points and self.interpolate:
                serie.interpolated = self._interpolate(x_pos, serie.values)
            else:
                serie.interpolated = []

    def _compute_secondary(self):
        """Compute secondary axis min max and label positions"""
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
            self._y_2nd_labels = [(self._y_format(ymin + i * scale), pos)
                                  for i, pos in enumerate(y_pos)]

            self._scale = left_range / right_range
            self._scale_diff = y_pos[0]
            self._scale_min_2nd = ymin

    def _post_compute(self):
        """Hook called after compute and before margin computations and plot"""
        pass

    def _get_x_label(self, i):
        """Convenience function to get the x_label of a value index"""
        if not self.x_labels or not self._x_labels or len(self._x_labels) <= i:
            return
        return self._x_labels[i][0]

    @property
    def all_series(self):
        """Getter for all series (nomal and secondary)"""
        return self.series + self.secondary_series

    @property
    def _x_format(self):
        """Return the abscissa value formatter (always unary)"""
        return self.x_value_formatter

    @property
    def _default_formatter(self):
        return to_str

    @property
    def _y_format(self):
        """Return the ordinate value formatter (always unary)"""
        return self.value_formatter

    def _value_format(self, value):
        """
        Format value for value display.
        (Varies in type between chart types)
        """

        return self._y_format(value)

    def _format(self, serie, i):
        """Format the nth value for the serie"""
        value = serie.values[i]
        metadata = serie.metadata.get(i)

        kwargs = {
            'chart': self,
            'serie': serie,
            'index': i
        }
        formatter = (
            (metadata and metadata.get('formatter')) or
            serie.formatter or
            self.formatter or
            self._value_format
        )
        kwargs = filter_kwargs(formatter, kwargs)
        return formatter(value, **kwargs)

    def _serie_format(self, serie, value):
        """Format an independent value for the serie"""

        kwargs = {
            'chart': self,
            'serie': serie,
            'index': None
        }
        formatter = (
            serie.formatter or
            self.formatter or
            self._value_format
        )
        kwargs = filter_kwargs(formatter, kwargs)
        return formatter(value, **kwargs)

    def _compute(self):
        """Initial computations to draw the graph"""

    def _compute_margin(self):
        """Compute graph margins from set texts"""
        self._legend_at_left_width = 0
        for series_group in (self.series, self.secondary_series):
            if self.show_legend and series_group:
                h, w = get_texts_box(
                    map(lambda x: truncate(x, self.truncate_legend or 15),
                        [serie.title['title']
                         if isinstance(serie.title, dict)
                         else serie.title or '' for serie in series_group]),
                    self.style.legend_font_size)
                if self.legend_at_bottom:
                    h_max = max(h, self.legend_box_size)
                    cols = (self._order // self.legend_at_bottom_columns
                            if self.legend_at_bottom_columns
                            else ceil(sqrt(self._order)) or 1)
                    self.margin_box.bottom += self.spacing + h_max * round(
                        cols - 1) * 1.5 + h_max
                else:
                    if series_group is self.series:
                        legend_width = self.spacing + w + self.legend_box_size
                        self.margin_box.left += legend_width
                        self._legend_at_left_width += legend_width
                    else:
                        self.margin_box.right += (
                            self.spacing + w + self.legend_box_size)

        self._x_labels_height = 0
        if (self._x_labels or self._x_2nd_labels) and self.show_x_labels:
            for xlabels in (self._x_labels, self._x_2nd_labels):
                if xlabels:
                    h, w = get_texts_box(
                        map(lambda x: truncate(x, self.truncate_label or 25),
                            cut(xlabels)),
                        self.style.label_font_size)
                    self._x_labels_height = self.spacing + max(
                        w * abs(sin(rad(self.x_label_rotation))), h)
                    if xlabels is self._x_labels:
                        self.margin_box.bottom += self._x_labels_height
                    else:
                        self.margin_box.top += self._x_labels_height
                    if self.x_label_rotation:
                        if self.x_label_rotation % 180 < 90:
                            self.margin_box.right = max(
                                w * abs(cos(rad(self.x_label_rotation))),
                                self.margin_box.right)
                        else:
                            self.margin_box.left = max(
                                w * abs(cos(rad(self.x_label_rotation))),
                                self.margin_box.left)

        if self.show_y_labels:
            for ylabels in (self._y_labels, self._y_2nd_labels):
                if ylabels:
                    h, w = get_texts_box(
                        cut(ylabels), self.style.label_font_size)
                    if ylabels is self._y_labels:
                        self.margin_box.left += self.spacing + max(
                            w * abs(cos(rad(self.y_label_rotation))), h)
                    else:
                        self.margin_box.right += self.spacing + max(
                            w * abs(cos(rad(self.y_label_rotation))), h)

        self._title = split_title(
            self.title, self.width, self.style.title_font_size)

        if self.title:
            h, _ = get_text_box(self._title[0], self.style.title_font_size)
            self.margin_box.top += len(self._title) * (self.spacing + h)

        self._x_title = split_title(
            self.x_title, self.width - self.margin_box.x,
            self.style.title_font_size)

        self._x_title_height = 0
        if self._x_title:
            h, _ = get_text_box(self._x_title[0], self.style.title_font_size)
            height = len(self._x_title) * (self.spacing + h)
            self.margin_box.bottom += height
            self._x_title_height = height + self.spacing

        self._y_title = split_title(
            self.y_title, self.height - self.margin_box.y,
            self.style.title_font_size)

        self._y_title_height = 0
        if self._y_title:
            h, _ = get_text_box(self._y_title[0], self.style.title_font_size)
            height = len(self._y_title) * (self.spacing + h)
            self.margin_box.left += height
            self._y_title_height = height + self.spacing

        # Inner margin
        if self.print_values_position == 'top':
            gh = self.height - self.margin_box.y
            alpha = 1.1 * (self.style.value_font_size / gh) * self._box.height
            if self._max and self._max > 0:
                self._box.ymax += alpha
            if self._min and self._min < 0:
                self._box.ymin -= alpha

    def _confidence_interval(self, node, x, y, value, metadata):
        if not metadata or 'ci' not in metadata:
            return
        ci = metadata['ci']
        ci['point_estimate'] = value

        low, high = getattr(
            stats,
            'confidence_interval_%s' % ci.get('type', 'manual')
        )(**ci)

        self.svg.confidence_interval(
            node, x,
            # Respect some charts y modifications (pyramid, stackbar)
            y + (self.view.y(low) - self.view.y(value)),
            y + (self.view.y(high) - self.view.y(value)))

    @cached_property
    def _legends(self):
        """Getter for series title"""
        return [serie.title for serie in self.series]

    @cached_property
    def _secondary_legends(self):
        """Getter for series title on secondary y axis"""
        return [serie.title for serie in self.secondary_series]

    @cached_property
    def _values(self):
        """Getter for series values (flattened)"""
        return [val
                for serie in self.series
                for val in serie.values
                if val is not None]

    @cached_property
    def _secondary_values(self):
        """Getter for secondary series values (flattened)"""
        return [val
                for serie in self.secondary_series
                for val in serie.values
                if val is not None]

    @cached_property
    def _len(self):
        """Getter for the maximum series size"""
        return max([
            len(serie.values)
            for serie in self.all_series] or [0])

    @cached_property
    def _secondary_min(self):
        """Getter for the minimum series value"""
        return (self.secondary_range[0] if (
            self.secondary_range and self.secondary_range[0] is not None)
            else (min(self._secondary_values)
                  if self._secondary_values else None))

    @cached_property
    def _min(self):
        """Getter for the minimum series value"""
        return (self.range[0] if (self.range and self.range[0] is not None)
                else (min(self._values)
                      if self._values else None))

    @cached_property
    def _max(self):
        """Getter for the maximum series value"""
        return (self.range[1] if (self.range and self.range[1] is not None)
                else (max(self._values) if self._values else None))

    @cached_property
    def _secondary_max(self):
        """Getter for the maximum series value"""
        return (self.secondary_range[1] if (
            self.secondary_range and self.secondary_range[1] is not None)
            else (max(self._secondary_values)
                  if self._secondary_values else None))

    @cached_property
    def _order(self):
        """Getter for the number of series"""
        return len(self.all_series)

    def _x_label_format_if_value(self, label):
        if not is_str(label):
            return self._x_format(label)
        return label

    def _compute_x_labels(self):
        self._x_labels = self.x_labels and list(
            zip(map(self._x_label_format_if_value, self.x_labels),
                self._x_pos))

    def _compute_x_labels_major(self):
        if self.x_labels_major_every:
            self._x_labels_major = [self._x_labels[i][0] for i in range(
                0, len(self._x_labels), self.x_labels_major_every)]

        elif self.x_labels_major_count:
            label_count = len(self._x_labels)
            major_count = self.x_labels_major_count
            if (major_count >= label_count):
                self._x_labels_major = [label[0] for label in self._x_labels]

            else:
                self._x_labels_major = [self._x_labels[
                    int(i * (label_count - 1) / (major_count - 1))][0]
                    for i in range(major_count)]
        else:
            self._x_labels_major = self.x_labels_major and list(
                map(self._x_label_format_if_value, self.x_labels_major)) or []

    def _compute_y_labels(self):
        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic,
            self.order_min, self.min_scale, self.max_scale
        )
        if self.y_labels:
            self._y_labels = []
            for i, y_label in enumerate(self.y_labels):
                if isinstance(y_label, dict):
                    pos = self._adapt(y_label.get('value'))
                    title = y_label.get('label', self._y_format(pos))
                elif is_str(y_label):
                    pos = self._adapt(y_pos[i % len(y_pos)])
                    title = y_label
                else:
                    pos = self._adapt(y_label)
                    title = self._y_format(pos)
                self._y_labels.append((title, pos))
            self._box.ymin = min(self._box.ymin, min(cut(self._y_labels, 1)))
            self._box.ymax = max(self._box.ymax, max(cut(self._y_labels, 1)))
        else:
            self._y_labels = list(zip(map(self._y_format, y_pos), y_pos))

    def _compute_y_labels_major(self):
        if self.y_labels_major_every:
            self._y_labels_major = [self._y_labels[i][1] for i in range(
                0, len(self._y_labels), self.y_labels_major_every)]

        elif self.y_labels_major_count:
            label_count = len(self._y_labels)
            major_count = self.y_labels_major_count
            if (major_count >= label_count):
                self._y_labels_major = [label[1] for label in self._y_labels]
            else:
                self._y_labels_major = [self._y_labels[
                    int(i * (label_count - 1) / (major_count - 1))][1]
                    for i in range(major_count)]

        elif self.y_labels_major:
            self._y_labels_major = list(map(self._adapt, self.y_labels_major))
        elif self._y_labels:
            self._y_labels_major = majorize(cut(self._y_labels, 1))
        else:
            self._y_labels_major = []

    def add_squares(self, squares):
        x_lines = squares[0] - 1
        y_lines = squares[1] - 1

        _current_x = 0
        _current_y = 0

        for line in range(x_lines):
            _current_x += (self.width - self.margin_box.x) / squares[0]
            self.svg.node(
                self.nodes['plot'], 'path',
                class_='bg-lines',
                d='M%s %s L%s %s' % (
                    _current_x, 0, _current_x,
                    self.height - self.margin_box.y))

        for line in range(y_lines):
            _current_y += (self.height - self.margin_box.y) / squares[1]
            self.svg.node(
                self.nodes['plot'], 'path',
                class_='bg-lines',
                d='M%s %s L%s %s' % (
                    0, _current_y, self.width - self.margin_box.x, _current_y))
        return ((self.width - self.margin_box.x) / squares[0],
                (self.height - self.margin_box.y) / squares[1])

    def _draw(self):
        """Draw all the things"""
        self._compute()
        self._compute_x_labels()
        self._compute_x_labels_major()
        self._compute_y_labels()
        self._compute_y_labels_major()
        self._compute_secondary()
        self._post_compute()
        self._compute_margin()
        self._decorate()
        if self.series and self._has_data() and self._values:
            self._plot()
        else:
            self.svg.draw_no_data()

    def _has_data(self):
        """Check if there is any data"""
        return any([
            len([
                v for a in (s[0] if is_list_like(s) else [s])
                for v in (a if is_list_like(a) else [a])
                if v is not None])
            for s in self.raw_series
        ])
