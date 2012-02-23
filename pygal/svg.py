# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
import os
from lxml import etree
from pygal.util import template


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
            },
            onload="svg_load();")
        self.root.append(etree.Comment(u'Generated with pygal ©Kozea 2012'))
        self.root.append(etree.Comment(u'http://github.com/Kozea/pygal'))
        self.defs = self.node(tag='defs')
        self.add_style(self.graph.base_css or os.path.join(
            os.path.dirname(__file__), 'css', 'graph.css'))
        self.add_script(self.graph.base_js or os.path.join(
            os.path.dirname(__file__), 'js', 'graph.js'))

    def add_style(self, css):
        style = self.node(self.defs, 'style', type='text/css')
        with open(css) as f:
            templ = template(
                f.read(),
                style=self.graph.style,
                font_sizes=self.graph.font_sizes,
                hidden='y' if self.graph._horizontal else 'x')
            style.text = templ.decode('utf-8')

    def add_script(self, js):
        script = self.node(self.root, 'script', type='text/javascript')
        with open(js) as f:
            script.text = f.read()

    def node(self, parent=None, tag='g', attrib=None, **extras):
        if parent is None:
            parent = self.root
        attrib = attrib or {}
        attrib.update(extras)
        for key, value in attrib.items():
            if value is None:
                del attrib[key]
            elif not isinstance(value, basestring):
                attrib[key] = str(value)
            elif key == 'class_':
                attrib['class'] = attrib['class_']
                del attrib['class_']
        return etree.SubElement(parent, tag, attrib)

    def transposable_node(self, parent=None, tag='g', attrib=None, **extras):
        if self.graph._horizontal:
            for key1, key2 in (('x', 'y'), ('width', 'height')):
                attr1 = extras.get(key1, None)
                attr2 = extras.get(key2, None)
                extras[key1], extras[key2] = attr2, attr1
        return self.node(parent, tag, attrib, **extras)

    def format(self, xy):
        return '%f %f' % xy

    def line(self, node, coords, close=False, **kwargs):
        root = 'M%s L%s Z' if close else 'M%s L%s'
        origin = self.format(coords[0])
        line = ' '.join(map(self.format, coords[1:]))
        self.node(node, 'path',
                  d=root % (origin, line), **kwargs)

    def render(self):
        return etree.tostring(
            self.root, pretty_print=True,
            xml_declaration=True, encoding='utf-8')
