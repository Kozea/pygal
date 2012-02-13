from pygal.graph.base import BaseGraph


class Bar(BaseGraph):
    """Bar graph"""

    def _compute(self):
        vals = [val for serie in self.series for val in serie.values]
        self._box.ymin, self._box.ymax = min(min(vals), 0), max(max(vals), 0)
        x_step = len(self.series[0].values)
        x_pos = [x / float(x_step) for x in range(x_step + 1)
        ] if x_step > 1 else [0, 1]  # Center if only one value
        y_pos = self._pos(self._box.ymin, self._box.ymax, self.y_scale
        ) if not self.y_labels else map(int, self.y_labels)

        self._x_ranges = zip(x_pos, x_pos[1:])
        self._x_labels = self.x_labels and zip(self.x_labels, [
            sum(x_range) / 2. for x_range in self._x_ranges])
        self._y_labels = zip(map(str, y_pos), y_pos)

    def _plot(self):
        for serie in self.series:
            serie_node = self.svg.serie(serie.index)
            self.svg.bar(serie_node, serie, [
                tuple((self._x_ranges[i][j], v) for j in range(2))
                for i, v in enumerate(serie.values)])
