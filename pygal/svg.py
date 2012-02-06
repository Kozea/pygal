import os
from lxml import etree
from pygal.view import View
from pygal.style import DefaultStyle


class Svg(object):
    """Svg object"""
    ns = 'http://www.w3.org/2000/svg'

    def __init__(self, width, height, base_css=None, style=None):
        self.width = width
        self.height = height
        self.margin = ()
        self.style = style or DefaultStyle
        self.root = etree.Element(
            "{%s}svg" % self.ns,
            attrib={
                'viewBox': '0 0 %d %d' % (width, height)
            },
            nsmap={
                None: self.ns,
                'xlink': 'http://www.w3.org/1999/xlink',
            })

        self.defs = self.node(tag='defs')

        base_css = base_css or os.path.join(
            os.path.dirname(__file__), 'css', 'graph.css')
        self.add_style(base_css)

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
                .format(style=self.style))

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

    def set_view(self, margin, ymin, ymax, xmin=0, xmax=1):
        self.view = View(
            self.width - margin.x,
            self.height - margin.y,
            xmin, xmax, ymin, ymax)

    def graph(self, margin):
        self.graph = self.node(class_='graph')
        self.node(self.graph, 'rect',
                  class_='background',
                  x=0, y=0,
                  width=self.width,
                  height=self.height)
        self.plot = self.node(
            self.graph, class_="plot",
            transform="translate(%d, %d)" % (margin.left, margin.top))
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
        for label in labels:
            guides = self.node(axis, class_='guides')
            x = self.view.x(label.pos)
            if x != 0:
                self.node(guides, 'path',
                          d='M%f %f v%f' % (x, 0, self.view.height),
                          class_='guide line')

            text = self.node(guides, 'text', x=x, y=self.view.height + 5)
            text.text = label.label

    def y_axis(self, labels):
        axis = self.node(self.plot, class_="axis y")
        # Plot axis
        self.node(axis, 'path',
                  d='M%f %f h%f' % (0, self.view.height, self.view.width),
                  class_='line')
        for label in labels:
            guides = self.node(axis, class_='guides')
            y = self.view.y(label.pos)
            if y != self.view.height:
                self.node(guides, 'path',
                          d='M%f %f h%f' % (0, y, self.view.width),
                          class_='guide line')
            text = self.node(guides, 'text', x=-5, y=y)
            text.text = label.label

    def legend(self, margin, titles):
        legend = self.node(
            self.graph, class_='legend',
            transform='translate(%d, %d)' % (
                margin.left + self.view.width + 10, margin.top + 10))
        for i, title in enumerate(titles):
            self.node(legend, 'rect', x=0, y=i * 15,
                      width=8, height=8, class_="color-%d" % i,
                  ).text = title
            self.node(legend, 'text', x=15, y=i * 15).text = title

    def title(self, margin, title):
        self.node(self.graph, 'text', class_='title',
                  x=margin.left + self.view.width / 2,
                  y=10).text = title

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
        view_values = map(lambda x: (self.view(x[0]), self.view(x[1])), values)

        for i, ((x, y), (X, Y)) in enumerate(view_values):
            width = X - x
            padding = .1 * width
            width = width - 2 * padding
            self.node(serie, 'rect',
                      width=width,
                      height=self.view.y(0) - y,
                      x=x + padding,
                      y=y,
                      class_='rect')

    def render(self):
        return etree.tostring(
            self.root, pretty_print=True,
            xml_declaration=True, encoding='utf-8')
