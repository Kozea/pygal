from pygal.base import BaseGraph


class StackedBar(BaseGraph):
    """Stacked Bar graph"""

    def _compute(self):
        transposed = zip(*[serie.values for serie in self.series])
        positive_vals = [sum([val if val > 0 else 0 for val in vals])
                           for vals in transposed]
        negative_vals = [sum([val if val < 0 else 0 for val in vals])
                           for vals in transposed]

        self._box.ymin, self._box.ymax = (
            min(min(negative_vals), 0), max(max(positive_vals), 0))
        self._length = len(self.series[0].values)

        x_pos = [x / float(self._length)
                 for x in range(self._length + 1)
             ] if self._length > 1 else [0, 1]  # Center if only one value
        y_pos = self._pos(self._box.ymin, self._box.ymax, self.y_scale
        ) if not self.y_labels else map(int, self.y_labels)
        self._x_ranges = zip(x_pos, x_pos[1:])

        self._x_labels = self.x_labels and zip(self.x_labels, [
            sum(x_range) / 2 for x_range in self._x_ranges])
        self._y_labels = zip(map(str, y_pos), y_pos)

    def _plot(self):
        stack_vals = [[0, 0] for i in range(self._length)]
        for serie in self.series:
            serie_node = self.svg.serie(serie.index)
            stack_vals = self.svg.bar(
                serie_node, serie, [
                tuple((self._x_ranges[i][j], v) for j in range(2))
                for i, v in enumerate(serie.values)],
                stack_vals)
