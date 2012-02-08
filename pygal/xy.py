from pygal.base import BaseGraph


class XY(BaseGraph):
    """XY Line graph"""

    def _draw(self):
        for serie in self.series:
            serie.values = sorted(serie.values, key=lambda x: x[0])
        xvals = [val[0] for serie in self.series for val in serie.values]
        yvals = [val[1] for serie in self.series for val in serie.values]
        xmin, xmax = min(xvals), max(xvals)
        ymin, ymax = min(yvals), max(yvals)

        x_pos = self._pos(xmin, xmax, self.x_scale)
        y_pos = self._pos(ymin, ymax, self.y_scale)

        x_labels = zip(map(str, x_pos), x_pos)
        y_labels = zip(map(str, y_pos), y_pos)

        self._compute_margin(x_labels, y_labels)
        self.svg.set_view(ymin, ymax, xmin, xmax)
        self.svg.make_graph()
        self.svg.x_axis(x_labels)
        self.svg.y_axis(y_labels)
        self.svg.legend([serie.title for serie in self.series])
        self.svg.title()

        for serie in self.series:
            self.svg.line(
                self.svg.serie(serie.index), serie.values)
