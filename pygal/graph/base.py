from pygal.serie import Serie
from pygal.view import Margin, Box
from pygal.util import round_to_scale, cut, rad
from pygal.svg import Svg
from pygal.config import Config
from pygal.util import cached_property
from math import log10, sin, cos


class BaseGraph(object):
    """Graphs commons"""

    def __init__(self, config=None, **kwargs):
        self.config = config or Config()
        self.config(**kwargs)
        self.svg = Svg(self)
        self.series = []
        self.margin = Margin(*([20] * 4))
        self._x_labels = self._y_labels = None
        self._box = Box()

    def __getattr__(self, attr):
        if attr in dir(self.config):
            return object.__getattribute__(self.config, attr)
        return object.__getattribute__(self, attr)

    def _pos(self, min_, max_, scale, min_scale=4, max_scale=20):
        if min_ == 0 and max_ == 0:
            return [0]
        order = round(log10(max(abs(min_), abs(max_)))) - 1
        while (max_ - min_) / float(10 ** order) < min_scale:
            order -= 1
        step = float(10 ** order)
        while (max_ - min_) / step > max_scale:
            step *= 2.
        positions = set()
        position = round_to_scale(min_, step)
        while position < (max_ + step):
            rounded = round_to_scale(position, scale)
            if min_ <= rounded <= max_:
                positions.add(rounded)
            position += step
        if len(positions) < 2:
            return [min_, max_]
        return positions

    def _text_len(self, lenght, fs):
        return lenght * 0.6 * fs

    def _get_text_box(self, text, fs):
        return (fs, self._text_len(len(text), fs))

    def _get_texts_box(self, texts, fs):
        max_len = max(map(len, texts))
        return (fs, self._text_len(max_len, fs))

    def _compute(self):
        """Initial computations to draw the graph"""

    def _compute_margin(self):
        if self.show_legend:
            h, w = self._get_texts_box(
                cut(self.series, 'title'), self.legend_font_size)
            self.margin.right += 10 + w + self.legend_box_size

        if self.title:
            h, w = self._get_text_box(self.title, self.title_font_size)
            self.margin.top += 10 + h

        if self._x_labels:
            h, w = self._get_texts_box(
                cut(self._x_labels), self.label_font_size)
            self.margin.bottom += 10 + max(
                w * sin(rad(self.x_label_rotation)), h)
            if self.x_label_rotation:
                self.margin.right = max(
                    .5 * w * cos(rad(self.x_label_rotation)),
                    self.margin.right)
        if self._y_labels:
            h, w = self._get_texts_box(
                cut(self._y_labels), self.label_font_size)
            self.margin.left += 10 + max(
                w * cos(rad(self.y_label_rotation)), h)

    @cached_property
    def _legends(self):
        return [serie.title for serie in self.series]

    @cached_property
    def _values(self):
        return [val for serie in self.series for val in serie.values]

    @cached_property
    def _len(self):
        return len(self.series[0].values)

    def _draw(self):
        self._compute()
        self._compute_margin()
        self._decorate()
        self._plot()

    def add(self, title, values):
        self.series.append(Serie(title, values, len(self.series)))

    def render(self):
        if len(self.series) == 0:
            return
        for serie in self.series:
            if not hasattr(serie.values, '__iter__'):
                serie.values = [serie.values]
        if sum(map(len, map(lambda s: s.values, self.series))) == 0:
            return
        self.validate()
        self._draw()
        return self.svg.render()

    def validate(self):
        if self.x_labels:
            assert len(self.series[0].values) == len(self.x_labels)
        for serie in self.series:
            assert len(self.series[0].values) == len(serie.values)

    def _in_browser(self):
        from lxml.html import open_in_browser
        self._draw()
        open_in_browser(self.svg.root, encoding='utf-8')

    def render_response(self):
        from flask import Response
        return Response(self.render(), mimetype='image/svg+xml')
