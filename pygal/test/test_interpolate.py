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
"""Interpolations tests"""

from pygal.test import make_data


def test_cubic(Chart, datas):
    """Test cubic interpolation"""
    chart = Chart(interpolate='cubic')
    chart = make_data(chart, datas)
    assert chart.render()


def test_cubic_prec(Chart, datas):
    """Test cubic interpolation precision"""
    chart = Chart(interpolate='cubic', interpolation_precision=200)
    chart = make_data(chart, datas)

    chart_low = Chart(interpolate='cubic', interpolation_precision=5)
    chart_low = make_data(chart, datas)

    assert len(chart.render()) >= len(chart_low.render())


def test_quadratic(Chart, datas):
    """Test quadratic interpolation"""
    chart = Chart(interpolate='quadratic')
    chart = make_data(chart, datas)
    assert chart.render()


def test_lagrange(Chart, datas):
    """Test lagrange interpolation"""
    chart = Chart(interpolate='lagrange')
    chart = make_data(chart, datas)
    assert chart.render()


def test_trigonometric(Chart, datas):
    """Test trigonometric interpolation"""
    chart = Chart(interpolate='trigonometric')
    chart = make_data(chart, datas)
    assert chart.render()


def test_hermite(Chart, datas):
    """Test hermite interpolation"""
    chart = Chart(interpolate='hermite')
    chart = make_data(chart, datas)
    assert chart.render()


def test_hermite_finite(Chart, datas):
    """Test hermite finite difference interpolation"""
    chart = Chart(
        interpolate='hermite',
        interpolation_parameters={'type': 'finite_difference'}
    )
    chart = make_data(chart, datas)
    assert chart.render()


def test_hermite_cardinal(Chart, datas):
    """Test hermite cardinal interpolation"""
    chart = Chart(
        interpolate='hermite',
        interpolation_parameters={
            'type': 'cardinal',
            'c': .75
        }
    )
    chart = make_data(chart, datas)
    assert chart.render()


def test_hermite_catmull_rom(Chart, datas):
    """Test hermite catmull rom interpolation"""
    chart = Chart(
        interpolate='hermite',
        interpolation_parameters={'type': 'catmull_rom'}
    )
    chart = make_data(chart, datas)
    assert chart.render()


def test_hermite_kochanek_bartels(Chart, datas):
    """Test hermite kochanek bartels interpolation"""
    chart = Chart(
        interpolate='hermite',
        interpolation_parameters={
            'type': 'kochanek_bartels',
            'b': -1,
            'c': 1,
            't': 1
        }
    )
    chart = make_data(chart, datas)
    assert chart.render()

    chart = Chart(
        interpolate='hermite',
        interpolation_parameters={
            'type': 'kochanek_bartels',
            'b': -1,
            'c': -8,
            't': 0
        }
    )
    chart = make_data(chart, datas)
    assert chart.render()

    chart = Chart(
        interpolate='hermite',
        interpolation_parameters={
            'type': 'kochanek_bartels',
            'b': 0,
            'c': 10,
            't': -1
        }
    )
    chart = make_data(chart, datas)
    assert chart.render()
