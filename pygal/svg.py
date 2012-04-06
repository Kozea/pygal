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
"""
Svg helper

"""

from __future__ import division
import io
import os
from lxml import etree
from math import cos, sin, pi
from pygal.util import template, coord_format
from pygal import __version__


class Svg(object):
    """Svg object"""
    ns = 'http://www.w3.org/2000/svg'

    def __init__(self, graph):
        self.graph = graph
        self.root = None
        self.defs = None

    def reinit(self):
        """(Re-)initialization"""
        self.root = etree.Element(
            "{%s}svg" % self.ns,
            nsmap={
                None: self.ns,
                'xlink': 'http://www.w3.org/1999/xlink',
            },
            onload="svg_load();")
        self.root.append(etree.Comment(
            u'Generated with pygal %s ©Kozea 2012' % __version__))
        self.root.append(etree.Comment(u'http://github.com/Kozea/pygal'))
        self.defs = self.node(tag='defs')

    def add_style(self, css):
        """Add the css to the svg"""
        style = self.node(self.defs, 'style', type='text/css')
        with io.open(css, encoding='utf-8') as f:
            templ = template(
                f.read(),
                style=self.graph.style,
                font_sizes=self.graph.font_sizes(),
                hidden='y' if self.graph.horizontal else 'x')
            style.text = templ

    def add_script(self, js):
        """Add the js to the svg"""
        script = self.node(self.defs, 'script', type='text/javascript')
        with io.open(js, encoding='utf-8') as f:
            templ = template(
                f.read(),
                font_sizes=self.graph.font_sizes(False),
                animation_steps=self.graph.animation_steps
            )
            script.text = templ

    def node(self, parent=None, tag='g', attrib=None, **extras):
        """Make a new svg node"""
        if parent is None:
            parent = self.root
        attrib = attrib or {}
        attrib.update(extras)
        for key, value in attrib.items():
            if value is None:
                del attrib[key]
            elif not isinstance(value, basestring):
                attrib[key] = str(value)
            elif key.endswith('_'):
                attrib[key.rstrip('_')] = attrib[key]
                del attrib[key]
            elif key == 'href':
                attrib['{http://www.w3.org/1999/xlink}' + key] = attrib[key]
                del attrib[key]
        return etree.SubElement(parent, tag, attrib)

    def transposable_node(self, parent=None, tag='g', attrib=None, **extras):
        """Make a new svg node which can be transposed if horizontal"""
        if self.graph.horizontal:
            for key1, key2 in (('x', 'y'), ('width', 'height')):
                attr1 = extras.get(key1, None)
                attr2 = extras.get(key2, None)
                extras[key1], extras[key2] = attr2, attr1
        return self.node(parent, tag, attrib, **extras)

    def line(self, node, coords, close=False, **kwargs):
        """Draw a svg line"""
        if len(coords) < 2:
            return
        root = 'M%s L%s Z' if close else 'M%s L%s'
        origin_index = 0
        while None in coords[origin_index]:
            origin_index += 1
        origin = coord_format(coords[origin_index])
        line = ' '.join([coord_format(c)
                         for c in coords[origin_index + 1:]
                         if None not in c])
        self.node(node, 'path',
                  d=root % (origin, line), **kwargs)

    def slice(self, serie_node, node, radius, small_radius,
            angle, start_angle, center, val):
        """Draw a pie slice"""
        project = lambda rho, alpha: (
            rho * sin(-alpha), rho * cos(-alpha))
        diff = lambda x, y: (x[0] - y[0], x[1] - y[1])
        fmt = lambda x: '%f %f' % x
        get_radius = lambda r: fmt(tuple([r] * 2))
        absolute_project = lambda rho, theta: fmt(
                diff(center, project(rho, theta)))

        if angle == 2 * pi:
            self.node(node, 'circle',
                          cx=center[0],
                          cy=center[1],
                          r=radius,
                          class_='slice reactive tooltip-trigger')
        else:
            to = [absolute_project(radius, start_angle),
                  absolute_project(radius, start_angle + angle),
                  absolute_project(small_radius, start_angle + angle),
                  absolute_project(small_radius, start_angle)]
            self.node(node, 'path',
                      d='M%s A%s 0 %d 1 %s L%s A%s 0 %d 0 %s z' % (
                          to[0],
                          get_radius(radius), int(angle > pi), to[1],
                          to[2],
                          get_radius(small_radius), int(angle > pi), to[3]),
                      class_='slice reactive tooltip-trigger')
        self.node(node, 'desc', class_="value").text = val
        tooltip_position = map(
            str, diff(center, project(
                (radius + small_radius) / 2, start_angle + angle / 2)))
        self.node(node, 'desc',
                      class_="x centered").text = tooltip_position[0]
        self.node(node, 'desc',
                      class_="y centered").text = tooltip_position[1]
        if self.graph.print_values:
            self.node(
                serie_node['text_overlay'], 'text',
                class_='centered',
                x=tooltip_position[0],
                y=tooltip_position[1]
            ).text = val if self.graph.print_zeroes or val != '0%' else ''

    def pre_render(self, no_data=False):
        """Last things to do before rendering"""
        self.add_style(self.graph.base_css or os.path.join(
            os.path.dirname(__file__), 'css', 'graph.css'))
        self.add_script(self.graph.base_js or os.path.join(
            os.path.dirname(__file__), 'js', 'graph.js'))
        self.root.set(
            'viewBox', '0 0 %d %d' % (self.graph.width, self.graph.height))
        if self.graph.explicit_size:
            self.root.set('width', str(self.graph.width))
            self.root.set('height', str(self.graph.height))
        if no_data:
            no_data = self.node(self.root, 'text',
            x=self.graph.width / 2,
            y=self.graph.height / 2,
            class_='no_data')
            no_data.text = self.graph.no_data_text

    def render(self, is_unicode=False):
        """Last thing to do before rendering"""
        svg = etree.tostring(
            self.root, pretty_print=True,
            xml_declaration=not self.graph.disable_xml_declaration,
            encoding='utf-8')
        if self.graph.disable_xml_declaration or is_unicode:
            svg = svg.decode('utf-8')
        return svg
