from pygal.serie import Serie
from pygal.base import BaseGraph
from math import pi


class Pie(BaseGraph):
    """Pie graph"""

    def add(self, title, value):
        self.series.append(Serie(title, [value], len(self.series)))

    def _plot(self):
        total = float(sum(serie.values[0] for serie in self.series))
        current_angle = 0
        for serie in self.series:
            val = serie.values[0]
            angle = 2 * pi * val / total
            self.svg.slice(
                self.svg.serie(serie.index),
                current_angle,
                angle, val / total)
            current_angle += angle
