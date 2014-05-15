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
from pygal import DateY
from pygal.test.utils import texts
from datetime import datetime


def test_date():
    datey = DateY(truncate_label=1000)
    datey.add('dates', [
        (datetime(2013, 1, 2), 300),
        (datetime(2013, 1, 12), 412),
        (datetime(2013, 2, 2), 823),
        (datetime(2013, 2, 22), 672)
    ])

    q = datey.render_pyquery()

    assert list(
        map(lambda t: t.split(' ')[0],
            q(".axis.x text").map(texts))) == [
        '2013-01-02',
        '2013-01-13',
        '2013-01-25',
        '2013-02-05',
        '2013-02-17'
    ]

    datey.x_labels = [
        datetime(2013, 1, 1),
        datetime(2013, 2, 1),
        datetime(2013, 3, 1)
    ]

    q = datey.render_pyquery()
    assert list(
        map(lambda t: t.split(' ')[0],
            q(".axis.x text").map(texts))) == [
        '2013-01-01',
        '2013-02-01',
        '2013-03-01'
    ]


def test_date_overflow():
    datey = DateY(truncate_label=1000)
    datey.add('dates', [1, 2, -1000000, 5, 100000000])
    assert datey.render_pyquery()
