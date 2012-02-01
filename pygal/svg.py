from lxml import etree


class Svg(object):
    """Svg object"""
    ns = 'http://www.w3.org/2000/svg'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = etree.Element(
            "{%s}svg" % self.ns,
            attrib={
                'viewBox': '0 0 %d %d' % (width, height)
            },
            nsmap={
                None: self.ns,
                'xlink': 'http://www.w3.org/1999/xlink',
            })

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

    def format_coords(self, xy):
        return '%f %f' % xy

    def graph(self):
        self.graph = self.node(id='graph')
        self.node(self.graph, 'rect', id='graph_background',
                  x=0, y=0, width=self.width, height=self.height)

    def line(self, values, origin=None):
        origin = self.format_coords(origin or values[0])
        values = ' '.join(map(self.format_coords, values))
        self.node(self.graph, 'path',
                  d='M%s L%s' % (origin, values))

    def render(self):
        return etree.tostring(
            self.root, pretty_print=True,
            xml_declaration=True, encoding='utf-8')
