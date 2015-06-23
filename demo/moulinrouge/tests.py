# -*- coding: utf-8 -*-
# This file is part of pygal
from pygal import (
    Bar, Gauge, Pyramid, Funnel, Dot, StackedBar, StackedLine, XY,
    CHARTS_BY_NAME, Config, Line, Worldmap, Histogram, Box, SwissMapCantons,
    FrenchMapDepartments, FrenchMapRegions, Pie, Treemap, TimeLine, DateLine,
    DateTimeLine, SupranationalWorldmap)


from pygal.style import styles, Style, RotateStyle
from pygal.colors import rotate
from pygal.graph.frenchmap import DEPARTMENTS, REGIONS
from pygal.graph.swissmap import CANTONS
from random import randint, choice
from datetime import datetime


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
        bar.js = ('http://l:2343/svg.jquery.js',
                  'http://l:2343/pygal-tooltips.js')
        bar.add('1234', [
            {'value': 10,
             'label': 'Ten',
             'xlink': 'http://google.com?q=10'},
            {'value': 20,
             'tooltip': 'Twenty',
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

    @app.route('/test/xy_links')
    def test_xy_links():
        xy = XY(style=styles['neon'], interpolate='cubic')
        xy.add('1234', [
            {'value': (10, 5),
             'label': 'Ten',
             'xlink': 'http://google.com?q=10'},
            {'value': (20, 20),
             'tooltip': 'Twenty',
             'xlink': 'http://google.com?q=20'},
            (30, 15),
            {'value': (40, -5),
             'label': 'Forty',
             'xlink': 'http://google.com?q=40'}
        ])

        xy.add('4321', [(40, 10), {
            'value': (30, 3),
            'label': 'Thirty',
            'xlink': 'http://google.com?q=30'
        }, (20, 10), (10, 21)])
        xy.x_labels = map(str, range(1, 5))
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
            '1 12 123 1234 12345 123456 1234567 12345678 123456789 1234567890')
        return bar.render_response()

    @app.route('/test/multiline_title')
    def test_multiline_title():
        bar = Bar()
        bar.add('Looooooooooooooooooooooooooooooooooong', [2, None, 12])
        bar.title = (
            'First line \n Second line \n Third line'
        )
        return bar.render_response()

    @app.route('/test/long_labels')
    def test_long_labels():
        bar = Bar()
        bar.add('Long', [2, None, 12])
        bar.title = (
            '1 12 123 1234 12345 123456 1234567 12345678 123456789 1234567890')
        bar.x_labels = 'a' * 100, 'b ' * 50, 'cc ! ' * 20
        bar.x_label_rotation = 45
        return bar.render_response()

    @app.route('/test/none')
    def test_bar_none():
        bar = Bar()
        bar.add('Lol', [2, None, 12])
        return bar.render_response()

    @app.route('/test/treemap')
    def test_treemap():
        treemap = Treemap(style=RotateStyle('#ff5995', opacity=.6))
        treemap.title = 'Binary TreeMap'
        treemap.add('A', [2, 1, 12, 4, 2, 1, 1, 3, 12, 3, 4, None, 9])
        treemap.add('B', [4, 2, 5, 10, 3, 4, 2, 7, 4, -10, None, 8, 3, 1])
        treemap.add('C', [3, 8, 3, 3, 5, 3, 3, 5, 4, 12])
        treemap.add('D', [23, 18])
        treemap.add('E', [1, 2, 1, 2, 3, 3, 1, 2, 3,
                          4, 3, 1, 2, 1, 1, 1, 1, 1])
        treemap.add('F', [31])
        treemap.add('G', [5, 9.3, 8.1, 12, 4, 3, 2])
        treemap.add('H', [12, 3, 3])
        return treemap.render_response()

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

    @app.route('/test/<chart>')
    def test_for(chart):
        graph = CHARTS_BY_NAME[chart]()
        graph.add('1', [1, 3, 12, 3, 4, None, 9])
        graph.add('2', [7, -4, 10, None, 8, 3, 1])
        graph.add('3', [7, -14, -10, None, 8, 3, 1])
        graph.add('4', [7, 4, -10, None, 8, 3, 1])
        graph.x_labels = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
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
        graph.x_labels = (
            'First point', 'Second point', 'Third point')
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
        graph = CHARTS_BY_NAME[chart](interpolate='lagrange',
                                      interpolation_parameters={
                                          'type': 'kochanek_bartels',
                                          'c': 1,
                                          'b': -1,
                                          't': -1})
        graph.add('1', [1, 3, 12, 3, 4])
        graph.add('2', [7, -4, 10, None, 8, 3, 1])
        return graph.render_response()

    @app.route('/test/logarithmic/<chart>')
    def test_logarithmic_for(chart):
        graph = CHARTS_BY_NAME[chart](logarithmic=True)
        if isinstance(graph, CHARTS_BY_NAME['XY']):
            graph.add('xy', [
                (.1, .234), (10, 243), (.001, 2), (1000000, 1231)])
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
        bar = Bar()
        bar.add('1', [1, 2, 3])
        bar.add('2', [4, 5, 6])
        bar.x_labels = ['a']
        return bar.render_response()

    @app.route('/test/histogram')
    def test_histogram():
        hist = Histogram(style=styles['neon'])
        hist.add('1', [
            (2, 0, 1),
            (4, 1, 3),
            (3, 3.5, 5),
            (1.5, 5, 10)
        ])
        hist.add('2', [(2, 2, 8)])
        return hist.render_response()

    @app.route('/test/ylabels')
    def test_ylabels():
        chart = Line()
        chart.x_labels = 'Red', 'Blue', 'Green'
        chart.y_labels = .0001, .0003, .0004, .00045, .0005
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
        chart.add(10 * '1b', [-4, 50, 6], secondary=True)
        chart.add(10 * '2b', [None, 10, 20], secondary=True)
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
        return chart.render_response()

    @app.route('/test/box')
    def test_box():
        chart = Box()
        chart.add('One', [15, 8, 2, -12, 9, 23])
        chart.add('Two', [5, 8, 2, -9, 23, 12])
        chart.add('Three', [8, -2, 12, -5, 9, 3])
        chart.add('Four', [5, 8, 2, -9, -3, 12])
        chart.add('Five', [8, 12, 12, -9, 5, 13])
        chart.x_labels = map(str, range(5))
        return chart.render_response()

    @app.route('/test/stacked')
    def test_stacked():
        stacked = StackedBar()
        stacked.add('1', [1, 2, 3])
        stacked.add('2', [4, 5, 6])
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
            js = ['http://l:2343/svg.jquery.js',
                  'http://l:2343/pygal-tooltips.js']

        stacked = StackedBar(LolConfig())
        stacked.add('1', [1, 2, 3])
        stacked.add('2', [4, 5, 6])
        return stacked.render_response()

    @app.route('/test/dateline')
    def test_dateline():
        datey = DateLine(show_dots=False)
        datey.add('1', [
            (datetime(2013, 1, 2), 300),
            (datetime(2013, 1, 12), 412),
            (datetime(2013, 2, 2), 823),
            (datetime(2013, 2, 22), 672)
        ])
        datey.x_label_rotation = 25
        return datey.render_response()

    @app.route('/test/timeline')
    def test_timexy():
        from datetime import time
        datey = TimeLine()
        datey.add('1', [
            (time(1, 12, 29), 2),
            (time(21, 2, 29), 10),
            (time(12, 30, 59), 7)
        ])
        datey.add(
            '2', [(time(12, 12, 12), 4), (time(), 8), (time(23, 59, 59), 6)])
        datey.x_label_rotation = 25
        return datey.render_response()

    @app.route('/test/worldmap')
    def test_worldmap():
        wmap = Worldmap(style=choice(list(styles.values())))

        wmap.add('1st', [('fr', 100), ('us', 10)])
        wmap.add('2nd', [('jp', 1), ('ru', 7), ('uk', 0)])
        wmap.add('3rd', ['ch', 'cz', 'ca', 'cn'])
        wmap.add('4th', {'br': 12, 'bo': 1, 'bu': 23, 'fr': 34})
        wmap.add('5th', [{
            'value': ('tw', 10),
            'label': 'First label',
            'xlink': 'http://google.com?q=tw'
        }, {
            'value': ('bw', 20),
            'label': 'Second one',
            'xlink': 'http://google.com?q=bw'
        }, {
            'value': ('mw', 40),
            'label': 'Last'
        }])
        wmap.add('6th', [3, 5, 34, 12])
        wmap.title = 'World Map !!'
        return wmap.render_response()

    @app.route('/test/supranational')
    def test_supranational():
        wmap = SupranationalWorldmap(style=choice(list(styles.values())))

        wmap.add('Asia', [('asia', 1)])
        wmap.add('Europe', [('europe', 1)])
        wmap.add('Africa', [('africa', 1)])
        wmap.add('North america', [('north_america', 1)])
        wmap.add('South america', [('south_america', 1)])
        wmap.add('Oceania', [('oceania', 1)])
        wmap.add('Antartica', [('antartica', 1)])

        wmap.title = 'Supra World Map !!'
        return wmap.render_response()

    @app.route('/test/frenchmapdepartments')
    def test_frenchmapdepartments():
        fmap = FrenchMapDepartments(style=choice(list(styles.values())))
        for i in range(10):
            fmap.add('s%d' % i, [
                (choice(list(DEPARTMENTS.keys())), randint(0, 100))
                for _ in range(randint(1, 5))])

        fmap.add('links', [{
            'value': (69, 10),
            'label': '\o/',
            'xlink': 'http://google.com?q=69'
        }, {
            'value': ('42', 20),
            'label': 'Y',
        }])
        fmap.add('6th', [3, 5, 34, 12])
        fmap.title = 'French map'
        return fmap.render_response()

    @app.route('/test/swissmap')
    def test_swissmap():
        smap = SwissMapCantons(style=choice(list(styles.values())))
        for i in range(10):
            smap.add('s%d' % i, [
                (choice(list(CANTONS.keys())), randint(0, 100))
                for _ in range(randint(1, 5))])

        smap.add('links', [{
            'value': ('kt-vs', 10),
            'label': '\o/',
            'xlink': 'http://google.com?q=69'
        }, {
            'value': ('bt', 20),
            'label': 'Y',
        }])
        smap.add('6th', [3, 5, 34, 12])
        smap.title = 'Swiss map'
        return smap.render_response()

    @app.route('/test/frenchmapregions')
    def test_frenchmapregions():
        fmap = FrenchMapRegions(style=choice(list(styles.values())))
        for i in range(10):
            fmap.add('s%d' % i, [
                (choice(list(REGIONS.keys())), randint(0, 100))
                for _ in range(randint(1, 5))])

        fmap.add('links', [{
            'value': ('02', 10),
            'label': '\o/',
            'xlink': 'http://google.com?q=69'
        }, {
            'value': ('72', 20),
            'label': 'Y',
        }])
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
        colors = [rotate('#ff0000', i * 360 / 64) for i in range(64)]
        pie = Pie(style=Style(colors=colors))
        for i in range(64):
            pie.add(str(i), 1)
        return pie.render_response()

    @app.route('/test/major_dots')
    def test_major_dots():
        line = Line(x_labels_major_count=2, show_only_major_dots=True)
        line.add('test', range(12))
        line.x_labels = [
            'lol', 'lol1', 'lol2', 'lol3', 'lol4', 'lol5',
            'lol6', 'lol7', 'lol8', 'lol9', 'lol10', 'lol11']
        # line.x_labels_major = ['lol3']
        return line.render_response()

    @app.route('/test/x_major_labels/<chart>')
    def test_x_major_labels_for(chart):
        chart = CHARTS_BY_NAME[chart]()
        chart.add('test', range(12))
        chart.x_labels = map(str, range(12))
        chart.x_labels_major_count = 4
        # chart.x_labels_major = ['1', '5', '11', '1.0', '5.0', '11.0']
        return chart.render_response()

    @app.route('/test/y_major_labels/<chart>')
    def test_y_major_labels_for(chart):
        chart = CHARTS_BY_NAME[chart]()
        chart.add('test', zip(*[range(12), range(12)]))
        chart.y_labels = range(12)
        # chart.y_labels_major_count = 4
        chart.y_labels_major = [1.0, 5.0, 11.0]
        return chart.render_response()

    @app.route('/test/stroke_config')
    def test_stroke_config():
        line = Line()
        line.add('test_no_line', range(12), stroke=False)
        line.add('test', reversed(range(12)))
        line.add('test_no_dots', [5] * 12, show_dots=False)
        line.add('test_big_dots', [
            randint(1, 12) for _ in range(12)], dots_size=5)
        line.add('test_fill', [
            randint(1, 3) for _ in range(12)], fill=True)

        line.x_labels = [
            'lol', 'lol1', 'lol2', 'lol3', 'lol4', 'lol5',
            'lol6', 'lol7', 'lol8', 'lol9', 'lol10', 'lol11']
        return line.render_response()

    @app.route('/test/pie_serie_radius')
    def test_pie_serie_radius():
        pie = Pie()
        for i in range(10):
            pie.add(str(i), i, inner_radius=(10 - i) / 10)

        return pie.render_response()

    @app.route('/test/half_pie')
    def test_half_pie():
        pie = Pie(half_pie=True)
        for i in range(100):
            pie.add(str(i), i, inner_radius=.1)
        pie.legend_at_bottom = True
        pie.legend_at_bottom_columns = 4
        return pie.render_response()

    @app.route('/test/interpolate/secondary')
    def test_interpolate_secondary():
        chart = Line(title=u'Some different points', interpolate='cubic')
        chart.add('line', [1000, 2000, 7000])
        chart.add('other line', [100, 500, 500], secondary=True)
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
        c.add('1', [
            {'style': 'fill: red', 'value': 1},
            {'color': 'blue', 'value': 2},
            {'style': 'fill: red; stroke: yellow', 'value': 3}])
        c.add('2', [
            {'value': 4},
            {'color': 'green', 'value': 5},
            6])
        return c.render_response()

    @app.route('/test/sparkline/<chart>')
    def test_sparkline_for(chart):
        graph = CHARTS_BY_NAME[chart](**dict(
            width=200,
            height=50,
            show_dots=False,
            show_legend=False,
            show_y_labels=False,
            show_x_labels=False,
            spacing=0,
            margin=5,
            explicit_size=True
        ))
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

    @app.route('/test/datetimeline')
    def test_datetimeline():
        line = DateTimeLine()
        line.add('dt', [
            (datetime(2013, 1, 12, 8, 0), 300),
            (datetime(2013, 1, 12, 12), 412),
            (datetime(2013, 2, 22, 12), 823),
            (datetime(2013, 2, 22, 20), 672)
        ])
        line.x_value_formatter = lambda x: x.strftime("%Y-%m-%d")
        line.x_label_rotation = 45
        return line.render_response()

    return list(sorted(filter(lambda x: x.startswith('test'), locals())))
