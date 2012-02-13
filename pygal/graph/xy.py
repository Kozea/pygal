from pygal.graph.base import BaseGraph


class XY(BaseGraph):
    """XY Line graph"""

    def _compute(self):
        for serie in self.series:
            serie.values = sorted(serie.values, key=lambda x: x[0])
        xvals = [val[0] for serie in self.series for val in serie.values]
        yvals = [val[1] for serie in self.series for val in serie.values]
        self._box.xmin, self._box.xmax = min(xvals), max(xvals)
        self._box.ymin, self._box.ymax = min(yvals), max(yvals)

        x_pos = self._pos(self._box.xmin, self._box.xmax, self.x_scale)
        y_pos = self._pos(self._box.ymin, self._box.ymax, self.y_scale)

        self._x_labels = zip(map(str, x_pos), x_pos)
        self._y_labels = zip(map(str, y_pos), y_pos)

    def _plot(self):
        for serie in self.series:
            self.svg.line(
                self.svg.serie(serie.index), serie.values, True)
