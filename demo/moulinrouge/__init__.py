# -*- coding: utf-8 -*-
from flask import Flask, Response, render_template, url_for
from log_colorizer import make_colored_stream_handler
from logging import getLogger, INFO, WARN, DEBUG
from moulinrouge.data import labels, series
# from pygal.bar import VerticalBar, HorizontalBar
from pygal.line import Line
from pygal.bar import Bar
from pygal.config import Config
from pygal.style import styles
# from pygal.pie import Pie
import math
import string
import random


def random_label():
    chars = string.letters + string.digits + u' àéèçêâäëï'
    return ''.join(
            [random.choice(chars)
             for i in range(
                     random.randrange(4, 30))])


def random_value(min=0, max=15):
    return random.randrange(min, max, 1)


# def generate_vbar(**opts):
#     g = VerticalBar(labels, opts)
#     for serie, values in series.items():
#         g.add_data({'data': values, 'title': serie})

#     return Response(g.burn(), mimetype='image/svg+xml')


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

    @app.route("/all-<type>-<style>.svg")
    def all_svg(type, style):
        data = random.randrange(1, 10)
        order = random.randrange(1, 10)
        max = 10 ** order
        min = 10 ** random.randrange(0, order)
        config = Config()
        config.width = 600
        config.height = 400
        config.style = styles[style]
        config.x_labels = [random_label() for i in range(data)]
        config.title = "%d - %d" % (min, max)
        if type == 'bar':
            g = Bar(config)
        # elif type == 'hbar':
            # g = HorizontalBar(labels)
        # elif type == 'pie':
            # series = 1
            # g = Pie({'fields': labels})
        elif type == 'line':
            g = Line(config)
        else:
            return

        for i in range(random.randrange(1, 10)):
            values = [random_value(min, max) for i in range(data)]
            g.add(random_label(), values)

        return Response(g.render(), mimetype='image/svg+xml')

    @app.route("/all")
    def all():
        width, height = 600, 400
        svgs = [url_for('all_svg', type=type, style=style)
                for style in styles
                for type in ('bar', 'line')]
        return render_template('svgs.jinja2',
                               svgs=svgs,
                               width=width,
                               height=height)

    # @app.route("/rotation[<int:angle>].svg")
    # def rotation_svg(angle):
    #     return generate_vbar(
    #         show_graph_title=True,
    #         graph_title="Rotation %d" % angle,
    #         x_label_rotation=angle)

    @app.route("/rotation")
    def rotation():
        width, height = 375, 245
        svgs = [url_for('rotation_svg', angle=angle)
                for angle in range(0, 91, 5)]
        return render_template('svgs.jinja2',
                               svgs=svgs,
                               width=width,
                               height=height)

    @app.route("/bigline.svg")
    def big_line_svg():
        g = Line(600, 400)
        g.x_labels = ['a', 'b', 'c', 'd']
        g.add('serie', [11, 50, 133, 2])
        return Response(g.render(), mimetype='image/svg+xml')

    @app.route("/bigline")
    def big_line():
        width, height = 900, 800
        svgs = [url_for('big_line_svg')]
        return render_template('svgs.jinja2',
                               svgs=svgs,
                               width=width,
                               height=height)

    return app
