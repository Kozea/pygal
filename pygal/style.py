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
Charts styling
"""
from __future__ import division
from pygal.util import cycle_fill
from pygal import colors
from pygal.colors import darken, lighten
import sys
import re

re_dasharray_delimiters = re.compile(r'[\.|,|x|\||\- ]+', re.I)

class Style(object):
    """Styling class containing colors for the css generation"""
    def __init__(
            self,
            background='black',
            plot_background='#111',
            foreground='#999',
            foreground_light='#eee',
            foreground_dark='#555',
            font_family='monospace',  # Monospaced font is highly encouraged
            opacity='.8',
            opacity_hover='.9',
            stroke_width='1',
            stroke_style='round',
            stroke_dasharray=(0,0),
            transition='250ms',
            colors=(
                '#ff5995', '#b6e354', '#feed6c', '#8cedff', '#9e6ffe',
                '#899ca1', '#f8f8f2', '#bf4646', '#516083', '#f92672',
                '#82b414', '#fd971f', '#56c2d6', '#808384', '#8c54fe',
                '#465457')):
        self.background = background
        self.plot_background = plot_background
        self.foreground = foreground
        self.foreground_light = foreground_light
        self.foreground_dark = foreground_dark
        self.font_family = font_family
        self.opacity = opacity
        self.opacity_hover = opacity_hover
        self.stroke_width = stroke_width
        self.stroke_style = stroke_style
        self.stroke_dasharray = stroke_dasharray
        self.transition = transition
        self.colors = colors

        self.validate_stroke_values()

    def validate_stroke_values(self):
        # stroke_width
        self.stroke_width = float(self.stroke_width)

        # stroke_style
        self.stroke_style = self.stroke_style.lower().strip()
        if not self.stroke_style in ['round', 'bevel', 'miter']:
            self.stroke_style = 'round'

        # stroke_dasharray
        if isinstance(self.stroke_dasharray, (list, tuple)):
            self.stroke_dasharray = '%d,%d' % self.stroke_dasharray

        if isinstance(self.stroke_dasharray, str):
            self.stroke_dasharray = re.sub(re_dasharray_delimiters, ',', self.stroke_dasharray)

        if not isinstance(self.stroke_dasharray, str):
            raise ValueError('stroke_dasharray not in proper form: tuple(int,int)')


    def get_colors(self, prefix):
        """Get the css color list"""

        def color(tupl):
            """Make a color css"""
            return ((
                '%s.color-{0}, %s.color-{0} a:visited {{\n'
                '  stroke: {1};\n'
                '  fill: {1};\n'
                '}}\n') % (prefix, prefix)).format(*tupl)

        return '\n'.join(map(color, enumerate(
            cycle_fill(self.colors, max(len(self.colors), 16)))))

    def to_dict(self):
        config = {}
        for attr in dir(self):
            if not attr.startswith('__'):
                value = getattr(self, attr)
                if not hasattr(value, '__call__'):
                    config[attr] = value
        return config


DefaultStyle = Style(opacity_hover='.4', opacity='.8')


LightStyle = Style(
    background='white',
    plot_background='rgba(0, 0, 255, 0.1)',
    foreground='rgba(0, 0, 0, 0.7)',
    foreground_light='rgba(0, 0, 0, 0.9)',
    foreground_dark='rgba(0, 0, 0, 0.5)',
    colors=('#242424', '#9f6767', '#92ac68',
            '#d0d293', '#9aacc3', '#bb77a4',
            '#77bbb5', '#777777'))


NeonStyle = Style(
    opacity='.1',
    opacity_hover='.75',
    transition='1s ease-out')


CleanStyle = Style(
    background='transparent',
    plot_background='rgba(240, 240, 240, 0.7)',
    foreground='rgba(0, 0, 0, 0.9)',
    foreground_light='rgba(0, 0, 0, 0.9)',
    foreground_dark='rgba(0, 0, 0, 0.5)',
    colors=(
        'rgb(12,55,149)', 'rgb(117,38,65)', 'rgb(228,127,0)', 'rgb(159,170,0)',
        'rgb(149,12,12)'))


solarized_colors = (
    '#b58900', '#cb4b16', '#dc322f', '#d33682',
    '#6c71c4', '#268bd2', '#2aa198', '#859900')


DarkSolarizedStyle = Style(
    background='#073642',
    plot_background='#002b36',
    foreground='#839496',
    foreground_light='#fdf6e3',
    foreground_dark='#657b83',
    opacity='.66',
    opacity_hover='.9',
    transition='500ms ease-in',
    colors=solarized_colors)


LightSolarizedStyle = Style(
    background='#fdf6e3',
    plot_background='#eee8d5',
    foreground='#657b83',
    foreground_light='#073642',
    foreground_dark='#073642',
    opacity='.6',
    opacity_hover='.9',
    transition='500ms ease-in',
    colors=solarized_colors)


RedBlueStyle = Style(
    background=lighten('#e6e7e9', 7),
    plot_background=lighten('#e6e7e9', 10),
    foreground='rgba(0, 0, 0, 0.9)',
    foreground_light='rgba(0, 0, 0, 0.9)',
    foreground_dark='rgba(0, 0, 0, 0.5)',
    opacity='.6',
    opacity_hover='.9',
    colors=(
        '#d94e4c', '#e5884f', '#39929a',
        lighten('#d94e4c', 10),  darken('#39929a', 15), lighten('#e5884f', 17),
        darken('#d94e4c', 10), '#234547'))


LightColorizedStyle = Style(
    background='#f8f8f8',
    plot_background=lighten('#f8f8f8', 3),
    foreground='#333',
    foreground_light='#666',
    foreground_dark='rgba(0, 0 , 0, 0.5)',
    opacity='.5',
    opacity_hover='.9',
    transition='250ms ease-in',
    colors=(
        '#fe9592', '#534f4c', '#3ac2c0', '#a2a7a1',
        darken('#fe9592', 15), lighten('#534f4c', 15), lighten('#3ac2c0', 15),
        lighten('#a2a7a1', 15), lighten('#fe9592', 15), darken('#3ac2c0', 10)))


DarkColorizedStyle = Style(
    background=darken('#3a2d3f', 5),
    plot_background=lighten('#3a2d3f', 2),
    foreground='rgba(255, 255, 255, 0.9)',
    foreground_light='rgba(255, 255, 255, 0.9)',
    foreground_dark='rgba(255, 255 , 255, 0.5)',
    opacity='.2',
    opacity_hover='.7',
    transition='250ms ease-in',
    colors=(
        '#c900fe', '#01b8fe', '#59f500', '#ff00e4', '#f9fa00',
        darken('#c900fe', 20), darken('#01b8fe', 15), darken('#59f500', 20),
        darken('#ff00e4', 15), lighten('#f9fa00', 20)))


TurquoiseStyle = Style(
    background=darken('#1b8088', 15),
    plot_background=darken('#1b8088', 17),
    foreground='rgba(255, 255, 255, 0.9)',
    foreground_light='rgba(255, 255, 255, 0.9)',
    foreground_dark='rgba(255, 255 , 255, 0.5)',
    opacity='.5',
    opacity_hover='.9',
    transition='250ms ease-in',
    colors=(
        '#93d2d9', '#ef940f', '#8C6243', '#fff',
        darken('#93d2d9', 20),  lighten('#ef940f', 15),
        lighten('#8c6243', 15), '#1b8088'))


LightGreenStyle = Style(
    background=lighten('#f3f3f3', 3),
    plot_background='#fff',
    foreground='#333333',
    foreground_light='#666',
    foreground_dark='#222222',
    opacity='.5',
    opacity_hover='.9',
    transition='250ms ease-in',
    colors=(
        '#7dcf30', '#247fab', lighten('#7dcf30', 10), '#ccc',
        darken('#7dcf30', 15), '#ddd', lighten('#247fab', 10),
        darken('#247fab', 15)))


DarkGreenStyle = Style(
    background=darken('#251e01', 3),
    plot_background=darken('#251e01', 1),
    foreground='rgba(255, 255, 255, 0.9)',
    foreground_light='rgba(255, 255, 255, 0.9)',
    foreground_dark='rgba(255, 255, 255, 0.6)',
    opacity='.6',
    opacity_hover='.9',
    transition='250ms ease-in',
    colors=(
        '#adde09', '#6e8c06', '#4a5e04', '#fcd202', '#C1E34D',
        lighten('#fcd202', 25)))


DarkGreenBlueStyle = Style(
    background='#000',
    plot_background=lighten('#000', 8),
    foreground='rgba(255, 255, 255, 0.9)',
    foreground_light='rgba(255, 255, 255, 0.9)',
    foreground_dark='rgba(255, 255, 255, 0.6)',
    opacity='.55',
    opacity_hover='.9',
    transition='250ms ease-in',
    colors=(lighten('#34B8F7', 15), '#7dcf30', '#247fab',
            darken('#7dcf30', 10), lighten('#247fab', 10),
            lighten('#7dcf30', 10), darken('#247fab', 10), '#fff'))


BlueStyle = Style(
    background=darken('#f8f8f8', 3),
    plot_background='#f8f8f8',
    foreground='rgba(0, 0, 0, 0.9)',
    foreground_light='rgba(0, 0, 0, 0.9)',
    foreground_dark='rgba(0, 0, 0, 0.6)',
    opacity='.5',
    opacity_hover='.9',
    transition='250ms ease-in',
    colors=(
        '#00b2f0', '#43d9be', '#0662ab', darken('#00b2f0', 20),
        lighten('#43d9be', 20), lighten('#7dcf30', 10), darken('#0662ab', 15),
        '#ffd541', '#7dcf30', lighten('#00b2f0', 15), darken('#ffd541', 20)))


SolidColorStyle = Style(
    background='#FFFFFF',
    plot_background='#FFFFFF',
    foreground='#000000',
    foreground_light='#000000',
    foreground_dark='#828282',
    opacity='.8',
    opacity_hover='.9',
    transition='400ms ease-in',
    colors=('#FF9900', '#DC3912', '#4674D1', '#109618', '#990099',
            '#0099C6', '#DD4477', '#74B217', '#B82E2E', '#316395', '#994499'))


styles = {'default': DefaultStyle,
          'light': LightStyle,
          'neon': NeonStyle,
          'clean': CleanStyle,
          'light_red_blue': RedBlueStyle,
          'dark_solarized': DarkSolarizedStyle,
          'light_solarized': LightSolarizedStyle,
          'dark_colorized': DarkColorizedStyle,
          'light_colorized': LightColorizedStyle,
          'turquoise': TurquoiseStyle,
          'green': LightGreenStyle,
          'dark_green': DarkGreenStyle,
          'dark_green_blue': DarkGreenBlueStyle,
          'blue': BlueStyle,
          'solid_color': SolidColorStyle}


parametric_styles = {}
for op in ('lighten', 'darken', 'saturate', 'desaturate', 'rotate'):
    name = op.capitalize() + 'Style'

    def get_style_for(op_name):
        operation = getattr(colors, op_name)

        def parametric_style(color, step=10, max_=None, base_style=None,
                             **kwargs):
            if max_ is None:
                violency = {
                    'darken': 50,
                    'lighten': 50,
                    'saturate': 100,
                    'desaturate': 100,
                    'rotate': 360
                }
                max__ = violency[op_name]
            else:
                max__ = max_

            def modifier(index):
                percent = max__ * index / (step - 1)
                return operation(color, percent)

            colors = list(map(modifier, range(0, max(2, step))))

            if base_style is None:
                return Style(colors=colors, **kwargs)
            opts = dict(base_style.__dict__)
            opts.update({'colors': colors})
            opts.update(kwargs)
            return Style(**opts)

        return parametric_style

    style = get_style_for(op)
    parametric_styles[name] = style
    setattr(sys.modules[__name__], name, style)
