# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2016 Kozea
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
"""Svg helper"""

from __future__ import division

import io
import json
import os
from datetime import date, datetime
from math import pi
from numbers import Number

from pygal import __version__
from pygal._compat import quote_plus, to_str, u
from pygal.etree import etree
from pygal.util import (
    coord_abs_project, coord_diff, coord_dual, coord_format, coord_project,
    minify_css, template)

nearly_2pi = 2 * pi - .00001


class Svg(object):

    """Svg related methods"""

    ns = 'http://www.w3.org/2000/svg'
    xlink_ns = 'http://www.w3.org/1999/xlink'

    def __init__(self, graph):
        """Create the svg helper with the chart instance"""
        self.graph = graph
        if not graph.no_prefix:
            self.id = '#chart-%s ' % graph.uuid
        else:
            self.id = ''
        self.processing_instructions = []
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
        if graph.classes:
            self.root.attrib['class'] = ' '.join(graph.classes)
        self.root.append(
            etree.Comment(u(
                'Generated with pygal %s (%s) ©Kozea 2012-2016 on %s' % (
                    __version__,
                    'lxml' if etree.lxml else 'etree',
                    date.today().isoformat()))))
        self.root.append(etree.Comment(u('http://pygal.org')))
        self.root.append(etree.Comment(u('http://github.com/Kozea/pygal')))
        self.defs = self.node(tag='defs')
        self.title = self.node(tag='title')
        self.title.text = graph.title or 'Pygal'

        for def_ in self.graph.defs:
            self.defs.append(etree.fromstring(def_))

    def add_styles(self):
        """Add the css to the svg"""
        colors = self.graph.style.get_colors(self.id, self.graph._order)
        strokes = self.get_strokes()
        all_css = []
        auto_css = ['file://base.css']

        if self.graph.style._google_fonts:
            auto_css.append(
                '//fonts.googleapis.com/css?family=%s' % quote_plus(
                    '|'.join(self.graph.style._google_fonts))
            )

        for css in auto_css + list(self.graph.css):
            css_text = None
            if css.startswith('inline:'):
                css_text = css[len('inline:'):]
            elif css.startswith('file://'):
                css = css[len('file://'):]

                if not os.path.exists(css):
                    css = os.path.join(
                        os.path.dirname(__file__), 'css', css)

                with io.open(css, encoding='utf-8') as f:
                    css_text = template(
                        f.read(),
                        style=self.graph.style,
                        colors=colors,
                        strokes=strokes,
                        id=self.id)

            if css_text is not None:
                if not self.graph.pretty_print:
                    css_text = minify_css(css_text)
                all_css.append(css_text)
            else:
                if css.startswith('//') and self.graph.force_uri_protocol:
                    css = '%s:%s' % (self.graph.force_uri_protocol, css)
                self.processing_instructions.append(
                    etree.PI(
                        u('xml-stylesheet'), u('href="%s"' % css)))
        self.node(
            self.defs, 'style', type='text/css').text = '\n'.join(all_css)

    def add_scripts(self):
        """Add the js to the svg"""
        common_script = self.node(self.defs, 'script', type='text/javascript')

        def get_js_dict():
            return dict(
                (k, getattr(self.graph.state, k))
                for k in dir(self.graph.config)
                if not k.startswith('_') and hasattr(self.graph.state, k) and
                not hasattr(getattr(self.graph.state, k), '__call__'))

        def json_default(o):
            if isinstance(o, (datetime, date)):
                return o.isoformat()
            if hasattr(o, 'to_dict'):
                return o.to_dict()
            return json.JSONEncoder().default(o)

        dct = get_js_dict()
        # Config adds
        dct['legends'] = [
            l.get('title') if isinstance(l, dict) else l
            for l in self.graph._legends + self.graph._secondary_legends]

        common_js = 'window.pygal = window.pygal || {};'
        common_js += 'window.pygal.config = window.pygal.config || {};'
        if self.graph.no_prefix:
            common_js += 'window.pygal.config = '
        else:
            common_js += 'window.pygal.config[%r] = ' % self.graph.uuid

        common_script.text = common_js + json.dumps(dct, default=json_default)

        for js in self.graph.js:
            if js.startswith('file://'):
                script = self.node(self.defs, 'script', type='text/javascript')
                with io.open(js[len('file://'):], encoding='utf-8') as f:
                    script.text = f.read()
            else:
                if js.startswith('//') and self.graph.force_uri_protocol:
                    js = '%s:%s' % (self.graph.force_uri_protocol, js)
                self.node(self.defs, 'script', type='text/javascript', href=js)

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
                    'http://www.w3.org/1999/xlink', key)] = attrib[key]
                del attrib[key]
        return etree.SubElement(parent, tag, attrib)

    def transposable_node(self, parent=None, tag='g', attrib=None, **extras):
        """Make a new svg node which can be transposed if horizontal"""
        if self.graph.horizontal:
            for key1, key2 in (('x', 'y'), ('width', 'height'), ('cx', 'cy')):
                attr1 = extras.get(key1, None)
                attr2 = extras.get(key2, None)
                if attr2:
                    extras[key1] = attr2
                elif attr1:
                    del extras[key1]
                if attr1:
                    extras[key2] = attr1
                elif attr2:
                    del extras[key2]
        return self.node(parent, tag, attrib, **extras)

    def serie(self, serie):
        """Make serie node"""
        return dict(
            plot=self.node(
                self.graph.nodes['plot'],
                class_='series serie-%d color-%d' % (
                    serie.index, serie.index)),
            overlay=self.node(
                self.graph.nodes['overlay'],
                class_='series serie-%d color-%d' % (
                    serie.index, serie.index)),
            text_overlay=self.node(
                self.graph.nodes['text_overlay'],
                class_='series serie-%d color-%d' % (
                    serie.index, serie.index)))

    def line(self, node, coords, close=False, **kwargs):
        """Draw a svg line"""
        line_len = len(coords)
        if len([c for c in coords if c[1] is not None]) < 2:
            return
        root = 'M%s L%s Z' if close else 'M%s L%s'
        origin_index = 0
        while origin_index < line_len and None in coords[origin_index]:
            origin_index += 1
        if origin_index == line_len:
            return
        if self.graph.horizontal:
            coord_format = lambda xy: '%f %f' % (xy[1], xy[0])
        else:
            coord_format = lambda xy: '%f %f' % xy

        origin = coord_format(coords[origin_index])
        line = ' '.join([coord_format(c)
                         for c in coords[origin_index + 1:]
                         if None not in c])
        return self.node(
            node, 'path', d=root % (origin, line), **kwargs)

    def slice(
            self, serie_node, node, radius, small_radius,
            angle, start_angle, center, val, i, metadata):
        """Draw a pie slice"""
        if angle == 2 * pi:
            angle = nearly_2pi

        if angle > 0:
            to = [coord_abs_project(center, radius, start_angle),
                  coord_abs_project(center, radius, start_angle + angle),
                  coord_abs_project(center, small_radius, start_angle + angle),
                  coord_abs_project(center, small_radius, start_angle)]
            rv = self.node(
                node, 'path',
                d='M%s A%s 0 %d 1 %s L%s A%s 0 %d 0 %s z' % (
                    to[0],
                    coord_dual(radius), int(angle > pi), to[1],
                    to[2],
                    coord_dual(small_radius), int(angle > pi), to[3]),
                class_='slice reactive tooltip-trigger')
        else:
            rv = None
        x, y = coord_diff(center, coord_project(
            (radius + small_radius) / 2, start_angle + angle / 2))

        self.graph._tooltip_data(
            node, val, x, y, "centered",
            self.graph._x_labels and self.graph._x_labels[i][0])
        if angle >= 0.3:  # 0.3 radians is about 17 degrees
            self.graph._static_value(serie_node, val, x, y, metadata)
        return rv

    def gauge_background(
            self, serie_node, start_angle, center, radius, small_radius,
            end_angle, half_pie, max_value):

        if end_angle == 2 * pi:
            end_angle = nearly_2pi

        to_shade = [
            coord_abs_project(center, radius, start_angle),
            coord_abs_project(center, radius, end_angle),
            coord_abs_project(center, small_radius, end_angle),
            coord_abs_project(center, small_radius, start_angle)]

        self.node(
            serie_node['plot'], 'path',
            d='M%s A%s 0 1 1 %s L%s A%s 0 1 0 %s z' % (
                to_shade[0],
                coord_dual(radius),
                to_shade[1],
                to_shade[2],
                coord_dual(small_radius),
                to_shade[3]),
            class_='gauge-background reactive')

        if half_pie:
            begin_end = [
                coord_diff(
                    center,
                    coord_project(
                        radius - (radius - small_radius) / 2, start_angle)),
                coord_diff(
                    center,
                    coord_project(
                        radius - (radius - small_radius) / 2, end_angle))]
            pos = 0
            for i in begin_end:
                self.node(
                    serie_node['plot'], 'text',
                    class_='y-{} bound reactive'.format(pos),
                    x=i[0],
                    y=i[1] + 10,
                    attrib={'text-anchor': 'middle'}
                ).text = '{}'.format(0 if pos == 0 else max_value)
                pos += 1
        else:
            middle_radius = .5 * (radius + small_radius)
            # Correct text vertical alignment
            middle_radius -= .1 * (radius - small_radius)
            to_labels = [
                coord_abs_project(
                    center, middle_radius, 0),
                coord_abs_project(
                    center, middle_radius, nearly_2pi)
            ]
            self.node(
                self.defs, 'path', id='valuePath-%s%s' % center,
                d='M%s A%s 0 1 1 %s' % (
                    to_labels[0],
                    coord_dual(middle_radius),
                    to_labels[1]
                ))
            text_ = self.node(
                serie_node['text_overlay'], 'text')
            self.node(
                text_, 'textPath', class_='max-value reactive',
                attrib={
                    'href': '#valuePath-%s%s' % center,
                    'startOffset': '99%',
                    'text-anchor': 'end'
                }
            ).text = max_value

    def solid_gauge(
            self, serie_node, node, radius, small_radius,
            angle, start_angle, center, val, i, metadata, half_pie, end_angle,
            max_value):
        """Draw a solid gauge slice and background slice"""
        if angle == 2 * pi:
            angle = nearly_2pi

        if angle > 0:
            to = [coord_abs_project(center, radius, start_angle),
                  coord_abs_project(center, radius, start_angle + angle),
                  coord_abs_project(center, small_radius, start_angle + angle),
                  coord_abs_project(center, small_radius, start_angle)]

            self.node(
                node, 'path',
                d='M%s A%s 0 %d 1 %s L%s A%s 0 %d 0 %s z' % (
                    to[0],
                    coord_dual(radius),
                    int(angle > pi),
                    to[1],
                    to[2],
                    coord_dual(small_radius),
                    int(angle > pi),
                    to[3]),
                class_='slice reactive tooltip-trigger')
        else:
            return

        x, y = coord_diff(center, coord_project(
            (radius + small_radius) / 2, start_angle + angle / 2))
        self.graph._static_value(serie_node, val, x, y, metadata, 'middle')
        self.graph._tooltip_data(
            node, val, x, y, "centered",
            self.graph._x_labels and self.graph._x_labels[i][0])

    def confidence_interval(self, node, x, low, high, width=7):
        if self.graph.horizontal:
            fmt = lambda xy: '%f %f' % (xy[1], xy[0])
        else:
            fmt = coord_format

        shr = lambda xy: (xy[0] + width, xy[1])
        shl = lambda xy: (xy[0] - width, xy[1])

        top = (x, high)
        bottom = (x, low)

        ci = self.node(node, class_="ci")

        self.node(
            ci, 'path', d="M%s L%s M%s L%s M%s L%s L%s M%s L%s" % tuple(
                map(fmt, (
                    top, shr(top), top, shl(top), top,
                    bottom, shr(bottom), bottom, shl(bottom)
                ))
            ), class_='nofill reactive'
        )

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
        """Write the no data text to the svg"""
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

        svg = b''
        if etree.lxml:
            args['pretty_print'] = pretty_print

        if not self.graph.disable_xml_declaration:
            svg = b"<?xml version='1.0' encoding='utf-8'?>\n"

        if not self.graph.disable_xml_declaration:
            svg += b'\n'.join(
                [etree.tostring(
                    pi, **args)
                 for pi in self.processing_instructions]
            )

        svg += etree.tostring(
            self.root, **args)

        if self.graph.disable_xml_declaration or is_unicode:
            svg = svg.decode('utf-8')
        return svg

    def get_strokes(self):
        """Return a css snippet containing all stroke style options"""
        def stroke_dict_to_css(stroke, i=None):
            """Return a css style for the given option"""
            css = ['%s.series%s {\n' % (
                self.id, '.serie-%d' % i if i is not None else '')]
            for key in (
                    'width', 'linejoin', 'linecap',
                    'dasharray', 'dashoffset'):
                if stroke.get(key):
                    css.append('  stroke-%s: %s;\n' % (
                        key, stroke[key]))
            css.append('}')
            return '\n'.join(css)

        css = []
        if self.graph.stroke_style is not None:
            css.append(stroke_dict_to_css(self.graph.stroke_style))
        for serie in self.graph.series:
            if serie.stroke_style is not None:
                css.append(stroke_dict_to_css(serie.stroke_style, serie.index))

        for secondary_serie in self.graph.secondary_series:
            if secondary_serie.stroke_style is not None:
                css.append(stroke_dict_to_css(secondary_serie.stroke_style, secondary_serie.index))
        return '\n'.join(css)
