from pygal.graph.line import Line
from pygal.view import PolarView
from pygal.util import deg
from math import cos, sin, pi


class Radar(Line):
    """Kiviat graph"""

    def _get_value(self, values, i):
        return str(values[i][0])

    def _set_view(self):
        self.view = PolarView(
            self.width - self.margin.x,
            self.height - self.margin.y,
            self._box)

    def _x_axis(self):
        if not self._x_labels:
            return

        axis = self.svg.node(self.plot, class_="axis x web")
        format = lambda x: '%f %f' % x
        center = self.view((0, 0))
        r = self._rmax
        for label, theta in self._x_labels:
            guides = self.svg.node(axis, class_='guides')
            end = self.view((r, theta))
            self.svg.node(guides, 'path',
                      d='M%s L%s' % (format(center), format(end)),
                      class_='line')
            r_txt = (1 - self._box.__class__._margin) * self._box.ymax
            pos_text = self.view((r_txt, theta))
            text = self.svg.node(guides, 'text',
                      x=pos_text[0],
                      y=pos_text[1]
            )
            text.text = label
            angle = - theta + pi / 2.
            if cos(angle) < 0:
                angle -= pi
            text.attrib['transform'] = 'rotate(%f %s)' % (
                deg(angle), format(pos_text))

    def _y_axis(self):
        if not self._y_labels:
            return

        axis = self.svg.node(self.plot, class_="axis y web")

        for label, r in reversed(self._y_labels):
            guides = self.svg.node(axis, class_='guides')
            self.svg.line(
                guides, [self.view((r, theta)) for theta in self._x_pos],
                close=True,
                class_='guide line')
            x, y = self.view((r, self._x_pos[0]))
            self.svg.node(guides, 'text',
                             x=x - 5,
                             y=y
            ).text = label

    def _compute(self):
        vals = [val for serie in self.series for val in serie.values]
        self._box._margin *= 2
        self._box.xmin = self._box.ymin = 0
        self._box.xmax = self._box.ymax = self._rmax = max(vals)

        x_step = len(self.series[0].values)
        delta = 2 * pi / float(len(self.x_labels))
        self._x_pos = [.5 * pi - i * delta for i in range(x_step)]
        self._y_pos = self._pos(
            self._box.ymin, self._box.ymax, self.y_scale, max_scale=8
        ) if not self.y_labels else map(int, self.y_labels)
        self._x_labels = self.x_labels and zip(self.x_labels, self._x_pos)
        self._y_labels = zip(map(str, self._y_pos), self._y_pos)
        self._box.xmin = self._box.ymin = - self._box.ymax
        self._line_close = True

    def _plot(self):
        for serie in self.series:
            serie_node = self._serie(serie.index)
            self.line(serie_node, [
                     (v, self._x_pos[i])
                     for i, v in enumerate(serie.values)])
