# -*- coding: utf-8 -*-
from flask import Flask, Response, render_template, url_for
from log_colorizer import make_colored_stream_handler
from logging import getLogger, INFO, WARN, DEBUG
from moulinrouge.data import labels, series
from pygal.bar import VerticalBar


def generate_vbar(**opts):
    opts.setdefault('width', 375)
    opts.setdefault('height', 245)

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
    getLogger('pygal').setLevel(INFO)

    @app.route("/")
    def index():
        return render_template('index.jinja2')

    @app.route("/rotation[<int:angle>].svg")
    def rotation_svg(angle):
        return generate_vbar(
            title="Rotation %d" % angle,
            x_label_rotation=angle)

    @app.route("/rotation")
    def rotation():
        svgs = [url_for('rotation_svg', angle=angle)
                for angle in range(0, 180, 10)]
        return render_template('svgs.jinja2', svgs=svgs)

    return app
