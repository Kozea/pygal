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
from pygal.util import template
from lxml.html import builder, tostring
import uuid


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

    def render(self, total=False, transpose=False, style=False):
        html = HTML()
        attrs = {}

        if style:
            attrs['id'] = 'table-%s' % uuid.uuid4()

        table = []

        _ = lambda x: x if x is not None else ''

        if self.x_labels:
            labels = [None] + list(self.x_labels)
            if len(labels) < self._len:
                labels += [None] * (self._len + 1 - len(labels))
            if len(labels) > self._len + 1:
                labels = labels[:self._len + 1]
            table.append(labels)

        if total:
            if len(table):
                table[0].append('Total')
            else:
                table.append([None] * (self._len + 1) + ['Total'])
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

        thead = []
        tbody = []
        tfoot = []

        if not transpose or self.x_labels:
            # There's always series title but not always x_labels
            thead = [table[0]]
            tbody = table[1:]
        else:
            tbody = table

        if total:
            tfoot = [tbody[-1]]
            tbody = tbody[:-1]

        parts = []
        if thead:
            parts.append(
                html.thead(
                    *[html.tr(
                        *[html.th(_(col)) for col in r]
                    ) for r in thead]
                )
            )
        if tbody:
            parts.append(
                html.tbody(
                    *[html.tr(
                        *[html.td(_(col)) for col in r]
                    ) for r in tbody]
                )
            )
        if tfoot:
            parts.append(
                html.tfoot(
                    *[html.tr(
                        *[html.th(_(col)) for col in r]
                    ) for r in tfoot]
                )
            )

        table = tostring(
            html.table(
                *parts, **attrs
            )
        )
        if style:
            if style is True:
                css = '''
                #{{ id }} {
                    border-collapse: collapse;
                    border-spacing: 0;
                    empty-cells: show;
                    border: 1px solid #cbcbcb;
                }
                #{{ id }} td, #{{ id }} th {
                    border-left: 1px solid #cbcbcb;
                    border-width: 0 0 0 1px;
                    margin: 0;
                    padding: 0.5em 1em;
                }
                #{{ id }} td:first-child, #{{ id }} th:first-child {
                    border-left-width: 0;
                }
                #{{ id }} thead, #{{ id }} tfoot {
                    color: #000;
                    text-align: left;
                    vertical-align: bottom;
                }
                #{{ id }} thead {
                    background: #e0e0e0;
                }
                #{{ id }} tfoot {
                    background: #ededed;
                }
                #{{ id }} tr:nth-child(2n-1) td {
                    background-color: #f2f2f2;
                }
                '''
            else:
                css = style
            table = tostring(html.style(
                template(css, **attrs),
                scoped='scoped')) + table
        if self.disable_xml_declaration:
            table = table.decode('utf-8')
        return table
