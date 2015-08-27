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
Radar chart: As known as kiviat chart or spider chart is a polar line chart
useful for multivariate observation.
"""

from __future__ import division

from math import cos, pi

from pygal._compat import is_str
from pygal.adapters import none_to_zero, positive
from pygal.graph.line import Line
from pygal.util import (
    cached_property, compute_scale, cut, deg, truncate)
from pygal.view import PolarLogView, PolarView


class Radar(Line):

    """Rada graph class"""

    _adapters = [positive, none_to_zero]

    def __init__(self, *args, **kwargs):
        """Init custom vars"""
        self._rmax = None
        super(Radar, self).__init__(*args, **kwargs)

    def _fill(self, values):
        """Add extra values to fill the line"""
        return values

    def _get_value(self, values, i):
        """Get the value formatted for tooltip"""
        return self._format(values[i][0])

    @cached_property
    def _values(self):
        """Getter for series values (flattened)"""
        if self.interpolate:
            return [val[0] for serie in self.series
                    for val in serie.interpolated]
        else:
            return super(Line, self)._values

    def _set_view(self):
        """Assign a view to current graph"""
        if self.logarithmic:
            view_class = PolarLogView
        else:
            view_class = PolarView

        self.view = view_class(
            self.width - self.margin_box.x,
            self.height - self.margin_box.y,
            self._box)

    def _x_axis(self, draw_axes=True):
        """Override x axis to make it polar"""
        if not self._x_labels or not self.show_x_labels:
            return

        axis = self.svg.node(self.nodes['plot'], class_="axis x web%s" % (
            ' always_show' if self.show_x_guides else ''
        ))
        format_ = lambda x: '%f %f' % x
        center = self.view((0, 0))
        r = self._rmax

        # Can't simply determine truncation
        truncation = self.truncate_label or 25

        for label, theta in self._x_labels:
            major = label in self._x_major_labels
            if not (self.show_minor_x_labels or major):
                continue
            guides = self.svg.node(axis, class_='guides')
            end = self.view((r, theta))

            self.svg.node(
                guides, 'path',
                d='M%s L%s' % (format_(center), format_(end)),
                class_='%s%sline' % (
                    'axis ' if label == "0" else '',
                    'major ' if major else ''))

            r_txt = (1 - self._box.__class__.margin) * self._box.ymax
            pos_text = self.view((r_txt, theta))
            text = self.svg.node(
                guides, 'text',
                x=pos_text[0],
                y=pos_text[1],
                class_='major' if major else '')
            text.text = truncate(label, truncation)
            if text.text != label:
                self.svg.node(guides, 'title').text = label
            else:
                self.svg.node(
                    guides, 'title',
                ).text = self._x_format(theta)

            angle = - theta + pi / 2
            if cos(angle) < 0:
                angle -= pi
            text.attrib['transform'] = 'rotate(%f %s)' % (
                self.x_label_rotation or deg(angle), format_(pos_text))

    def _y_axis(self, draw_axes=True):
        """Override y axis to make it polar"""
        if not self._y_labels or not self.show_y_labels:
            return

        axis = self.svg.node(self.nodes['plot'], class_="axis y web")

        for label, r in reversed(self._y_labels):
            major = r in self._y_major_labels
            if not (self.show_minor_y_labels or major):
                continue
            guides = self.svg.node(axis, class_='%sguides' % (
                'logarithmic ' if self.logarithmic else ''
            ))
            if self.show_y_guides:
                self.svg.line(
                    guides, [self.view((r, theta)) for theta in self._x_pos],
                    close=True,
                    class_='%sguide line' % (
                        'major ' if major else ''))
            x, y = self.view((r, self._x_pos[0]))
            x -= 5
            text = self.svg.node(
                guides, 'text',
                x=x,
                y=y,
                class_='major' if major else ''
            )
            text.text = label

            if self.y_label_rotation:
                text.attrib['transform'] = "rotate(%d %f %f)" % (
                    self.y_label_rotation, x, y)

            self.svg.node(
                guides, 'title',
            ).text = self._format(r)

    def _compute(self):
        """Compute r min max and labels position"""
        delta = 2 * pi / self._len if self._len else 0
        self._x_pos = [.5 * pi + i * delta for i in range(self._len + 1)]
        for serie in self.all_series:
            serie.points = [
                (v, self._x_pos[i])
                for i, v in enumerate(serie.values)]
            if self.interpolate:
                extended_x_pos = (
                    [.5 * pi - delta] + self._x_pos)
                extended_vals = (serie.values[-1:] +
                                 serie.values)
                serie.interpolated = list(
                    map(tuple,
                        map(reversed,
                            self._interpolate(
                                extended_x_pos, extended_vals))))

        # x labels space
        self._box.margin *= 2
        self._rmin = self.zero
        self._rmax = self._max or 1
        self._box.set_polar_box(self._rmin, self._rmax)
        self._self_close = True

    def _compute_y_labels(self):
        y_pos = compute_scale(
            self._rmin, self._rmax, self.logarithmic, self.order_min,
            self.min_scale, self.max_scale / 2
        )
        if self.y_labels:
            self._y_labels = []
            for i, y_label in enumerate(self.y_labels):
                if isinstance(y_label, dict):
                    pos = self._adapt(y_label.get('value'))
                    title = y_label.get('label', self._format(pos))
                elif is_str(y_label):
                    pos = self._adapt(y_pos[i])
                    title = y_label
                else:
                    pos = self._adapt(y_label)
                    title = self._format(pos)
                self._y_labels.append((title, pos))
            self._rmin = min(self._rmin, min(cut(self._y_labels, 1)))
            self._rmax = max(self._rmax, max(cut(self._y_labels, 1)))
            self._box.set_polar_box(self._rmin, self._rmax)

        else:
            self._y_labels = list(zip(map(self._format, y_pos), y_pos))
