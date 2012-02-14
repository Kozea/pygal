# -*- coding: utf-8 -*-
from flask import Flask, Response, render_template, url_for
from log_colorizer import make_colored_stream_handler
from moulinrouge.data import labels, series
from logging import getLogger, INFO, DEBUG
import pygal
from pygal.config import Config
from pygal.style import styles
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
        if type != 'Pie':
            config.x_labels = [random_label() for i in range(data)]
        config.title = "%d - %d" % (min, max)
        g = getattr(pygal, type)(config)

        for i in range(random.randrange(1, 10)):
            if type == 'Pie':
                values = random_value(min, max)
            elif type == 'XY':
                values = [(
                    random_value((-max, min)[random.randrange(0, 2)], max),
                    random_value((-max, min)[random.randrange(0, 2)], max))
                          for i in range(data)]
            else:
                values = [random_value((-max, min)[random.randrange(0, 2)],
                                       max) for i in range(data)]
            g.add(random_label(), values)
        return g.render_response()

    @app.route("/all")
    def all():
        width, height = 600, 400
        svgs = [url_for('all_svg', type=type, style=style)
                for style in styles
                for type in ('Bar', 'Line', 'XY', 'Pie', 'StackedBar',
                          'HorizontalBar', 'HorizontalStackedBar', 'Radar')]
        return render_template('svgs.jinja2',
                               svgs=svgs,
                               width=width,
                               height=height)

    @app.route("/rotation[<int:angle>].svg")
    def rotation_svg(angle):
        config = Config()
        config.width = 375
        config.height = 245
        config.x_labels = labels
        config.x_label_rotation = angle
        g = pygal.Line(config)
        for serie, values in series.items():
            g.add(serie, values)

        g.add(serie, values)
        return g.render_response()

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
        g = pygal.Line(600, 400)
        g.x_labels = ['a', 'b', 'c', 'd']
        g.add('serie', [11, 50, 133, 2])
        return g.render_response()

    @app.route("/bigline")
    def big_line():
        width, height = 900, 800
        svgs = [url_for('big_line_svg')]
        return render_template('svgs.jinja2',
                               svgs=svgs,
                               width=width,
                               height=height)

    return app
