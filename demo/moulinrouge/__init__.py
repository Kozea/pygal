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
from flask import Flask, render_template, Response, request
import pygal
from pygal.config import Config
from pygal.util import cut
from pygal.etree import etree
from pygal.style import styles, parametric_styles
from base64 import (
    urlsafe_b64encode as b64encode, urlsafe_b64decode as b64decode
)
import string
import random
import pickle


def get(type):
    from importlib import import_module
    module = '.'.join(type.split('.')[:-1])
    name = type.split('.')[-1]
    return getattr(import_module(module), name)


def random_label():
    chars = string.ascii_letters + string.digits + u' àéèçêâäëï'
    return ''.join([
        random.choice(chars) for i in range(random.randrange(4, 30))
    ])


def random_value(min=0, max=15):
    return random.randrange(min, max, 1)


def create_app():
    """Creates the pygal test web app"""

    app = Flask(__name__)

    @app.before_request
    def before_request():
        if request.args.get('etree'):
            etree.to_etree()
        elif request.args.get('lxml'):
            etree.to_lxml()

    def _random(data, order):
        max = 10**order
        min = 10**random.randrange(0, order)

        series = []
        for i in range(random.randrange(1, 10)):
            values = [(
                random_value((-max, min)[random.randrange(0, 2)], max),
                random_value((-max, min)[random.randrange(0, 2)], max)
            ) for i in range(data)]
            series.append((random_label(), values, {}))
        return series

    def _random_series(type, data, order):
        max = 10**order
        min = 10**random.randrange(0, order)
        with_secondary = bool(random.randint(0, 1))
        series = []
        for i in range(random.randrange(1, 10)):
            if type == 'Pie':
                values = random_value(min, max)
            elif type == 'XY':
                values = [(
                    random_value((-max, min)[random.randrange(0, 2)], max),
                    random_value((-max, min)[random.randrange(0, 2)], max)
                ) for i in range(data)]
            else:
                values = [
                    random_value((-max, min)[random.randrange(1, 2)], max)
                    for i in range(data)
                ]
            config = {
                'secondary': with_secondary and bool(random.randint(0, 1))
            }
            series.append((random_label(), values, config))
        return series

    from .tests import get_test_routes
    links = get_test_routes(app)

    @app.route("/")
    def index():
        return render_template(
            'index.jinja2',
            styles=styles,
            parametric_styles=parametric_styles,
            parametric_colors=(
                '#ff5995', '#b6e354', '#feed6c', '#8cedff', '#9e6ffe'
            ),
            links=links,
            charts_name=pygal.CHARTS_NAMES
        )

    @app.route("/svg/<type>/<series>/<config>")
    def svg(type, series, config):
        graph = get(type)(pickle.loads(b64decode(str(config))))
        for title, values, serie_config in pickle.loads(b64decode(
                str(series))):
            graph.add(title, values, **serie_config)
        return graph.render_response()

    @app.route("/table/<type>/<series>/<config>")
    def table(type, series, config):
        graph = get(type)(pickle.loads(b64decode(str(config))))
        for title, values, serie_config in pickle.loads(b64decode(
                str(series))):
            graph.add(title, values, **serie_config)
        return graph.render_table()

    @app.route("/sparkline/<style>")
    @app.route("/sparkline/parameric/<style>/<color>")
    def sparkline(style, color=None):
        if color is None:
            style = styles[style]
        else:
            style = parametric_styles[style](color)

        line = pygal.Line(style=style, pretty_print=True)
        line.add('_', [random.randrange(0, 10) for _ in range(25)])
        return Response(
            line.render_sparkline(height=40), mimetype='image/svg+xml'
        )

    @app.route("/with/table/<type>")
    def with_table(type):
        chart = pygal.StackedBar(
            disable_xml_declaration=True, x_label_rotation=35
        )
        chart.title = (
            'What Linux distro do you primarily use'
            ' on your server computers? (Desktop'
            ' users vs Server Users)'
        )

        if type == 'series':
            chart.add('Debian', [1775, 82])
            chart.add('Ubuntu', [1515, 80])
            chart.add('CentOS', [807, 60])
            chart.add('Arch Linux', [549, 12])
            chart.add('Red Hat Enterprise Linux', [247, 10])
            chart.add('Gentoo', [129, 7])
            chart.add('Fedora', [91, 6])
            chart.add('Amazon Linux', [60, 0])
            chart.add('OpenSUSE', [58, 0])
            chart.add('Slackware', [50, 3])
            chart.add('Xubuntu', [38, 1])
            chart.add('Rasbian', [33, 4])
            chart.add('SUSE Linux Enterprise Server', [33, 1])
            chart.add('Linux Mint', [30, 4])
            chart.add('Scientific Linux', [32, 0])
            chart.add('Other', [187, 5])

        elif type == 'labels':
            chart.x_labels = [
                'Debian', 'Ubuntu', 'CentOS', 'Arch Linux',
                'Red Hat Enterprise Linux', 'Gentoo', 'Fedora', 'Amazon Linux',
                'OpenSUSE', 'Slackware', 'Xubuntu', 'Rasbian',
                'SUSE Linux Enterprise Server', 'Linux Mint',
                'Scientific Linux', 'Other'
            ]
            chart.add(
                'Desktop Users', [
                    1775, 1515, 807, 549, 247, 129, 91, 60, 58, 50, 38, 33, 33,
                    30, 32, 187
                ]
            )
            chart.add(
                'Server Users',
                [82, 80, 60, 12, 10, 7, 6, 0, 0, 3, 1, 4, 1, 4, 0, 5]
            )

        return render_template('table.jinja2', chart=chart)

    @app.route("/all")
    @app.route("/all/<style>")
    @app.route("/all/<style>/<color>")
    @app.route("/all/<style>/<color>/<base_style>")
    @app.route("/all/interpolate=<interpolate>")
    def all(style='default', color=None, interpolate=None, base_style=None):
        width, height = 600, 400
        data = random.randrange(1, 10)
        order = random.randrange(1, 10)
        if color is None:
            style = styles[style]
        else:
            style = parametric_styles[style](
                color, base_style=styles[base_style or 'default']
            )

        xy_series = _random(data, order)
        other_series = []
        for title, values, config in xy_series:
            other_series.append((title, cut(values, 1), config))
        xy_series = b64encode(pickle.dumps(xy_series))
        other_series = b64encode(pickle.dumps(other_series))
        config = Config()
        config.width = width
        config.height = height
        config.fill = bool(random.randrange(0, 2))
        config.interpolate = interpolate
        config.style = style
        svgs = []
        for chart in pygal.CHARTS:
            type = '.'.join((chart.__module__, chart.__name__))
            if chart._dual:
                config.x_labels = None
            else:
                config.x_labels = [random_label() for i in range(data)]
            svgs.append({
                'type': type,
                'series': xy_series if chart._dual else other_series,
                'config': b64encode(pickle.dumps(config))
            })

        return render_template(
            'svgs.jinja2', svgs=svgs, width=width, height=height
        )

    @app.route("/rotation")
    def rotation():
        width, height = 375, 245
        config = Config()
        config.width = width
        config.height = height
        config.fill = True
        config.style = styles['neon']
        data = random.randrange(1, 10)
        order = random.randrange(1, 10)
        series = b64encode(pickle.dumps(_random_series(type, data, order)))
        labels = [random_label() for i in range(data)]
        svgs = []
        config.show_legend = bool(random.randrange(0, 2))
        for angle in range(0, 370, 10):
            config.title = "%d rotation" % angle
            config.x_labels = labels
            config.x_label_rotation = angle
            config.y_label_rotation = angle
            svgs.append({
                'type': 'pygal.Bar',
                'series': series,
                'config': b64encode(pickle.dumps(config))
            })

        return render_template(
            'svgs.jinja2', svgs=svgs, width=width, height=height
        )

    @app.route("/interpolation")
    def interpolation():
        width, height = 600, 400
        config = Config()
        config.width = width
        config.height = height
        config.fill = True
        config.style = styles['neon']
        data = random.randrange(1, 10)
        order = random.randrange(1, 10)
        series = b64encode(pickle.dumps(_random_series(type, data, order)))
        svgs = []
        for interpolation in 'quadratic', 'cubic', 'lagrange', 'trigonometric':
            config.title = "%s interpolation" % interpolation
            config.interpolate = interpolation
            svgs.append({
                'type': 'pygal.StackedLine',
                'series': series,
                'config': b64encode(pickle.dumps(config))
            })

        for params in [{'type': 'catmull_rom'}, {'type': 'finite_difference'},
                       {'type': 'cardinal',
                        'c': .25}, {'type': 'cardinal',
                                    'c': .5}, {'type': 'cardinal', 'c': .75},
                       {'type': 'cardinal',
                        'c': 1.5}, {'type': 'cardinal',
                                    'c': 2}, {'type': 'cardinal', 'c': 5},
                       {'type': 'kochanek_bartels', 'b': 1, 'c': 1,
                        't': 1}, {'type': 'kochanek_bartels', 'b': -1, 'c': 1,
                                  't': 1}, {'type': 'kochanek_bartels', 'b': 1,
                                            'c': -1, 't': 1},
                       {'type': 'kochanek_bartels', 'b': 1, 'c': 1, 't': -1}, {
                           'type': 'kochanek_bartels', 'b': -1, 'c': 1, 't': -1
                       }, {'type': 'kochanek_bartels', 'b': -1, 'c': -1,
                           't': 1}, {'type': 'kochanek_bartels', 'b': -1,
                                     'c': -1, 't': -1}]:
            config.title = "Hermite interpolation with params %r" % params
            config.interpolate = 'hermite'
            config.interpolation_parameters = params
            svgs.append({
                'type': 'pygal.StackedLine',
                'series': series,
                'config': b64encode(pickle.dumps(config))
            })

        return render_template(
            'svgs.jinja2', svgs=svgs, width=width, height=height
        )

    @app.route("/raw_svgs/")
    def raw_svgs():
        svgs = []
        for color in styles['neon'].colors:
            chart = pygal.Pie(
                style=parametric_styles['rotate'](color),
                width=400,
                height=300
            )
            chart.title = color
            chart.disable_xml_declaration = True
            chart.explicit_size = True
            chart.js = ['http://l:2343/2.0.x/pygal-tooltips.js']
            for i in range(6):
                chart.add(str(i), 2**i)
            svgs.append(chart.render())
        return render_template('raw_svgs.jinja2', svgs=svgs)

    return app
