from pygal.graph.base import BaseGraph
from math import pi


class Radar(BaseGraph):
    """Kiviat graph"""

    def _compute(self):
        vals = [val for serie in self.series for val in serie.values]
        self._box.ymax = 2 * max(vals)
        self._box.ymin = - self._box.ymax
        self._box.xmin = self._box.ymin
        self._box.xmax = self._box.ymax

        delta = 2 * pi / float(len(self.x_labels))
        x_step = len(self.series[0].values)
        self._x_pos = [.5 * pi - i * delta for i in range(x_step)]
        self._y_pos = self._pos(self._box.ymin, self._box.ymax, self.y_scale
        ) if not self.y_labels else map(int, self.y_labels)
        self._x_labels = self.x_labels and zip(self.x_labels, self._x_pos)
        self._y_labels = zip(map(str, self._y_pos), self._y_pos)

    def _plot(self):
        for serie in self.series:
            serie_node = self.svg.serie(serie.index)
            # self.svg.web(serie_node, serie,
                         # [val / float(self._rmax) for val in serie.values])
