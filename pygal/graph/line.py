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


class Line(Graph):
    """Line graph"""

    def __init__(self, *args, **kwargs):
        super(Line, self).__init__(*args, **kwargs)
        self._line_close = False

    def _get_value(self, values, i):
        return str(values[i][1])

    def line(self, serie_node, values):
        view_values = map(self.view, values)

        dots = self.svg.node(serie_node, class_="dots")
        for i, (x, y) in enumerate(view_values):
            dot = self.svg.node(dots, class_='dot')
            self.svg.node(dot, 'circle', cx=x, cy=y, r=2.5)
            self.svg.node(dot, 'text', x=x, y=y
            ).text = self._get_value(values, i)
        self.svg.line(
            serie_node, view_values, class_='line', close=self._line_close)

    def _compute(self):
        if self.include_x_axis:
            self._box.ymin = min(min(self._values), 0)
            self._box.ymax = max(max(self._values), 0)
        else:
            self._box.ymin = min(self._values)
            self._box.ymax = max(self._values)

        x_step = len(self.series[0].values)
        self._x_pos = [x / float(x_step - 1) for x in range(x_step)
        ] if x_step != 1 else [.5]  # Center if only one value
        self._y_pos = self._pos(self._box.ymin, self._box.ymax, self.y_scale
        ) if not self.y_labels else map(int, self.y_labels)

        self._x_labels = self.x_labels and zip(self.x_labels, self._x_pos)
        self._y_labels = zip(map(str, self._y_pos), self._y_pos)

    def _plot(self):
        for serie in self.series:
            self.line(
                self._serie(serie.index), [
                (self._x_pos[i], v)
                for i, v in enumerate(serie.values)])
