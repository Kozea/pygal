# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
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
from flask import Flask, render_template, request
from pygal import CHARTS_BY_NAME
from pygal.graph import CHARTS_NAMES
from pygal.config import Config
from pygal.style import styles
from json import loads


def create_app():
    """Creates the pygal test web app"""

    app = Flask(__name__)

    @app.route("/")
    def index():
        configs = Config()._items
        return render_template(
            'index.jinja2', charts_names=CHARTS_NAMES, configs=dict(configs),
            styles_names=styles.keys())

    @app.route("/svg", methods=('POST',))
    def svg():
        values = request.values
        chart = CHARTS_BY_NAME[values['type']](
            disable_xml_declaration=True,
            style=styles[values['style']], **loads(values['opts']))
        for title, vals in loads(values['vals']).items():
            chart.add(title, vals)
        return chart.render_response()

    return app
