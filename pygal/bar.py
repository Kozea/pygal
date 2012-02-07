from pygal import Margin, Label
from pygal.base import BaseGraph


class Bar(BaseGraph):
    """Bar graph"""

    def _draw(self):
        ymin, ymax = 0, max([
            val for serie in self.series for val in serie.values])
        x_step = len(self.series[0].values)
        x_pos = [x / float(x_step) for x in range(x_step + 1)
        ] if x_step > 1 else [0, 1]  # Center if only one value
        y_pos = self._y_pos(ymin, ymax) if not self.y_labels else map(
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

        for serie_index, serie in enumerate(self.series):
            serie_node = self.svg.serie(serie_index)
            self.svg.bar(serie_node, [
                tuple((x_ranges[i][j], v) for j in range(2))
                for i, v in enumerate(serie.values)])
