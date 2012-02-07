from pygal import Serie, Margin, Label
from pygal.svg import Svg
from pygal.util import round_to_int, round_to_float
from pygal.base import BaseGraph


class Line(BaseGraph):
    """Line graph"""

    def __init__(self, width, height, scale=1, style=None):
        self.width = width
        self.height = height
        self.svg = Svg(width, height, style=style)
        self.label_font_size = 12
        self.series = []
        self.scale = scale
        self.x_labels = self.y_labels = self.title = None
        rnd = round_to_float if self.scale < 1 else round_to_int
        self.round = lambda x: rnd(x, self.scale)

    def add(self, title, values):
        self.series.append(Serie(title, values))

    def _label(self, number):
        return Label(*self.round(number))

    def _y_labels(self, ymin, ymax):
        step = (ymax - ymin) / 20.

        if not step:
            return [self._label(ymin)]
        label = ymin
        labels = set()
        while label < (ymax + step):
            labels.add(self._label(label))
            label += step
        return labels

    def validate(self):
        if self.x_labels:
            assert len(self.series[0].values) == len(self.x_labels)
        for serie in self.series:
            assert len(self.series[0].values) == len(serie.values)

    def draw(self):
        vals = [val for serie in self.series for val in serie.values]
        if not vals:
            return
        self.validate()
        x_step = len(self.series[0].values)
        x_pos = [x / float(x_step - 1) for x in range(x_step)
        ] if x_step != 1 else [.5]  # Center if only one value
        margin = Margin(*(4 * [10]))
        ymin, ymax = min(vals), max(vals)
        if self.x_labels:
            x_labels = [Label(label, x_pos[i])
                         for i, label in enumerate(self.x_labels)]
        y_labels = self.y_labels or self._y_labels(ymin, ymax)
        series_labels = [serie.title for serie in self.series]
        margin.left += 10 + max(
            map(len, [l.label for l in y_labels])) * 0.6 * self.label_font_size
        if self.x_labels:
            margin.bottom += 10 + self.label_font_size
        margin.right += 20 + max(
            map(len, series_labels)) * 0.6 * self.label_font_size
        margin.top += 10 + self.label_font_size

        # Actual drawing
        self.svg.set_view(margin, ymin, ymax)
        self.svg.graph(margin)
        if self.x_labels:
            self.svg.x_axis(x_labels)
        self.svg.y_axis(y_labels)
        self.svg.legend(margin, series_labels)
        self.svg.title(margin, self.title)
        for serie_index, serie in enumerate(self.series):
            serie_node = self.svg.serie(serie_index)
            self.svg.line(serie_node, [
                (x_pos[i], v)
                for i, v in enumerate(serie.values)])
