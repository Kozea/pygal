from pygal.base import BaseGraph


class Line(BaseGraph):
    """Line graph"""

    def _draw(self):
        vals = [val for serie in self.series for val in serie.values]
        ymin, ymax = min(vals), max(vals)
        x_step = len(self.series[0].values)
        x_pos = [x / float(x_step - 1) for x in range(x_step)
        ] if x_step != 1 else [.5]  # Center if only one value
        y_pos = self._pos(
            ymin, ymax, self.y_scale) if not self.y_labels else map(
            int, self.y_labels)

        x_labels = self.x_labels and zip(self.x_labels, x_pos)
        y_labels = zip(map(str, y_pos), y_pos)

        self._compute_margin(x_labels, y_labels)
        self.svg.set_view(ymin, ymax)
        self.svg.make_graph()
        self.svg.x_axis(x_labels)
        self.svg.y_axis(y_labels)
        self.svg.legend([serie.title for serie in self.series])
        self.svg.title()

        for serie in self.series:
            self.svg.line(
                self.svg.serie(serie.index), [
                (x_pos[i], v)
                for i, v in enumerate(serie.values)])
