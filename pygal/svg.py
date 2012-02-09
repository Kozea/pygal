import os
from lxml import etree
from pygal.view import View
from pygal.style import DefaultStyle
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
            style.text = (
                f.read()
                # Lol
                .replace('{{ ', '\x00')
                .replace('{', '{{')
                .replace('\x00', '{')
                .replace(' }}', '\x00')
                .replace('}', '}}')
                .replace('\x00', '}')
                .format(style=self.graph.style))

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

    def set_view(self, ymin=0, ymax=1, xmin=0, xmax=1):
        self.view = View(
            self.graph.width - self.graph.margin.x,
            self.graph.height - self.graph.margin.y,
            xmin, xmax, ymin, ymax)

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

    def x_axis(self, labels):
        axis = self.node(self.plot, class_="axis x")
        # Plot axis
        self.node(axis, 'path',
                  d='M%f %f v%f' % (0, 0, self.view.height),
                  class_='line')
        if not labels:
            return
        for label, position in labels:
            guides = self.node(axis, class_='guides')
            x = self.view.x(position)
            if x != 0:
                self.node(guides, 'path',
                          d='M%f %f v%f' % (x, 0, self.view.height),
                          class_='guide line')

            text = self.node(guides, 'text', x=x, y=self.view.height + 5)
            text.text = label

    def y_axis(self, labels):
        axis = self.node(self.plot, class_="axis y")
        # Plot axis
        self.node(axis, 'path',
                  d='M%f %f h%f' % (0, self.view.height, self.view.width),
                  class_='line')
        for label, position in labels:
            guides = self.node(axis, class_='guides')
            y = self.view.y(position)
            if y != self.view.height:
                self.node(guides, 'path',
                          d='M%f %f h%f' % (0, y, self.view.width),
                          class_='guide line')
            text = self.node(guides, 'text', x=-5, y=y)
            text.text = label

    def legend(self, titles):
        legend = self.node(
            self.graph_node, class_='legend',
            transform='translate(%d, %d)' % (
                self.graph.margin.left + self.view.width + 10,
                self.graph.margin.top + 10))
        for i, title in enumerate(titles):
            self.node(legend, 'rect', x=0, y=i * 15,
                      width=8, height=8, class_="color-%d" % i,
                  ).text = title
            self.node(legend, 'text', x=15, y=i * 15).text = title

    def title(self):
        self.node(self.graph_node, 'text', class_='title',
                  x=self.graph.margin.left + self.view.width / 2,
                  y=10).text = self.graph.title

    def serie(self, serie):
        return self.node(
            self.plot, class_='series serie-%d color-%d' % (serie, serie))

    def line(self, serie_node, values):
        view_values = map(self.view, values)
        origin = '%f %f' % view_values[0]

        dots = self.node(serie_node, class_="dots")
        for i, (x, y) in enumerate(view_values):
            dot = self.node(dots, class_='dot')
            self.node(dot, 'circle', cx=x, cy=y, r=2.5)
            self.node(dot, 'text', x=x, y=y).text = str(values[i][1])

        svg_values = ' '.join(map(lambda x: '%f %f' % x, view_values))
        self.node(serie_node, 'path',
                  d='M%s L%s' % (origin, svg_values), class_='line')

    def bar(self, serie_node, serie, values):
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
            bar_width = inner_width / len(self.graph.series)
            bar_padding = .1 * bar_width
            bar_inner_width = bar_width - 2 * bar_padding
            offset = serie.index * bar_width + bar_padding
            height = self.view.y(0) - y
            x = x + padding + offset
            y_txt = y + height / 2
            if height < 0:
                y = y + height
                height = -height
                y_txt = y + height / 2
            bar = self.node(bars, class_='bar')
            self.node(bar, 'rect',
                      x=x,
                      y=y,
                      rx=self.graph.rounded_bars * 1,
                      ry=self.graph.rounded_bars * 1,
                      width=bar_inner_width,
                      height=height,
                      class_='rect')
            self.node(bar, 'text',
                      x=x + bar_inner_width / 2,
                      y=y_txt,
                      ).text = str(values[i][1][1])

    def stackbar(self, serie_node, serie, values, stack_vals):
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
            x = x + padding
            y_txt = y + height / 2
            shift = stack_vals[i]
            stack_vals[i] += height
            if height < 0:
                y = y + height
                height = -height
                y_txt = y + height / 2
            bar = self.node(bars, class_='bar')
            self.node(bar, 'rect',
                      x=x,
                      y=y - shift,
                      rx=self.graph.rounded_bars * 1,
                      ry=self.graph.rounded_bars * 1,
                      width=inner_width,
                      height=height,
                      class_='rect')
            self.node(bar, 'text',
                      x=x + inner_width / 2,
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
        text_r = min(center)
        self.node(slice_, 'text',
                  x=center[0] + text_r * cos(text_angle),
                  y=center[1] - text_r * sin(text_angle),
              ).text = '{:.2%}'.format(perc)

    def render(self):
        return etree.tostring(
            self.root, pretty_print=True,
            xml_declaration=True, encoding='utf-8')
