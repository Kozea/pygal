from pygal.graph.graph import Graph


class Line(Graph):
    """Line graph"""

    def _get_value(self, values, i):
        return str(values[i][1])

    def line(self, serie_node, values):
        view_values = map(self.view, values)

        dots = self.svg.node(serie_node, class_="dots")
        for i, (x, y) in enumerate(view_values):
            dot = self.svg.node(dots, class_='dot')
            self.svg.node(dot, 'circle', cx=x, cy=y, r=2.5)
            self.svg.node(dot, 'text', x=x, y=y
            ).text = self._get_value(values, i)
        self.svg.line(serie_node, view_values, class_='line', close=True)

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
            self.line(
                self._serie(serie.index), [
                (self._x_pos[i], v)
                for i, v in enumerate(serie.values)])
