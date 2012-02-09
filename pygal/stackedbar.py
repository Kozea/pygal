from pygal.base import BaseGraph


class StackedBar(BaseGraph):
    """Stacked Bar graph"""

    def _draw(self):
        transposed = zip(*[serie.values for serie in self.series])
        positive_vals = [sum([val if val > 0 else 0 for val in vals])
                           for vals in transposed]
        negative_vals = [sum([val if val < 0 else 0 for val in vals])
                           for vals in transposed]
        ymin, ymax = min(min(negative_vals), 0), max(max(positive_vals), 0)
        length = len(self.series[0].values)
        x_pos = [x / float(length) for x in range(length + 1)
        ] if length > 1 else [0, 1]  # Center if only one value
        y_pos = self._pos(
            ymin, ymax, self.y_scale) if not self.y_labels else map(
            int, self.y_labels)
        x_ranges = zip(x_pos, x_pos[1:])

        x_labels = self.x_labels and zip(self.x_labels, [
            sum(x_range) / 2 for x_range in x_ranges])
        y_labels = zip(map(str, y_pos), y_pos)

        self._compute_margin(x_labels, y_labels)
        self.svg.set_view(ymin, ymax)
        self.svg.make_graph()
        self.svg.x_axis(x_labels)
        self.svg.y_axis(y_labels)
        self.svg.legend([serie.title for serie in self.series])
        self.svg.title()

        stack_vals = [[0, 0] for i in range(length)]
        for serie in self.series:
            serie_node = self.svg.serie(serie.index)
            stack_vals = self.svg.stackbar(
                serie_node, serie, [
                tuple((x_ranges[i][j], v) for j in range(2))
                for i, v in enumerate(serie.values)],
                stack_vals)
