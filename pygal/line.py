from pygal import Serie
from pygal.svg import Svg
from pygal.base import BaseGraph


class Line(BaseGraph):
    """Line graph"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.svg = Svg(width, height)
        self.series = []

    def add(self, title, values):
        self.series.append(
            Serie(title, values))

    def draw(self):
        min_value = min((val
                         for serie in self.series
                         for val in serie.values))
        max_value = max((val
                         for serie in self.series
                         for val in serie.values))
        self.svg.graph(min_value, max_value)
        for serie in self.series:
            n_values = len(serie.values) - 1
            x_spacing = self.width / n_values
            self.svg.line([
                (i * x_spacing, v)
                for i, v in enumerate(serie.values)])
