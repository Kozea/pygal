from pygal import Serie, Margin, Label
from pygal.svg import Svg
from pygal.base import BaseGraph


class Line(BaseGraph):
    """Line graph"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.svg = Svg(width, height)
        self.label_font_size = 12
        self.series = []
        self.x_labels = None

    def add(self, title, values):
        self.series.append(
            Serie(title, values))

    def set_labels(self, labels):
        values = float(len(labels) - 1)
        self.x_labels = [Label(label, i / values)
                         for i, label in enumerate(labels)]

    def y_labels(self, ymin, ymax):
        step = (ymax - ymin) / 20.
        label = ymin
        labels = []
        while label < ymax:
            labels.append(Label(str(label), label))
            label += step
        return labels

    def validate(self):
        assert len(self.series)
        if self.x_labels:
            assert len(self.series[0].values) == len(self.x_labels)
        for serie in self.series:
            assert len(self.series[0].values) == len(serie.values)

    def draw(self):
        self.validate()

        vals = [val for serie in self.series for val in serie.values]
        margin = Margin(*(4 * [20]))
        ymin, ymax = min(vals), max(vals)
        x_labels = self.x_labels
        y_labels = self.y_labels(ymin, ymax)
        margin.left += 10 + max(
            map(len, [l.label for l in y_labels])) * 0.6 * self.label_font_size
        margin.bottom += 10 + self.label_font_size

        # Actual drawing

        self.svg.set_view(margin, ymin, ymax)
        self.svg.graph(margin)
        self.svg.x_axis(x_labels)
        self.svg.y_axis(y_labels)
        for serie_index, serie in enumerate(self.series):
            serie_node = self.svg.serie(serie_index)
            self.svg.line(serie_node, [
                (x_labels[i].pos, v)
                for i, v in enumerate(serie.values)])
