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
Table maker

"""

from pygal.graph.base import BaseGraph
from lxml.html import builder, tostring


class HTML(object):
    def __getattribute__(self, attr):
        return getattr(builder, attr.upper())


class Table(BaseGraph):
    _dual = None

    def __init__(self, config, series, secondary_series, uuid, xml_filters):
        "Init the table"
        self.uuid = uuid
        self.series = series or []
        self.secondary_series = secondary_series or []
        self.xml_filters = xml_filters or []
        self.__dict__.update(config.to_dict())
        self.config = config

    def render(self, total=False, transpose=False):
        html = HTML()
        table = []

        _ = lambda x: x if x is not None else ''

        table.append([None])
        labels = []
        if self.x_labels:
            labels += self.x_labels
        if len(labels) < self._len:
            labels += [None] * (self._len - len(labels))
        if len(labels) > self._len:
            labels = labels[:self._len]

        for label in labels:
            table[0].append(label)

        if total:
            table[0].append('Total')
            acc = [0] * (self._len + 1)

        for i, serie in enumerate(self.series):
            row = [serie.title]
            if total:
                sum_ = 0
            for j, value in enumerate(serie.values):
                if total:
                    acc[j] += value
                    sum_ += value
                row.append(self._format(value))
            if total:
                acc[-1] += sum_
                row.append(self._format(sum_))
            table.append(row)

        width = self._len + 1
        if total:
            width += 1
            table.append(['Total'])
            for val in acc:
                table[-1].append(self._format(val))

        # Align values
        len_ = max([len(r) for r in table] or [0])

        for i, row in enumerate(table[:]):
            len_ = len(row)
            if len_ < width:
                table[i] = row + [None] * (width - len_)

        if not transpose:
            table = list(zip(*table))

        table = tostring(
            html.table(
                html.tbody(
                    *[html.tr(
                        *[html.td(_(col)) for col in r]
                    ) for r in table]
                )
            )
        )
        if self.disable_xml_declaration:
            table = table.decode('utf-8')
        return table
