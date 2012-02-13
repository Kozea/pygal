import os
from lxml import etree
from pygal.view import View
from pygal.util import template
from math import cos, sin, pi


class Svg(object):
    """Svg object"""
    ns = 'http://www.w3.org/2000/svg'

    def __init__(self, graph):
        self.graph = graph
        self.root = etree.Element(
            "{%s}svg" % self.ns,
            attrib={
                'viewBox': '0 0 %d %d' % (self.graph.width, self.graph.height)
            },
            nsmap={
                None: self.ns,
                'xlink': 'http://www.w3.org/1999/xlink',
            })

        self.defs = self.node(tag='defs')
        self.add_style(self.graph.base_css or os.path.join(
            os.path.dirname(__file__), 'css', 'graph.css'))

    def add_style(self, css):
        style = self.node(self.defs, 'style', type='text/css')
        with open(css) as f:
            style.text = template(
                f.read(),
                style=self.graph.style,
                font_sizes=self.graph.font_sizes)

    def node(self, parent=None, tag='g', attrib=None, **extras):
        if parent is None:
            parent = self.root
        attrib = attrib or {}
        attrib.update(extras)
        for key, value in attrib.items():
            if not isinstance(value, basestring):
                attrib[key] = str(value)
            if key == 'class_':
                attrib['class'] = attrib['class_']
                del attrib['class_']

        return etree.SubElement(parent, tag, attrib)

    def set_view(self):
        self.view = View(
            self.graph.width - self.graph.margin.x,
            self.graph.height - self.graph.margin.y,
            self.graph._box)

    def make_graph(self):
        self.graph_node = self.node(
            class_='graph %s' % self.graph.__class__.__name__)
        self.node(self.graph_node, 'rect',
                  class_='background',
                  x=0, y=0,
                  width=self.graph.width,
                  height=self.graph.height)
        self.plot = self.node(
            self.graph_node, class_="plot",
            transform="translate(%d, %d)" % (
                self.graph.margin.left, self.graph.margin.top))
        self.node(self.plot, 'rect',
                  class_='background',
                  x=0, y=0,
                  width=self.view.width,
                  height=self.view.height)

    def x_axis(self):
        if not self.graph._x_labels:
            return

        axis = self.node(self.plot, class_="axis x")

        if 0 not in [label[1] for label in self.graph._x_labels]:
            self.node(axis, 'path',
                      d='M%f %f v%f' % (0, 0, self.view.height),
                      class_='line')
        for label, position in self.graph._x_labels:
            guides = self.node(axis, class_='guides')
            x = self.view.x(position)
            y = self.view.height + 5
            self.node(guides, 'path',
                      d='M%f %f v%f' % (x, 0, self.view.height),
                    class_='%sline' % (
                        'guide ' if position != 0 else ''))
            text = self.node(guides, 'text',
                             x=x,
                             y=y + .5 * self.graph.label_font_size + 5)
            if self.graph.x_label_rotation:
                text.attrib['transform'] = "rotate(%d %f %f)" % (
                    self.graph.x_label_rotation, x, y)
            text.text = label

    def y_axis(self):
        if not self.graph._y_labels:
            return

        axis = self.node(self.plot, class_="axis y")

        if 0 not in [label[1] for label in self.graph._y_labels]:
            self.node(axis, 'path',
                      d='M%f %f h%f' % (0, self.view.height, self.view.width),
                      class_='line')
        for label, position in self.graph._y_labels:
            guides = self.node(axis, class_='guides')
            x = -5
            y = self.view.y(position)
            self.node(guides, 'path',
                      d='M%f %f h%f' % (0, y, self.view.width),
                      class_='%sline' % (
                          'guide ' if position != 0 else ''))
            text = self.node(guides, 'text',
                             x=x,
                             y=y + .35 * self.graph.label_font_size)
            if self.graph.y_label_rotation:
                text.attrib['transform'] = "rotate(%d %f %f)" % (
                    self.graph.y_label_rotation, x, y)
            text.text = label

    def legend(self):
        if not self.graph.show_legend:
            return
        legends = self.node(
            self.graph_node, class_='legends',
            transform='translate(%d, %d)' % (
                self.graph.margin.left + self.view.width + 10,
                self.graph.margin.top + 10))
        for i, title in enumerate(self.graph._legends):
            legend = self.node(legends, class_='legend')
            self.node(legend, 'rect',
                      x=0,
                      y=1.5 * i * self.graph.legend_box_size,
                      width=self.graph.legend_box_size,
                      height=self.graph.legend_box_size,
                      class_="color-%d" % i,
                  ).text = title
            # Serious magical numbers here
            self.node(legend, 'text',
                      x=self.graph.legend_box_size + 5,
                      y=1.5 * i * self.graph.legend_box_size
                      + .5 * self.graph.legend_box_size
                      + .3 * self.graph.legend_font_size
            ).text = title

    def title(self):
        if self.graph.title:
            self.node(self.graph_node, 'text', class_='title',
                      x=self.graph.margin.left + self.view.width / 2,
                      y=self.graph.title_font_size + 10
            ).text = self.graph.title

    def serie(self, serie):
        return self.node(
            self.plot, class_='series serie-%d color-%d' % (serie, serie))

    def line(self, serie_node, values, xy=False):
        view_values = map(self.view, values)
        origin = '%f %f' % view_values[0]

        dots = self.node(serie_node, class_="dots")
        for i, (x, y) in enumerate(view_values):
            dot = self.node(dots, class_='dot')
            self.node(dot, 'circle', cx=x, cy=y, r=2.5)
            self.node(dot, 'text', x=x, y=y).text = str(
                values[i]) if xy else str(values[i][1])

        svg_values = ' '.join(map(lambda x: '%f %f' % x, view_values))
        self.node(serie_node, 'path',
                  d='M%s L%s' % (origin, svg_values), class_='line')

    def bar(self, serie_node, serie, values, stack_vals=None):
        """Draw a bar graph for a serie"""
        # value here is a list of tuple range of tuple coord

        def view(rng):
            """Project range"""
            return (self.view(rng[0]), self.view(rng[1]))

        bars = self.node(serie_node, class_="bars")
        view_values = map(view, values)
        for i, ((x, y), (X, Y)) in enumerate(view_values):
            # x and y are left range coords and X, Y right ones
            width = X - x
            padding = .1 * width
            inner_width = width - 2 * padding
            height = self.view.y(0) - y
            if stack_vals == None:
                bar_width = inner_width / len(self.graph.series)
                bar_padding = .1 * bar_width
                bar_inner_width = bar_width - 2 * bar_padding
                offset = serie.index * bar_width + bar_padding
                shift = 0
            else:
                offset = 0
                bar_inner_width = inner_width
                shift = stack_vals[i][int(height < 0)]
                stack_vals[i][int(height < 0)] += height
            x = x + padding + offset

            if height < 0:
                y = y + height
                height = -height

            y_txt = y + height / 2 + .3 * self.graph.values_font_size
            bar = self.node(bars, class_='bar')
            self.node(bar, 'rect',
                      x=x,
                      y=y - shift,
                      rx=self.graph.rounded_bars * 1,
                      ry=self.graph.rounded_bars * 1,
                      width=bar_inner_width,
                      height=height,
                      class_='rect')
            self.node(bar, 'text',
                      x=x + bar_inner_width / 2,
                      y=y_txt - shift,
                      ).text = str(values[i][1][1])
        return stack_vals

    def slice(self, serie_node, start_angle, angle, perc):
        slices = self.node(serie_node, class_="slices")
        slice_ = self.node(slices, class_="slice")
        center = ((self.graph.width - self.graph.margin.x) / 2.,
                  (self.graph.height - self.graph.margin.y) / 2.)
        r = min(center)
        center_str = '%f %f' % center
        rxy = '%f %f' % tuple([r] * 2)
        to = '%f %f' % (r * sin(angle), r * (1 - cos(angle)))
        self.node(slice_, 'path',
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
        self.node(slice_, 'text',
                  x=center[0] + text_r * cos(text_angle),
                  y=center[1] - text_r * sin(text_angle),
              ).text = '{:.2%}'.format(perc)

    def render(self):
        return etree.tostring(
            self.root, pretty_print=True,
            xml_declaration=True, encoding='utf-8')
