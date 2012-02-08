from pygal.serie import Serie
from pygal.base import BaseGraph
from math import pi


class Pie(BaseGraph):
    """Pie graph"""

    def add(self, title, value):
        self.series.append(Serie(title, [value], len(self.series)))

    def _draw(self):
        self._compute_margin()
        self.svg.set_view()
        self.svg.make_graph()
        self.svg.legend([serie.title for serie in self.series])
        self.svg.title()
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
