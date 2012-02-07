from pygal import Serie, Label, Margin
from pygal.util import round_to_scale
from pygal.svg import Svg
from pygal.config import Config


class BaseGraph(object):
    """Graphs commons"""

    def __init__(self, config=None):
        self.config = config or Config()
        self.svg = Svg(self)
        self.series = []
        self.margin = Margin(*([10] * 4))

    def __getattr__(self, attr):
        if attr in dir(self.config):
            return object.__getattribute__(self.config, attr)
        return object.__getattribute__(self, attr)

    def _y_pos(self, ymin, ymax):
        step = (ymax - ymin) / float(self.max_scale_step)
        position = ymin
        if not step:
            return [position]
        positions = set()
        while position < (ymax + step):
            positions.add(round_to_scale(position, self.scale))
            position += step
        return positions

    def _compute_margin(self, x_labels, y_labels):
        self.margin.left += 10 + max(
            map(len, [l for l, _ in y_labels])
        ) * 0.6 * self.label_font_size
        if x_labels:
            self.margin.bottom += 10 + self.label_font_size
        self.margin.right += 20 + max(
            map(len, [serie.title for serie in self.series])
        ) * 0.6 * self.label_font_size
        self.margin.top += 10 + self.label_font_size

    def add(self, title, values):
        self.series.append(Serie(title, values, len(self.series)))

    def render(self):
        if len(self.series) == 0 or sum(
                map(len, map(lambda s: s.values, self.series))) == 0:
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
