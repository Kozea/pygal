from pygal.base import BaseGraph


class Line(BaseGraph):
    """Line graph"""

    def _compute(self):
        vals = [val for serie in self.series for val in serie.values]
        self._box.ymin, self._box.ymax = min(vals), max(vals)
        x_step = len(self.series[0].values)
        self._x_pos = [x / float(x_step - 1) for x in range(x_step)
        ] if x_step != 1 else [.5]  # Center if only one value
        self._y_pos = self._pos(self._box.ymin, self._box.ymax, self.y_scale
        ) if not self.y_labels else map(int, self.y_labels)

        self._x_labels = self.x_labels and zip(self.x_labels, self._x_pos)
        self._y_labels = zip(map(str, self._y_pos), self._y_pos)

    def _plot(self):
        for serie in self.series:
            self.svg.line(
                self.svg.serie(serie.index), [
                (self._x_pos[i], v)
                for i, v in enumerate(serie.values)])
