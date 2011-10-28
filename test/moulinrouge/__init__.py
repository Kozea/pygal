# -*- coding: utf-8 -*-
from flask import Flask, Response, render_template, url_for
from log_colorizer import make_colored_stream_handler
from logging import getLogger, INFO, WARN, DEBUG
from moulinrouge.data import labels, series
from pygal.bar import VerticalBar, HorizontalBar
from pygal.line import Line
from pygal.pie import Pie
import string
import random


def random_label():
    chars = string.letters + string.digits + u' àéèçêâäëï'
    return ''.join(
            [random.choice(chars)
             for i in range(
                     random.randrange(4, 30))])


def random_value():
    return random.randrange(0, 15, 1)


def generate_vbar(**opts):
    g = VerticalBar(labels, opts)
    for serie, values in series.items():
        g.add_data({'data': values, 'title': serie})

    return Response(g.burn(), mimetype='image/svg+xml')


def create_app():
    """Creates the pygal test web app"""

    app = Flask(__name__)
    handler = make_colored_stream_handler()
    getLogger('werkzeug').addHandler(handler)
    getLogger('werkzeug').setLevel(INFO)
    getLogger('pygal').addHandler(handler)
    getLogger('pygal').setLevel(DEBUG)

    @app.route("/")
    def index():
        return render_template('index.jinja2')

    @app.route("/all-<type>.svg")
    def all_svg(type):
        series = random.randrange(1, 10)
        data = random.randrange(1, 10)

        labels = [random_label() for i in range(data)]

        if type == 'vbar':
            g = VerticalBar(labels)
        elif type == 'hbar':
            g = HorizontalBar(labels)
        elif type == 'pie':
            series = 1
            g = Pie({'fields': labels})
        elif type == 'line':
            g = Line({'fields': labels})

        for i in range(series):
            values = [random_value() for i in range(data)]
            g.add_data({'data': values, 'title': random_label()})

        return Response(g.burn(), mimetype='image/svg+xml')

    @app.route("/all")
    def all():
        width, height = 800, 600
        svgs = [url_for('all_svg', type=type) for type in
                ('vbar', 'hbar', 'line', 'pie')]
        return render_template('svgs.jinja2',
                               svgs=svgs,
                               width=width,
                               height=height)

    @app.route("/rotation[<int:angle>].svg")
    def rotation_svg(angle):
        return generate_vbar(
            show_graph_title=True,
            graph_title="Rotation %d" % angle,
            x_label_rotation=angle)

    @app.route("/rotation")
    def rotation():
        width, height = 375, 245
        svgs = [url_for('rotation_svg', angle=angle)
                for angle in range(0, 91, 5)]
        return render_template('svgs.jinja2',
                               svgs=svgs,
                               width=width,
                               height=height)

    return app
