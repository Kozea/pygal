from pygal.serie import Serie
from pygal.graph.graph import Graph
from math import cos, sin, pi


class Pie(Graph):
    """Pie graph"""

    def slice(self, serie_node, start_angle, angle, perc):
        slices = self.svg.node(serie_node, class_="slices")
        slice_ = self.svg.node(slices, class_="slice")
        center = ((self.width - self.margin.x) / 2.,
                  (self.height - self.margin.y) / 2.)
        r = min(center)
        center_str = '%f %f' % center
        rxy = '%f %f' % tuple([r] * 2)
        to = '%f %f' % (r * sin(angle), r * (1 - cos(angle)))
        self.svg.node(slice_, 'path',
                  d='M%s v%f a%s 0 %d 1 %s z' % (
                      center_str, -r,
                      rxy,
                      1 if angle > pi else 0,
                      to),
                  transform='rotate(%f %s)' % (
                      start_angle * 180 / pi, center_str),
                  class_='slice')
        text_angle = pi / 2. - (start_angle + angle / 2.)
        text_r = min(center) * .8
        self.svg.node(slice_, 'text',
                  x=center[0] + text_r * cos(text_angle),
                  y=center[1] - text_r * sin(text_angle),
              ).text = '{:.2%}'.format(perc)

    def add(self, title, value):
        self.series.append(Serie(title, [value], len(self.series)))

    def _plot(self):
        total = float(sum(serie.values[0] for serie in self.series))
        current_angle = 0
        for serie in self.series:
            val = serie.values[0]
            angle = 2 * pi * val / total
            self.slice(
                self._serie(serie.index),
                current_angle,
                angle, val / total)
            current_angle += angle
