# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2014 Kozea
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
from pygal._compat import to_str, u
from pygal.etree import etree
import io
import os
import json
from datetime import date, datetime
from numbers import Number
from math import cos, sin, pi
from pygal.util import template, coord_format, minify_css
from pygal import __version__


class Svg(object):
    """Svg object"""
    ns = 'http://www.w3.org/2000/svg'
    xlink_ns = 'http://www.w3.org/1999/xlink'

    def __init__(self, graph):
        self.graph = graph
        if not graph.no_prefix:
            self.id = '#chart-%s ' % graph.uuid
        else:
            self.id = ''
        self.processing_instructions = [
            etree.ProcessingInstruction(
                u('xml'), u("version='1.0' encoding='utf-8'"))]
        if etree.lxml:
            attrs = {
                'nsmap': {
                    None: self.ns,
                    'xlink': self.xlink_ns
                }
            }
        else:
            attrs = {
                'xmlns': self.ns
            }
            if hasattr(etree, 'register_namespace'):
                etree.register_namespace('xlink', self.xlink_ns)
            else:
                etree._namespace_map[self.xlink_ns] = 'xlink'

        self.root = etree.Element('svg', **attrs)
        self.root.attrib['id'] = self.id.lstrip('#').rstrip()
        self.root.attrib['class'] = 'pygal-chart'
        self.root.append(
            etree.Comment(u(
                'Generated with pygal %s (%s) ©Kozea 2011-2014 on %s' % (
                    __version__,
                    'lxml' if etree.lxml else 'etree',
                    date.today().isoformat()))))
        self.root.append(etree.Comment(u('http://pygal.org')))
        self.root.append(etree.Comment(u('http://github.com/Kozea/pygal')))
        self.defs = self.node(tag='defs')
        self.title = self.node(tag='title')
        self.title.text = graph.title or 'Pygal'

    def add_styles(self):
        """Add the css to the svg"""
        colors = self.graph.config.style.get_colors(self.id)
        all_css = []
        for css in ['base.css'] + list(self.graph.css):
            if '://' in css:
                self.processing_instructions.append(
                    etree.PI(
                        u('xml-stylesheet'), u('href="%s"' % css)))
            else:
                if css.startswith('inline:'):
                    css_text = css[len('inline:'):]
                else:
                    if not os.path.exists(css):
                        css = os.path.join(
                            os.path.dirname(__file__), 'css', css)
                    with io.open(css, encoding='utf-8') as f:
                        css_text = template(
                            f.read(),
                            style=self.graph.config.style,
                            colors=colors,
                            font_sizes=self.graph.config.font_sizes(),
                            id=self.id)
                if not self.graph.pretty_print:
                    css_text = minify_css(css_text)
                all_css.append(css_text)
        self.node(
            self.defs, 'style', type='text/css').text = '\n'.join(all_css)

    def add_scripts(self):
        """Add the js to the svg"""
        common_script = self.node(self.defs, 'script', type='text/javascript')
        common_script.text = " = ".join(
            ("window.config", json.dumps(
                self.graph.config.to_dict(),
                default=lambda o: (
                    o.isoformat() if isinstance(o, (datetime, date))
                    else json.JSONEncoder().default(o))
            )))

        for js in self.graph.js:
            if '://' in js:
                self.node(
                    self.defs, 'script', type='text/javascript', href=js)
            else:
                script = self.node(self.defs, 'script', type='text/javascript')
                with io.open(js, encoding='utf-8') as f:
                    script.text = f.read()

    def node(self, parent=None, tag='g', attrib=None, **extras):
        """Make a new svg node"""
        if parent is None:
            parent = self.root
        attrib = attrib or {}
        attrib.update(extras)

        def in_attrib_and_number(key):
            return key in attrib and isinstance(attrib[key], Number)

        for pos, dim in (('x', 'width'), ('y', 'height')):
            if in_attrib_and_number(dim) and attrib[dim] < 0:
                attrib[dim] = - attrib[dim]
                if in_attrib_and_number(pos):
                    attrib[pos] = attrib[pos] - attrib[dim]

        for key, value in dict(attrib).items():
            if value is None:
                del attrib[key]

            attrib[key] = to_str(value)
            if key.endswith('_'):
                attrib[key.rstrip('_')] = attrib[key]
                del attrib[key]
            elif key == 'href':
                attrib[etree.QName(
                    'http://www.w3.org/1999/xlink',  key)] = attrib[key]
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

    def serie(self, serie):
        """Make serie node"""
        return dict(
            plot=self.node(
                self.graph.nodes['plot'],
                class_='series serie-%d color-%d' % (
                    serie.index, serie.index % len(
                        self.graph.style['colors']))),
            overlay=self.node(
                self.graph.nodes['overlay'],
                class_='series serie-%d color-%d' % (
                    serie.index, serie.index % len(
                        self.graph.style['colors']))),
            text_overlay=self.node(
                self.graph.nodes['text_overlay'],
                class_='series serie-%d color-%d' % (
                    serie.index, serie.index % len(
                        self.graph.style['colors']))))

    def line(self, node, coords, close=False, **kwargs):
        """Draw a svg line"""
        line_len = len(coords)
        if line_len < 2:
            return
        root = 'M%s L%s Z' if close else 'M%s L%s'
        origin_index = 0
        while origin_index < line_len and None in coords[origin_index]:
            origin_index += 1
        if origin_index == line_len:
            return
        origin = coord_format(coords[origin_index])
        line = ' '.join([coord_format(c)
                         for c in coords[origin_index + 1:]
                         if None not in c])
        self.node(node, 'path',
                  d=root % (origin, line), **kwargs)

    def slice(
            self, serie_node, node, radius, small_radius,
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
        elif angle > 0:
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
        x, y = diff(center, project(
            (radius + small_radius) / 2, start_angle + angle / 2))

        self.graph._tooltip_data(node, val, x, y, classes="centered")
        if angle >= 0.3:  # 0.3 radians is about 17 degrees
            self.graph._static_value(serie_node, val, x, y)

    def pre_render(self):
        """Last things to do before rendering"""
        self.add_styles()
        self.add_scripts()
        self.root.set(
            'viewBox', '0 0 %d %d' % (self.graph.width, self.graph.height))
        if self.graph.explicit_size:
            self.root.set('width', str(self.graph.width))
            self.root.set('height', str(self.graph.height))

    def draw_no_data(self):
        no_data = self.node(self.graph.nodes['text_overlay'], 'text',
                            x=self.graph.view.width / 2,
                            y=self.graph.view.height / 2,
                            class_='no_data')
        no_data.text = self.graph.no_data_text

    def render(self, is_unicode=False, pretty_print=False):
        """Last thing to do before rendering"""
        for f in self.graph.xml_filters:
            self.root = f(self.root)
        args = {
            'encoding': 'utf-8'
        }
        if etree.lxml:
            args['pretty_print'] = pretty_print
        svg = etree.tostring(
            self.root, **args)
        if not self.graph.disable_xml_declaration:
            svg = b'\n'.join(
                [etree.tostring(
                    pi, **args)
                 for pi in self.processing_instructions]
            ) + b'\n' + svg
        if self.graph.disable_xml_declaration or is_unicode:
            svg = svg.decode('utf-8')
        return svg
