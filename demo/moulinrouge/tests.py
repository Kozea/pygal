# -*- coding: utf-8 -*-
# This file is part of pygal
from pygal import (
    Bar, Gauge, Pyramid, Funnel, Dot, StackedBar,
    CHARTS_BY_NAME, Config, Line)
from pygal.style import styles


def get_test_routes(app):
    lnk = lambda v, l=None: {
        'value': v,
        'xlink': 'javascript:alert("Test %s")' % v,
        'label': l}

    @app.route('/test/unsorted')
    def test_unsorted():
        bar = Bar(style=styles['neon'])
        bar.add('A', {'red': 10, 'green': 12, 'blue': 14})
        bar.add('B', {'green': 11, 'blue': 7})
        bar.add('C', {'blue': 7})
        bar.add('D', {})
        bar.add('E', {'blue': 2, 'red': 13})
        bar.x_labels = ('red', 'green', 'blue')
        return bar.render_response()

    @app.route('/test/bar_links')
    def test_bar_links():
        bar = Bar(style=styles['neon'])
        bar.add('1234', [
            {'value': 10,
             'label': 'Ten',
             'xlink': 'http://google.com?q=10'},
            {'value': 20,
             'label': 'Twenty',
             'xlink': 'http://google.com?q=20'},
            30,
            {'value': 40,
             'label': 'Forty',
             'xlink': 'http://google.com?q=40'}
        ])

        bar.add('4321', [40, {
            'value': 30,
            'label': 'Thirty',
            'xlink': 'http://google.com?q=30'
        }, 20, 10])
        bar.x_labels = map(str, range(1, 5))
        bar.logarithmic = True
        bar.zero = 1
        return bar.render_response()

    @app.route('/test/none')
    def test_bar_none():
        bar = Bar()
        bar.add('Lol', [2, None, 12])
        return bar.render_response()

    @app.route('/test/gauge')
    def test_gauge():
        gauge = Gauge()

        gauge.range = [-10, 10]
        gauge.add('Need l', [2.3, 5.12])
        gauge.add('No', [99, -99])
        return gauge.render_response()

    @app.route('/test/pyramid')
    def test_pyramid():
        pyramid = Pyramid()

        pyramid.x_labels = ['0-25', '25-45', '45-65', '65+']
        pyramid.add('Man single', [2, 4, 2, 1])
        pyramid.add('Woman single', [10, 6, 1, 1])
        pyramid.add('Man maried', [10, 3, 4, 2])
        pyramid.add('Woman maried', [3, 3, 5, 3])

        return pyramid.render_response()

    @app.route('/test/funnel')
    def test_funnel():
        funnel = Funnel()

        funnel.add('1', [1, 2, 3])
        funnel.add('3', [3, 4, 5])
        funnel.add('6', [6, 5, 4])
        funnel.add('12', [12, 2, 9])

        return funnel.render_response()

    @app.route('/test/dot')
    def test_dot():
        dot = Dot()
        dot.x_labels = map(str, range(4))

        dot.add('a', [1, lnk(3, 'Foo'), 5, 3])
        dot.add('b', [2, 2, 0, 2])
        dot.add('c', [5, 1, 5, lnk(3, 'Bar')])
        dot.add('d', [5, 5, lnk(0, 'Babar'), 3])

        return dot.render_response()

    @app.route('/test/interpolate/<chart>')
    def test_interpolate_for(chart):
        graph = CHARTS_BY_NAME[chart](interpolate='cubic')
        graph.add('1', [1, 3, 12, 3, 4])
        graph.add('2', [7, -4, 10, None, 8, 3, 1])
        return graph.render_response()

    @app.route('/test/stacked')
    def test_stacked():
        stacked = StackedBar()
        stacked.add('1', [1, 2, 3])
        stacked.add('2', [4, 5, 6])
        return stacked.render_response()

    @app.route('/test/show_dots')
    def test_show_dots():
        line = Line(show_dots=False)
        line.add('1', [1, 2, 3])
        line.add('2', [4, 5, 6])
        return line.render_response()

    @app.route('/test/config')
    def test_config():

        class LolConfig(Config):
            js = ['http://l:2343/svg.jquery.js',
                  'http://l:2343/pygal-tooltips.js']

        stacked = StackedBar(LolConfig())
        stacked.add('1', [1, 2, 3])
        stacked.add('2', [4, 5, 6])
        return stacked.render_response()

    return filter(lambda x: x.startswith('test'), locals())
