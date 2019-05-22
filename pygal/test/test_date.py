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

"""Date related charts tests"""

from datetime import date, datetime, time, timedelta

from pygal import DateLine, DateTimeLine, TimeDeltaLine, TimeLine
from pygal._compat import timestamp, utc
from pygal.test.utils import texts


def test_date():
    """Test a simple dateline"""
    date_chart = DateLine(truncate_label=1000)
    date_chart.add('dates', [
        (date(2013, 1, 2), 300),
        (date(2013, 1, 12), 412),
        (date(2013, 2, 2), 823),
        (date(2013, 2, 22), 672)
    ])

    q = date_chart.render_pyquery()

    assert list(
        map(lambda t: t.split(' ')[0],
            q(".axis.x text").map(texts))) == [
                '2013-01-12',
                '2013-01-24',
                '2013-02-04',
                '2013-02-16']


def test_time():
    """Test a simple timeline"""
    time_chart = TimeLine(truncate_label=1000)
    time_chart.add('times', [
        (time(1, 12, 29), 2),
        (time(21, 2, 29), 10),
        (time(12, 30, 59), 7)
    ])

    q = time_chart.render_pyquery()

    assert list(
        map(lambda t: t.split(' ')[0],
            q(".axis.x text").map(texts))) == [
                '02:46:40',
                '05:33:20',
                '08:20:00',
                '11:06:40',
                '13:53:20',
                '16:40:00',
                '19:26:40']


def test_datetime():
    """Test a simple datetimeline"""
    datetime_chart = DateTimeLine(truncate_label=1000)
    datetime_chart.add('datetimes', [
        (datetime(2013, 1, 2, 1, 12, 29), 300),
        (datetime(2013, 1, 12, 21, 2, 29), 412),
        (datetime(2013, 2, 2, 12, 30, 59), 823),
        (datetime(2013, 2, 22), 672)
    ])

    q = datetime_chart.render_pyquery()

    assert list(
        map(lambda t: t.split(' ')[0],
            q(".axis.x text").map(texts))) == [
                '2013-01-12T14:13:20',
                '2013-01-24T04:00:00',
                '2013-02-04T17:46:40',
                '2013-02-16T07:33:20']


def test_timedelta():
    """Test a simple timedeltaline"""
    timedelta_chart = TimeDeltaLine(truncate_label=1000)
    timedelta_chart.add('timedeltas', [
        (timedelta(seconds=1), 10),
        (timedelta(weeks=1), 50),
        (timedelta(hours=3, seconds=30), 3),
        (timedelta(microseconds=12112), .3),
    ])

    q = timedelta_chart.render_pyquery()
    assert list(
        t for t in q(".axis.x text").map(texts) if t != '0:00:00'
    ) == [
        '1 day, 3:46:40',
        '2 days, 7:33:20',
        '3 days, 11:20:00',
        '4 days, 15:06:40',
        '5 days, 18:53:20',
        '6 days, 22:40:00']


def test_date_xrange():
    """Test dateline with xrange"""
    datey = DateLine(truncate_label=1000)
    datey.add('dates', [
        (date(2013, 1, 2), 300),
        (date(2013, 1, 12), 412),
        (date(2013, 2, 2), 823),
        (date(2013, 2, 22), 672)
    ])

    datey.xrange = (date(2013, 1, 1), date(2013, 3, 1))

    q = datey.render_pyquery()
    assert list(
        map(lambda t: t.split(' ')[0],
            q(".axis.x text").map(texts))) == [
                '2013-01-01',
                '2013-01-12',
                '2013-01-24',
                '2013-02-04',
                '2013-02-16',
                '2013-02-27']


def test_date_labels():
    """Test dateline with xrange"""
    datey = DateLine(truncate_label=1000)
    datey.add('dates', [
        (date(2013, 1, 2), 300),
        (date(2013, 1, 12), 412),
        (date(2013, 2, 2), 823),
        (date(2013, 2, 22), 672)
    ])

    datey.x_labels = [
        date(2013, 1, 1),
        date(2013, 2, 1),
        date(2013, 3, 1)
    ]

    q = datey.render_pyquery()
    assert list(
        map(lambda t: t.split(' ')[0],
            q(".axis.x text").map(texts))) == [
                '2013-01-01',
                '2013-02-01',
                '2013-03-01']


def test_utc_timestamping():
    assert timestamp(
        datetime(2017, 7, 14, 2, 40).replace(tzinfo=utc)
    ) == 1500000000

    for d in (
        datetime.now(),
        datetime.utcnow(),
        datetime(1999, 12, 31, 23, 59, 59),
        datetime(2000, 1, 1, 0, 0, 0)
    ):
        assert datetime.utcfromtimestamp(
            timestamp(d)) - d < timedelta(microseconds=10)
