# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2013 Kozea
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
from flask import Flask, render_template, Response
import pygal
from pygal.config import Config
from pygal.util import cut
from pygal.graph import CHARTS_NAMES
from pygal.style import styles
from base64 import (
    urlsafe_b64encode as b64encode,
    urlsafe_b64decode as b64decode)
import string
import random
import pickle


def random_label():
    chars = string.letters + string.digits + u' àéèçêâäëï'
    return ''.join(
        [random.choice(chars)
         for i in range(random.randrange(4, 30))])


def random_value(min=0, max=15):
    return random.randrange(min, max, 1)


def create_app():
    """Creates the pygal test web app"""

    app = Flask(__name__)

    def _random(data, order):
        max = 10 ** order
        min = 10 ** random.randrange(0, order)

        series = []
        for i in range(random.randrange(1, 10)):
            values = [(
                random_value((-max, min)[random.randrange(0, 2)], max),
                random_value((-max, min)[random.randrange(0, 2)], max)
            ) for i in range(data)]
            series.append((random_label(), values))
        return series

    def _random_series(type, data, order):
        max = 10 ** order
        min = 10 ** random.randrange(0, order)

        series = []
        for i in range(random.randrange(1, 10)):
            if type == 'Pie':
                values = random_value(min, max)
            elif type == 'XY':
                values = [(
                    random_value((-max, min)[random.randrange(0, 2)], max),
                    random_value((-max, min)[random.randrange(0, 2)], max))
                    for i in range(data)]
            else:
                values = [random_value((-max, min)[random.randrange(1, 2)],
                                       max) for i in range(data)]
            series.append((random_label(), values))
        return series

    from .tests import get_test_routes
    links = get_test_routes(app)

    @app.route("/")
    def index():
        return render_template(
            'index.jinja2', styles=styles,
            links=links, charts_name=CHARTS_NAMES)

    @app.route("/svg/<type>/<series>/<config>")
    def svg(type, series, config):
        graph = getattr(pygal, type)(pickle.loads(b64decode(str(config))))
        for title, values in pickle.loads(b64decode(str(series))):
            graph.add(title, values)
        return graph.render_response()

    @app.route("/sparkline/<style>")
    def sparkline(style):
        line = pygal.Line(style=styles[style])
        line.add('_', [random.randrange(0, 10) for _ in range(25)])
        return Response(
            line.render_sparkline(height=40), mimetype='image/svg+xml')

    @app.route("/all")
    @app.route("/all/style=<style>")
    @app.route("/all/interpolate=<interpolate>")
    def all(style='default', interpolate=None):
        width, height = 600, 400
        data = random.randrange(1, 10)
        order = random.randrange(1, 10)
        xy_series = _random(data, order)
        other_series = []
        for title, values in xy_series:
            other_series.append(
                (title, cut(values, 1)))
        xy_series = b64encode(pickle.dumps(xy_series))
        other_series = b64encode(pickle.dumps(other_series))
        config = Config()
        config.width = width
        config.height = height
        config.fill = bool(random.randrange(0, 2))
        config.human_readable = True
        config.interpolate = interpolate
        config.style = styles[style]
        config.x_labels = [random_label() for i in range(data)]
        svgs = []
        for chart in pygal.CHARTS:
            type = chart.__name__
            svgs.append({'type': type,
                         'series': xy_series if type == 'XY' else other_series,
                         'config': b64encode(pickle.dumps(config))})

        return render_template('svgs.jinja2',
                               svgs=svgs,
                               width=width,
                               height=height)

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
        for angle in range(0, 91, 5):
            config.title = "%d rotation" % angle
            config.x_labels = labels
            config.x_label_rotation = angle
            svgs.append({'type': 'Bar',
                         'series': series,
                         'config': b64encode(pickle.dumps(config))})

        return render_template('svgs.jinja2',
                               svgs=svgs,
                               width=width,
                               height=height)

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
            svgs.append({'type': 'StackedLine',
                         'series': series,
                         'config': b64encode(pickle.dumps(config))})

        for params in [
                {'type': 'catmull_rom'},
                {'type': 'finite_difference'},
                {'type': 'cardinal', 'c': .25},
                {'type': 'cardinal', 'c': .5},
                {'type': 'cardinal', 'c': .75},
                {'type': 'cardinal', 'c': 1.5},
                {'type': 'cardinal', 'c': 2},
                {'type': 'cardinal', 'c': 5},
                {'type': 'kochanek_bartels', 'b': 1, 'c': 1, 't': 1},
                {'type': 'kochanek_bartels', 'b': -1, 'c': 1, 't': 1},
                {'type': 'kochanek_bartels', 'b': 1, 'c': -1, 't': 1},
                {'type': 'kochanek_bartels', 'b': 1, 'c': 1, 't': -1},
                {'type': 'kochanek_bartels', 'b': -1, 'c': 1, 't': -1},
                {'type': 'kochanek_bartels', 'b': -1, 'c': -1, 't': 1},
                {'type': 'kochanek_bartels', 'b': -1, 'c': -1, 't': -1}
        ]:
            config.title = "Hermite interpolation with params %r" % params
            config.interpolate = 'hermite'
            config.interpolation_parameters = params
            svgs.append({'type': 'StackedLine',
                         'series': series,
                         'config': b64encode(pickle.dumps(config))})

        return render_template('svgs.jinja2',
                               svgs=svgs,
                               width=width,
                               height=height)
    return app
