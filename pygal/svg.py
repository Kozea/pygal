import os
from lxml import etree
from pygal.view import View
from pygal.style import DefaultStyle


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

    def set_view(self, ymin, ymax, xmin=0, xmax=1):
        self.view = View(
            self.graph.width - self.graph.margin.x,
            self.graph.height - self.graph.margin.y,
            xmin, xmax, ymin, ymax)

    def make_graph(self):
        self.graph_node = self.node(class_='graph')
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

    def line(self, serie, values, origin=None):
        view_values = map(self.view, values)
        if origin == None:
            origin = '%f %f' % view_values[0]

        dots = self.node(serie, class_="dots")
        for i, (x, y) in enumerate(view_values):
            dot = self.node(dots, class_='dot')
            self.node(dot, 'circle', cx=x, cy=y, r=2.5)
            self.node(dot, 'text', x=x, y=y).text = str(values[i][1])

        svg_values = ' '.join(map(lambda x: '%f %f' % x, view_values))
        self.node(serie, 'path',
                  d='M%s L%s' % (origin, svg_values), class_='line')

    def bar(self, serie, values, origin=None):
        """Draw a bar graph for a serie"""
        # value here is a list of tuple range of tuple coord

        def view(rng):
            """Project range"""
            return (self.view(rng[0]), self.view(rng[1]))

        view_values = map(view, values)
        for i, ((x, y), (X, Y)) in enumerate(view_values):
            # x and y are left range coords and X, Y right ones
            width = X - x
            padding = .1 * width
            width = width - 2 * padding
            self.node(serie, 'rect',
                      x=x + padding,
                      y=y,
                      width=width,
                      height=self.view.y(0) - y,
                      class_='rect')

    def render(self):
        return etree.tostring(
            self.root, pretty_print=True,
            xml_declaration=True, encoding='utf-8')
