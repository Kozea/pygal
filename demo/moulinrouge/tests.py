# -*- coding: utf-8 -*-
# This file is part of pygal
from datetime import date, datetime
from random import choice, randint

from flask import abort
from pygal import (
    CHARTS_BY_NAME, XY, Bar, Box, Config, DateLine, DateTimeLine, Dot, Funnel,
    Gauge, Histogram, HorizontalBar, Line, Pie, Pyramid, Radar, SolidGauge,
    StackedBar, StackedLine, TimeLine, Treemap, formatters, stats
)
from pygal.colors import rotate
from pygal.graph.horizontal import HorizontalGraph
from pygal.style import RotateStyle, Style, styles

try:
    from pygal.maps import world
except ImportError:
    world = None

try:
    from pygal.maps import fr
except ImportError:
    fr = None

try:
    from pygal.maps import ch
except ImportError:
    ch = None


def get_test_routes(app):
    lnk = lambda v, l=None: {
        'value': v,
        'xlink': 'javascript:alert("Test %s")' % v,
        'label': l}

    @app.route('/test/unsorted')
    def test_unsorted():
        bar = Bar(
            style=styles['neon'], value_formatter=formatters.human_readable
        )
        bar.add('A', {'red': 10, 'green': 12, 'blue': 14})
        bar.add('B', {'green': 11, 'blue': 7})
        bar.add('C', {'blue': 7})
        bar.add('D', {})
        bar.add('E', {'blue': 2, 'red': 13})
        bar.x_labels = ('red', 'green', 'blue')
        return bar.render_response()

    @app.route('/test/bar_links')
    def test_bar_links():
        bar = StackedLine(
            style=styles['default'](font_family='googlefont:Raleway')
        )
        bar.js = ('http://l:2343/2.0.x/pygal-tooltips.js', )
        bar.title = 'Wow ! Such Chart !'
        bar.x_title = 'Many x labels'
        bar.y_title = 'Much y labels'
        bar.dynamic_print_values = True

        bar.add(
            'Red serie', [{
                'value': 10,
                'label': 'Ten',
                'xlink': 'http://google.com?q=10'
            }, {
                'value': 20,
                'label':
                    'Twenty is a good number yada yda yda yada '
                    'yadaaaaaaaaaaaaaaaaaaaaaa',
                'xlink': 'http://google.com?q=20'
            }, 30, {
                'value': 40,
                'label': 'Forty',
                'xlink': 'http://google.com?q=40'
            }]
        )

        bar.add(
            'Blue serie', [
                40, {
                    'value': 30,
                    'label': 'Thirty',
                    'xlink': 'http://google.com?q=30'
                }, 20, 10
            ]
        )
        bar.x_labels = [
            'Yesterday', 'Today or any other day', 'Tomorrow', 'Someday'
        ]
        bar.logarithmic = True
        # bar.zero = 1
        return bar.render_response()

    @app.route('/test/xy_links')
    def test_xy_links():
        xy = XY(style=styles['neon'], interpolate='cubic')
        xy.add(
            '1234', [{
                'value': (10, 5),
                'label': 'Ten',
                'xlink': 'http://google.com?q=10'
            }, {
                'value': (20, 20),
                'tooltip': 'Twenty',
                'xlink': 'http://google.com?q=20'
            }, (30, 15), {
                'value': (40, -5),
                'label': 'Forty',
                'xlink': 'http://google.com?q=40'
            }]
        )

        xy.add(
            '4321', [(40, 10), {
                'value': (30, 3),
                'label': 'Thirty',
                'xlink': 'http://google.com?q=30'
            }, (20, 10), (10, 21)]
        )
        xy.x_labels = list(range(1, 50))
        xy.y_labels = list(range(1, 50))
        return xy.render_response()

    @app.route('/test/long_title')
    def test_long_title():
        bar = Bar()
        bar.add('Looooooooooooooooooooooooooooooooooong', [2, None, 12])
        bar.title = (
            '1 12 123 1234 12345 123456 1234567 12345678 123456789 1234567890 '
            '12345678901 123456789012 1234567890123 12345678901234 '
            '123456789012345 1234567890123456 12345678901234567 '
            '123456789012345678 1234567890123456789 12345678901234567890 '
            '123456789012345 1234567890123456 12345678901234567 '
            '12345678901 123456789012 1234567890123 12345678901234 '
            '1 12 123 1234 12345 123456 1234567 12345678 123456789 1234567890'
        )
        return bar.render_response()

    @app.route('/test/multiline_title')
    def test_multiline_title():
        bar = Bar()
        bar.add('Looooooooooooooooooooooooooooooooooong', [2, None, 12])
        bar.title = ('First line \n Second line \n Third line')
        return bar.render_response()

    @app.route('/test/long_labels')
    def test_long_labels():
        bar = Bar()
        bar.add('Long', [2, None, 12])
        bar.title = (
            '1 12 123 1234 12345 123456 1234567 12345678 123456789 1234567890'
        )
        bar.x_labels = 'a' * 100, 'b ' * 50, 'cc ! ' * 20
        bar.x_label_rotation = 45
        return bar.render_response()

    @app.route('/test/none')
    def test_bar_none():
        bar = Bar()
        bar.add('Lol', [2, None, 12])
        bar.x_labels = range(1, 4)
        return bar.render_response()

    @app.route('/test/print_values/<chart>')
    def test_print_values_for(chart):
        graph = CHARTS_BY_NAME[chart](
            print_values=True,
            print_labels=True,
            print_zeroes=True,
            style=styles['default'](
                value_font_family='googlefont:Raleway',
                value_colors=(None, None, 'blue', 'red', 'green')
            )
        )
        graph.js = ('http://l:2343/2.0.x/pygal-tooltips.js', )
        for i in range(12):
            graph.add(
                '', [{
                    'value': i + j,
                    'label': 'abcdefghijklmnopqrstuvwxyz' [i + j]
                } for j in range(5)]
            )
        return graph.render_response()

    @app.route('/test/treemap')
    def test_treemap():
        treemap = Treemap(
            style=RotateStyle(
                '#ff5995',
                opacity=.6,
                value_font_size=32,
                value_colors=['#ffffff']
            )
        )
        treemap.title = 'Binary TreeMap'
        treemap.print_values = True
        treemap.print_labels = True
        for i in range(1, 5):
            treemap.add('', [{'label': 'Area %d' % i, 'value': i}])
        treemap.add('', [2])
        # treemap.add('A', [2, 1, 12, 4, 2, 1, 1, 3, 12, 3, 4, None, 9])
        # treemap.add('B', [4, 2, 5, 10, 3, 4, 2, 7, 4, -10, None, 8, 3, 1])
        # treemap.add('C', [3, 8, 3, 3, 5, 3, 3, 5, 4, 12])
        # treemap.add('D', [23, 18])
        # treemap.add('E', [1, 2, 1, 2, 3, 3, 1, 2, 3,
        #                   4, 3, 1, 2, 1, 1, 1, 1, 1])
        # treemap.add('F', [31])
        # treemap.add('G', [5, 9.3, 8.1, 12, 4, 3, 2])
        # treemap.add('H', [12, 3, 3])
        return treemap.render_response()

    @app.route('/test/gauge')
    def test_gauge():
        gauge = Gauge()

        gauge.range = [-10, 10]
        gauge.add('Need l', [2.3, 5.12])
        gauge.add('Need m', [-4])
        gauge.add('Need z', [-10, 10.5])
        gauge.add('No', [99, -99])
        gauge.y_labels = [{
            'label': 'X',
            'value': 6
        }, {
            'label': '><',
            'value': -6
        }]
        return gauge.render_response()

    @app.route('/test/solidgauge/')
    def test_solidgauge():
        gauge = SolidGauge(
            half_pie=True,
            inner_radius=0.70,
            print_values=not True,
            human_readable=True
        )
        gauge.title = 'Hello World!'
        percent_formatter = lambda x: '{:.10g}%'.format(x)
        dollar_formatter = lambda x: '{:.10g}$'.format(x)
        gauge.value_formatter = percent_formatter

        gauge.add(
            'Series 1', [{
                'value': 225000,
                'max_value': 1275000
            }],
            formatter=dollar_formatter
        )
        gauge.add('Series 2', [{'value': 110, 'max_value': 100}])
        gauge.add('Series 3', [{'value': 3}])
        gauge.add(
            'Series 4', [{
                'value': 51,
                'max_value': 100
            }, {
                'value': 12,
                'max_value': 100
            }]
        )
        gauge.add('Series 5', [{'value': 79, 'max_value': 100}])
        gauge.add('Series 6', 99)
        gauge.add('Series 7', [{'value': 100, 'max_value': 100}])
        return gauge.render_response()

    @app.route('/test/gauge/log')
    def test_gauge_log():
        gauge = Gauge(logarithmic=True)

        gauge.add('Need l', [200.3, 500.12])
        gauge.add('Need z', [10, 1000.5])
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
        dot = Dot(logarithmic=True)
        dot.x_labels = map(str, range(4))
        dot.add('a', [1, lnk(3, 'Foo'), 5, 3])
        dot.add('b', [2, -2, 0, 2, .1])
        dot.add('c', [5, 1, 50, lnk(3, 'Bar')])
        dot.add('d', [-5, 5, lnk(0, 'Babar'), 3])

        return dot.render_response()

    @app.route('/test/<chart>')
    def test_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        graph.add('1', [1, 3, 12, 3, 4, None, 9])
        graph.add('2', [7, -4, 10, None, 8, 3, 1])
        graph.add('3', [7, -14, -10, None, 8, 3, 1])
        graph.add('4', [7, 4, -10, None, 8, 3, 1])
        graph.x_labels = ('a', 'b', 'c', 'd')
        graph.x_label_rotation = 90
        return graph.render_response()

    @app.route('/test/<chart>')
    def test_call_api_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        graph(1, 3, 12, 3, 4, None, 9, title='1')
        graph(7, -4, 10, None, 8, 3, 1, title='2')
        graph(7, -14, -10, None, 8, 3, 1, title='3')
        graph(7, 4, -10, None, 8, 3, 1, title='4')
        graph.x_labels = ('a', 'b', 'c', 'd')
        graph.x_label_rotation = 90
        return graph.render_response()

    @app.route('/test/one/<chart>')
    def test_one_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        graph.add('1', [10])
        graph.x_labels = 'a',
        return graph.render_response()

    @app.route('/test/xytitles/<chart>')
    def test_xy_titles_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        graph.title = 'My global title'
        graph.x_title = 'My X title'
        graph.y_title = 'My Y title'
        graph.add('My number 1 serie', [1, 3, 12])
        graph.add('My number 2 serie', [7, -4, 10])
        graph.add('A', [17, -14, 11], secondary=True)
        graph.x_label_rotation = 25
        graph.legend_at_bottom = not True
        graph.x_labels = ('First point', 'Second point', 'Third point')
        return graph.render_response()

    @app.route('/test/no_data/<chart>')
    def test_no_data_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        graph.add('Empty 1', [])
        graph.add('Empty 2', [])
        graph.x_labels = 'empty'
        graph.title = '123456789 ' * 30
        return graph.render_response()

    @app.route('/test/xy_single')
    def test_xy_single():
        graph = XY(interpolate='cubic')
        graph.add('Single', [(1, 1)])
        return graph.render_response()

    @app.route('/test/no_data/at_all/<chart>')
    def test_no_data_at_all_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        return graph.render_response()

    @app.route('/test/interpolate/<chart>')
    def test_interpolate_for(chart):
        graph = CHARTS_BY_NAME[chart](
            interpolate='lagrange',
            interpolation_parameters={
                'type': 'kochanek_bartels',
                'c': 1,
                'b': -1,
                't': -1
            }
        )
        graph.add('1', [1, 3, 12, 3, 4])
        graph.add('2', [7, -4, 10, None, 8, 3, 1])
        return graph.render_response()

    @app.route('/test/logarithmic/<chart>')
    def test_logarithmic_for(chart):
        graph = CHARTS_BY_NAME[chart](logarithmic=True)
        if isinstance(graph, CHARTS_BY_NAME['XY']):
            graph.add(
                'xy', [(.1, .234), (10, 243), (.001, 2), (1000000, 1231)]
            )
        else:
            graph.add('1', [.1, 10, .01, 10000])
            graph.add('2', [.234, 243, 2, 2379, 1231])
            graph.x_labels = ('a', 'b', 'c', 'd', 'e')
        graph.x_label_rotation = 90
        return graph.render_response()

    @app.route('/test/zero_at_34/<chart>')
    @app.route('/test/zero_at_<int:zero>/<chart>')
    def test_zero_at_34_for(chart, zero=34):
        graph = CHARTS_BY_NAME[chart](fill=True, zero=zero)
        graph.add('1', [100, 34, 12, 43, -48])
        graph.add('2', [73, -14, 10, None, -58, 32, 91])
        return graph.render_response()

    @app.route('/test/range/<chart>')
    def test_range_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        graph.range = [0, 100]
        graph.add('1', [1, 2, 10])
        return graph.render_response()

    @app.route('/test/fill_with_none/')
    def test_fill_with_none():
        graph = XY(fill=True)
        graph.add('1', [(1, 2), (3, 3), (3.5, 5), (5, 1)])
        graph.add('2', [(1, 9), (None, 5), (5, 23)])
        return graph.render_response()

    @app.route('/test/negative/<chart>')
    def test_negative_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        graph.add('1', [10, 0, -10])
        return graph.render_response()

    @app.route('/test/bar')
    def test_bar():
        bar = Bar(dynamic_print_values=True, show_minor_x_labels=False)
        bar.add('1', [1, 2, 3])
        bar.add('2', [4, 5, 6])
        bar.x_labels = [2, 4, 6]
        bar.x_labels_major = [4]
        return bar.render_response()

    @app.route('/test/formatters/<chart>')
    def test_formatters_for(chart):
        chart = CHARTS_BY_NAME[chart](
            print_values=True,
            formatter=lambda x, chart, serie: '%s%s$' % (x, serie.title)
        )
        chart.add('_a', [1, 2, {'value': 3, 'formatter': lambda x: '%s¥' % x}])
        chart.add('_b', [4, 5, 6], formatter=lambda x: '%s€' % x)
        chart.x_labels = [2, 4, 6]
        chart.x_labels_major = [4]
        return chart.render_response()

    @app.route('/test/bar/position')
    def test_bar_print_values_position():
        bar = StackedBar(
            print_values=True,
            print_values_position='top',
            zero=2,
            style=styles['default'](
                value_font_family='googlefont:Raleway', value_font_size=46
            )
        )
        bar.add('1', [1, -2, 3])
        bar.add('2', [4, -5, 6])
        bar.x_labels = [2, 4, 6]
        bar.x_labels_major = [4]
        return bar.render_response()

    @app.route('/test/histogram')
    def test_histogram():
        hist = Histogram(
            print_values=True,
            print_values_position='top',
            style=styles['neon']
        )
        hist.add('1', [(2, 0, 1), (4, 1, 3), (3, 3.5, 5), (1.5, 5, 10)])
        hist.add('2', [(2, 2, 8)])
        hist.x_labels = [0, 3, 6, 9, 12]
        return hist.render_response()

    @app.route('/test/ylabels')
    def test_ylabels():
        chart = Bar()
        chart.x_labels = 'Red', 'Blue', 'Green'
        chart.y_labels = [{
            'value': .0001,
            'label': 'LOL'
        }, {
            'value': .0003,
            'label': 'ROFL'
        }, {
            'value': .0004,
            'label': 'MAO'
        }, {
            'value': .00045,
            'label': 'LMFAO'
        }, {
            'value': .0005,
            'label': 'GMCB'
        }]
        chart.add('line', [.0002, .0005, .00035])
        return chart.render_response()

    @app.route('/test/secondary/<chart>')
    def test_secondary_for(chart):
        chart = CHARTS_BY_NAME[chart](fill=True)
        chart.title = 'LOL ' * 23
        chart.x_labels = 'abc'
        chart.x_label_rotation = 25
        chart.y_label_rotation = 50
        chart.add('1', [30, 20, -2])
        chart.add('1b', [-4, 50, 6], secondary=True)
        chart.add('2b', [None, 10, 20], secondary=True)
        chart.add('2', [8, 21, -0])
        chart.add('3', [None, 20, 10])
        chart.add('3b', [-1, 2, -3], secondary=True)
        return chart.render_response()

    @app.route('/test/secondary_xy')
    def test_secondary_xy():
        chart = XY()
        chart.add(10 * '1', [(30, 5), (20, 12), (25, 4)])
        chart.add(10 * '1b', [(4, 12), (5, 8), (6, 4)], secondary=True)
        chart.add(10 * '2b', [(3, 24), (0, 17), (12, 9)], secondary=True)
        chart.add(10 * '2', [(8, 23), (21, 1), (5, 0)])
        chart.value_formatter = lambda x: str(int(x)) + '+'
        return chart.render_response()

    @app.route('/test/box')
    def test_box():
        chart = Box()
        # chart.js = ('http://l:2343/2.0.x/pygal-tooltips.js',)
        chart.box_mode = '1.5IQR'
        chart.add('One', [15, 8, 2, -12, 9, 23])
        chart.add('Two', [5, 8, 2, -9, 23, 12])
        chart.add('Three', [8, -2, 12, -5, 9, 3])
        chart.add('Four', [5, 8, 2, -9, -3, 12])
        chart.add('Five', [8, 12, 12, -9, 5, 13])
        chart.x_labels = map(str, range(5))
        return chart.render_response()

    @app.route('/test/stacked')
    def test_stacked():
        stacked = StackedLine(stack_from_top=True, logarithmic=True)
        stacked.add('1', [1, 2])
        stacked.add('2', [10, 12])
        stacked.x_labels = ['a', 'b', 'c', 'd']
        return stacked.render_response()

    @app.route('/test/stacked/reverse')
    def test_stacked_reverse():
        stacked = StackedBar(stack_from_top=True)
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
            js = ['http://l:2343/2.0.x/pygal-tooltips.js']

        stacked = StackedBar(LolConfig())
        stacked.add('', [1, 2, 3])
        stacked.add('My beautiful serie of 2019', [4, 5, 6])
        return stacked.render_response()

    @app.route('/test/dateline')
    def test_dateline():
        dateline = DateLine(y_label_rotation=112)
        dateline.x_labels = [
            date(2013, 1, 1),
            date(2013, 7, 1),
            date(2014, 1, 1),
            date(2014, 7, 1),
            date(2015, 1, 1),
            date(2015, 7, 1)
        ]
        dateline.x_labels_major = [date(2013, 1, 1), date(2015, 7, 1)]
        dateline.add(
            "Serie", [(date(2013, 1, 2), 213), (date(2013, 8, 2), 281),
                      (date(2013, 5, 31), 281), (date(2014, 12, 7), 198),
                      (date(2014, 9, 6), 198), (date(2015, 3, 21), 120)]
        )
        return dateline.render_response()

    @app.route('/test/timeline')
    def test_timexy():
        from datetime import time
        timeline = TimeLine()
        timeline.add(
            '1', [(time(1, 12, 29), 2), (time(21, 2, 29), 10),
                  (time(12, 30, 59), 7)]
        )
        timeline.add(
            '2', [(time(12, 12, 12), 4), (time(), 8), (time(23, 59, 59), 6)]
        )
        timeline.x_label_rotation = 25
        return timeline.render_response()

    @app.route('/test/worldmap')
    def test_worldmap():
        wmap = world.World(
            print_values=True, style=choice(list(styles.values()))
        )
        # wmap.js = ('http://l:2343/2.0.x/pygal-tooltips.js',)
        # wmap.add('1st', [('fr', 100), {
        #     'value': ('us', 10),
        #     'node': {'style': 'fill: red'}
        # }
        # ])
        # wmap.add('2nd', [('jp', 1), ('ru', 7), ('uk', 0)])
        # wmap.add('3rd', ['ch', 'cz', 'ca', 'cn'])
        # wmap.add('4th', {'jp': 12, 'bo': 1, 'bu': 23, 'fr': 34})
        # wmap.add('5th', [{
        #     'value': ('tw', 10),
        #     'label': 'First label',
        #     'xlink': 'http://google.com?q=tw',
        # }, {
        #     'value': ('bw', 20),
        #     'label': 'Second one',
        #     'xlink': 'http://google.com?q=bw',
        #     'node': {'style': 'fill: blue'}
        # }, {
        #     'value': ('mw', 40),
        #     'label': 'Last'
        # }])
        wmap.add('_', {'us': 1})
        wmap.add('-', {'us': 2})
        wmap.add('.', {'us': 3})
        wmap.title = 'World Map !!'
        wmap.value_formatter = lambda x: '%d%%' % x
        return wmap.render_response()

    @app.route('/test/supranational')
    def test_supranational():
        wmap = world.SupranationalWorld(style=choice(list(styles.values())))
        v = [('europe', 0), ('oceania', 2), ('antartica', 4),
             ('south_america', 5), ('africa', 6), ('north_america',
                                                   7), ('asia', 8)]
        wmap.add(
            'Serie with metadata', [
                v[0], {
                    'value': v[1]
                }, {
                    'value': v[2],
                    'label': 'Three'
                }, {
                    'value': v[3],
                    'xlink': 'http://4.example.com/'
                }, {
                    'value': v[4],
                    'xlink': 'http://5.example.com/',
                    'label': 'Five'
                }, {
                    'value': v[5],
                    'xlink': {
                        'href': 'http://6.example.com/'
                    },
                    'label': 'Six'
                }, {
                    'value': v[6],
                    'xlink': {
                        'href': 'http://7.example.com/',
                        'target': '_blank'
                    },
                    'label': 'Seven'
                }
            ]
        )
        # wmap.add('Asia', [('asia', 1)])
        # wmap.add('Europe', [('europe', 1)])
        # wmap.add('Africa', [('africa', 1)])
        # wmap.add('North america', [('north_america', 1)])
        # wmap.add('South america', [('south_america', 1)])
        # wmap.add('Oceania', [('oceania', 1)])
        # wmap.add('Antartica', [('antartica', 1)])

        wmap.title = 'Supra World Map !!'
        return wmap.render_response()

    @app.route('/test/frenchmapdepartments')
    def test_frenchmapdepartments():
        if fr is None:
            abort(404)
        fmap = fr.Departments(style=choice(list(styles.values())))
        fmap.add('', [(i, i) for i in range(1, 100)])
        fmap.add('', [(970 + i, i) for i in range(1, 7)])
        fmap.add('', [('2A', 1), ('2B', 2)])
        fmap.title = 'French map'
        return fmap.render_response()

    @app.route('/test/swissmap')
    def test_swissmap():
        smap = ch.Cantons(style=choice(list(styles.values())))
        for i in range(10):
            smap.add(
                's%d' % i, [(choice(list(ch.CANTONS.keys())), randint(0, 100))
                            for _ in range(randint(1, 5))]
            )

        smap.add(
            'links', [{
                'value': ('kt-vs', 10),
                'label': '\o/',
                'xlink': 'http://google.com?q=69'
            }, {
                'value': ('bt', 20),
                'label': 'Y',
            }]
        )
        smap.add('6th', [3, 5, 34, 12])
        smap.title = 'Swiss map'
        return smap.render_response()

    @app.route('/test/frenchmapregions')
    def test_frenchmapregions():
        if fr is None:
            abort(404)
        fmap = fr.Regions(style=choice(list(styles.values())))
        for i in range(10):
            fmap.add(
                's%d' % i, [(choice(list(fr.REGIONS.keys())), randint(0, 100))
                            for _ in range(randint(1, 5))]
            )

        fmap.add(
            'links', [{
                'value': ('02', 10),
                'label': '\o/',
                'xlink': 'http://google.com?q=69'
            }, {
                'value': ('72', 20),
                'label': 'Y',
            }]
        )
        fmap.add('6th', [91, 2, 41])
        fmap.title = 'French map'
        return fmap.render_response()

    @app.route('/test/labels')
    def test_labels():
        line = Line()
        line.add('test1', range(100))
        line.x_labels = map(str, range(11))
        return line.render_response()

    @app.route('/test/64colors')
    def test_64_colors():
        n = 64
        colors = [rotate('#ff0000', i * 360 / n) for i in range(n)]
        pie = Pie(style=Style(colors=colors))
        for i in range(n):
            pie(1, title=str(i) if i % 5 == 1 else None)
        return pie.render_response()

    @app.route('/test/major_dots')
    def test_major_dots():
        line = Line(x_labels_major_count=2, show_only_major_dots=True)
        line.add('test', range(12))
        line.x_labels = [
            'lol', 'lol1', 'lol2', 'lol3', 'lol4', 'lol5', 'lol6', 'lol7',
            'lol8', 'lol9', 'lol10', 'lol11'
        ]
        # line.x_labels_major = ['lol3']
        return line.render_response()

    @app.route('/test/x_major_labels/<chart>')
    def test_x_major_labels_for(chart):
        chart = CHARTS_BY_NAME[chart](show_minor_y_labels=False)
        for i in range(12):
            chart.add('test', range(12))
        chart.x_labels = map(str, range(12))
        # chart.x_labels_major_count = 4
        # chart.x_labels_major = ['1', '5', '11', 6]
        # chart.y_labels_major = [60, 120]
        return chart.render_response()

    @app.route('/test/y_major_labels/<chart>')
    def test_y_major_labels_for(chart):
        chart = CHARTS_BY_NAME[chart]()
        chart.add('test', range(12))
        # chart.add('test', zip(*[range(12), range(12)]))
        chart.y_labels = range(12)
        # chart.y_labels_major_count = 4
        chart.y_labels_major = [1.0, 5.0, 11.0]
        return chart.render_response()

    @app.route('/test/stroke_config')
    def test_stroke_config():
        line = Line(stroke_style={'width': .5})
        line.add('test_no_line', range(12), stroke=False)
        line.add('test', reversed(range(12)), stroke_style={'width': 3})
        line.add(
            'test_no_dots', [5] * 12,
            show_dots=False,
            stroke_style={
                'width': 2,
                'dasharray': '12, 31'
            }
        )
        line.add(
            'test_big_dots', [randint(1, 12) for _ in range(12)], dots_size=5
        )
        line.add(
            'test_fill', [randint(1, 3) for _ in range(12)],
            fill=True,
            stroke_style={
                'width': 5,
                'dasharray': '4, 12, 7, 20'
            }
        )

        line.x_labels = [
            'lol', 'lol1', 'lol2', 'lol3', 'lol4', 'lol5', 'lol6', 'lol7',
            'lol8', 'lol9', 'lol10', 'lol11'
        ]
        return line.render_response()

    @app.route('/test/radar')
    def test_radar():
        radar = Radar()
        for i in range(10):
            radar.add(str(i), [i * j for j in range(8)])
        radar.x_labels = [
            'lol', 'rofl', 'mao', 'lolroflmao', '12345678901234567890'
        ]
        radar.x_label_rotation = 35
        radar.y_label_rotation = 35
        radar.y_labels = [{
            'label': '500',
            'value': 10
        }, {
            'label': '1000',
            'value': 20
        }, {
            'label': '5000',
            'value': 30
        }, {
            'label': '10000',
            'value': 40
        }]
        return radar.render_response()

    @app.route('/test/pie_serie_radius')
    def test_pie_serie_radius():
        pie = Pie()
        pie.js = ('http://a.zi:2343/2.0.x/pygal-tooltips.js', )
        for i in range(10):
            pie.add(str(i), i, inner_radius=(10 - i) / 10)

        return pie.render_response()

    @app.route('/test/half_pie')
    def test_half_pie():
        pie = Pie(half_pie=True)
        for i in range(20):
            pie.add(str(i), i, inner_radius=.1)
        pie.legend_at_bottom = True
        pie.legend_at_bottom_columns = 4
        return pie.render_response()

    @app.route('/test/interpolate/secondary')
    def test_interpolate_secondary():
        chart = Line(title=u'Some different points', interpolate='cubic')
        chart.add('line', [1000, 2000, 7000])
        chart.add('other line', [100, 500, 500], secondary=True)
        chart.range = 0, 10000
        chart.secondary_range = 0, 1000
        return chart.render_response()

    @app.route('/test/legend_at_bottom/<chart>')
    def test_legend_at_bottom_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        graph.add('1', [1, 3, 12, 3, 4, None, 9])
        graph.add('2', [7, -4, 10, None, 8, 3, 1])
        graph.add('3', [7, -14, -10, None, 8, 3, 1])
        graph.add('4', [7, 4, -10, None, 8, 3, 1])
        graph.x_labels = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        graph.legend_at_bottom = True
        return graph.render_response()

    @app.route('/test/custom_metadata/<chart>')
    def test_custom_metadata_for(chart):
        c = CHARTS_BY_NAME[chart]()
        c.add(
            '1', [{
                'style': 'fill: red',
                'value': 1,
                'node': {
                    'r': 12
                }
            }, {
                'color': 'blue',
                'value': 2,
                'node': {
                    'width': 12
                }
            }, {
                'style': 'fill: red; stroke: yellow',
                'value': 3
            }]
        )
        c.add(
            '2', [{
                'value': 4,
                'xlink': {
                    'href': 'javascript:alert("-")',
                    'target': 'top',
                    'class': 'lol'
                }
            }, {
                'color': 'green',
                'value': 5
            }, 6]
        )
        return c.render_response()

    @app.route('/test/sparkline/<chart>')
    def test_sparkline_for(chart):
        graph = CHARTS_BY_NAME[chart](
            **dict(
                width=200,
                height=50,
                show_dots=False,
                show_legend=False,
                show_y_labels=False,
                show_x_labels=False,
                spacing=0,
                margin=5,
                explicit_size=True
            )
        )
        graph.add('1', [1, 3, 12, 3, 4, None, 9])
        graph.add('2', [7, -4, 10, None, 8, 3, 1])
        graph.add('3', [7, -14, -10, None, 8, 3, 1])
        graph.add('4', [7, 4, -10, None, 8, 3, 1])
        graph.x_labels = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        graph.legend_at_bottom = True
        return graph.render_response()

    @app.route('/test/sparkline/label/<chart>')
    def test_sparkline_label_for(chart):
        graph = CHARTS_BY_NAME[chart](
            **dict(
                width=200,
                height=50,
                show_dots=False,
                show_legend=False,
                # show_y_labels=False,
                # show_x_labels=False,
                spacing=0,
                margin=5,
                min_scale=2,
                max_scale=2,
                explicit_size=True
            )
        )
        graph.add('1', [1, 3, 12, 3, 4, None, 9])
        graph.add('2', [7, -4, 10, None, 8, 3, 1])
        graph.add('3', [7, -14, -10, None, 8, 3, 1])
        graph.add('4', [7, 4, -10, None, 8, 3, 1])
        graph.x_labels = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        graph.legend_at_bottom = True
        return graph.render_response()

    @app.route('/test/normal/<chart>')
    def test_normal_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        graph.add('1', [1, 3, 12, 3, 4, None, 9])
        graph.add('2', [7, -4, 10, None, 8, 3, 1])
        graph.add('3', [7, -14, -10, None, 8, 3, 1])
        graph.add('4', [7, 4, -10, None, 8, 3, 1])
        graph.x_labels = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        graph.legend_at_bottom = True
        return graph.render_response()

    @app.route('/test/horizontal_force/<chart>')
    def test_horizontal_force_for(chart):
        class H(CHARTS_BY_NAME[chart], HorizontalGraph):
            pass

        graph = H()

        graph.add('1', [1, 3, 12, 3, 4, None, 9])
        graph.add('2', [7, -4, 10, None, 8, 3, 1])
        graph.add('3', [7, -14, -10, None, 8, 3, 1])
        graph.add('4', [7, 4, -10, None, 8, 3, 1])
        graph.x_labels = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        graph.legend_at_bottom = True
        return graph.render_response()

    @app.route('/test/inverse_y_axis/<chart>')
    def test_inverse_y_axis_for(chart):
        graph = CHARTS_BY_NAME[chart](**dict(inverse_y_axis=True))
        graph.add('inverse', [1, 2, 3, 12, 24, 36])
        return graph.render_response()

    @app.route('/test/only_zeroes')
    def test_only_zeroes():
        line = Line()
        line.add('zeroes', [])
        line.add('zeroes 2', [0])
        return line.render_response()

    @app.route('/test/rotations/<chart>')
    def test_rotations_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        # graph.x_label_rotation = 290
        # graph.y_label_rotation = 0
        graph.add('lalalla al alallaa a 1', [1, 3, 12, 3, 4, None, 9])
        graph.add(
            'lalalla al alallaa a 2', [7, -4, 10, None, 8, 3, 1],
            secondary=True
        )
        graph.add('lalalla al alallaa a 3', [7, -14, -10, None, 8, 3, 1])
        graph.add(
            'lalalla al alallaa a 4', [7, 4, -10, None, 8, 3, 1],
            secondary=True
        )
        graph.x_labels = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        # graph.legend_at_bottom = True
        return graph.render_response()

    @app.route('/test/datetimeline')
    def test_datetimeline():
        line = DateTimeLine()
        from datetime import timezone, timedelta
        tz7 = timezone(timedelta(hours=7), 'GMT +7')
        tzn4 = timezone(timedelta(hours=-4), 'GMT -4')

        line.add(
            'dt', [(datetime(2013, 1, 12, 8, tzinfo=tz7), 300),
                   (datetime(2013, 1, 12, 8), 412),
                   (datetime(2013, 1, 12, 8, tzinfo=tzn4), 823)]
        )
        line.x_label_rotation = 45
        return line.render_response()

    @app.route('/test/datetimeline_with_pytz')
    def test_datetimeline_with_pytz():
        import pytz
        tz = pytz.timezone('US/Eastern')

        line = DateTimeLine()
        line.add(
            'dt', [(tz.localize(datetime(2013, 1, 12, 8)), 300),
                   (tz.localize(datetime(2013, 1, 12, 10)), 600),
                   (tz.localize(datetime(2013, 1, 12, 14)), 30),
                   (tz.localize(datetime(2013, 1, 12, 16)), 200)]
        )
        from datetime import timezone
        line.x_value_formatter = lambda x: (
            x.replace(tzinfo=timezone.utc).astimezone(tz)).isoformat()
        # line.x_value_formatter = lambda x: tz.normalize(
        #     x.replace(tzinfo=pytz.utc)).isoformat()
        line.x_label_rotation = 45
        return line.render_response()

    @app.route('/test/order_min')
    def test_order_min():
        line = Line(order_min=-32)
        line.add('_', [1, 32, 12, .4, .009])
        return line.render_response()

    @app.route('/test/custom_css_file')
    def test_custom_css_file():
        from tempfile import NamedTemporaryFile
        custom_css = '''
          {{ id }}text {
            fill: green;
            font-family: monospace;
          }
          {{ id }}.legends .legend text {
            font-size: {{ font_sizes.legend }};
          }
          {{ id }}.axis {
            stroke: #666;
          }
          {{ id }}.axis text {
            font-size: {{ font_sizes.label }};
            font-family: sans;
            stroke: none;
          }
          {{ id }}.axis.y text {
            text-anchor: end;
          }
          {{ id }}#tooltip text {
            font-size: {{ font_sizes.tooltip }};
          }
          {{ id }}.dot {
            fill: yellow;
          }
          {{ id }}.color-0 {
            stroke: #ff1100;
            fill: #ff1100;
          }
          {{ id }}.color-1 {
            stroke: #ffee00;
            fill: #ffee00;
          }
          {{ id }}.color-2 {
            stroke: #66bb44;
            fill: #66bb44;
          }
          {{ id }}.color-3 {
            stroke: #88bbdd;
            fill: #88bbdd;
          }
          {{ id }}.color-4 {
            stroke: #0000ff;
            fill: #0000ff;
          }
        '''
        custom_css_file = '/tmp/pygal_custom_style.css'
        with open(custom_css_file, 'w') as f:
            f.write(custom_css)
        config = Config(fill=True, interpolate='cubic')
        config.css.append(custom_css_file)
        chart = StackedLine(config)
        chart.add('A', [1, 3, 5, 16, 13, 3, 7])
        chart.add('B', [5, 2, 3, 2, 5, 7, 17])
        chart.add('C', [6, 10, 9, 7, 3, 1, 0])
        chart.add('D', [2, 3, 5, 9, 12, 9, 5])
        chart.add('E', [7, 4, 2, 1, 2, 10, 0])
        return chart.render_response()

    @app.route('/test/legendlink/<chart>')
    def test_legend_link_for(chart):
        chart = CHARTS_BY_NAME[chart]()
        # link on chart and label
        chart.add([{
            'value': 2,
            'label': 'This is red',
            'tooltip': 'LOOLLOLOLO',
            'xlink': {
                'href': 'http://en.wikipedia.org/wiki/Red'
            }
        }],
                  title={
                      'title': 'Red',
                      'tooltip': 'Cramoisi',
                      'xlink': {
                          'href': 'http://en.wikipedia.org/wiki/Red'
                      }
                  })

        chart.add({
            'title': 'Yellow',
            'xlink': {
                'href': 'http://en.wikipedia.org/wiki/Yellow',
                'target': '_blank'
            }
        }, 7)

        return chart.render_response()

    @app.route('/test/gradient/<chart>')
    def test_gradient_for(chart):

        config = Config()
        config.style = styles['dark']
        config.defs.append(
            '''
          <linearGradient id="gradient-0" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stop-color="#ff5995" />
            <stop offset="100%" stop-color="#feed6c" />
          </linearGradient>
        '''
        )
        config.defs.append(
            '''
          <linearGradient id="gradient-1" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stop-color="#b6e354" />
            <stop offset="100%" stop-color="#8cedff" />
          </linearGradient>
        '''
        )
        config.css.append(
            '''inline:
          .color-0 {
            fill: url(#gradient-0) !important;
            stroke: url(#gradient-0) !important;
          }'''
        )
        config.css.append(
            '''inline:
          .color-1 {
            fill: url(#gradient-1) !important;
            stroke: url(#gradient-1) !important;
          }'''
        )
        chart = CHARTS_BY_NAME[chart](config)
        chart.add('1', [1, 3, 12, 3, 4, None, 9])
        chart.add('2', [7, -4, 10, None, 8, 3, 1])
        chart.x_labels = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        chart.legend_at_bottom = True
        chart.interpolate = 'cubic'
        return chart.render_response()

    @app.route('/test/erfinv/approx')
    def test_erfinv():
        from scipy import stats as sstats
        chart = Line(show_dots=False)
        chart.add('scipy', [sstats.norm.ppf(x / 1000) for x in range(1, 999)])
        chart.add('approx', [stats.ppf(x / 1000) for x in range(1, 999)])

        # chart.add('approx', [
        #    special.erfinv(x/1000) - erfinv(x/1000)
        #    for x in range(-999, 1000)])
        return chart.render_response()

    @app.route('/test/ci/<chart>')
    def test_ci_for(chart):
        chart = CHARTS_BY_NAME[chart](
            style=styles['default'](
                value_font_family='googlefont:Raleway',
                value_colors=(None, None, 'blue', 'red', 'green'),
                ci_colors=(None, 'magenta')
            )
        )
        chart.add(
            'Series 1', [
                {
                    'value': 127.3,
                    'ci': {
                        'type': 'continuous',
                        'sample_size': 3534,
                        'stddev': 19,
                        'confidence': .99
                    }
                },
                {
                    'value': 127.3,
                    'ci': {
                        'type': 'continuous',
                        'sample_size': 3534,
                        'stddev': 19
                    }
                },
                {
                    'value': 127.3,
                    'ci': {
                        'type': 'continuous',
                        'sample_size': 3534,
                        'stddev': 19,
                        'confidence': .90
                    }
                },
                {
                    'value': 127.3,
                    'ci': {
                        'type': 'continuous',
                        'sample_size': 3534,
                        'stddev': 19,
                        'confidence': .75
                    }
                },
            ]
        )
        chart.add(
            'Series 2', [
                {
                    'value': 34.5,
                    'ci': {
                        'type': 'dichotomous',
                        'sample_size': 3532
                    }
                },
            ]
        )
        chart.add(
            'Series 3', [
                {
                    'value': 100,
                    'ci': {
                        'low': 50,
                        'high': 150
                    }
                },
                {
                    'value': 100,
                    'ci': {
                        'low': 75,
                        'high': 175
                    }
                },
                {
                    'value': 50,
                    'ci': {
                        'low': 50,
                        'high': 100
                    }
                },
                {
                    'value': 125,
                    'ci': {
                        'low': 120,
                        'high': 130
                    }
                },
            ]
        )
        chart.range = (30, 200)
        return chart.render_response()

    @app.route('/test/interruptions')
    def test_interruptions():
        chart = Line(allow_interruptions=True)
        chart.add(
            'interrupt', [22, 34, 43, 12, None, 12, 55, None, 56],
            allow_interruptions=False
        )
        chart.add(
            'not interrupt', [
                -a if a else None
                for a in (22, 34, 43, 12, None, 12, 55, None, 56)
            ]
        )
        return chart.render_response()

    return list(
        sorted(
            filter(
                lambda x: x.startswith('test') and not x.endswith('_for'),
                locals()
            )
        )
    ) + list(
        sorted(
            filter(
                lambda x: x.startswith('test') and x.endswith('_for'), locals()
            )
        )
    )
