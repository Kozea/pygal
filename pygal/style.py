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
"""Charts styling classes"""

from __future__ import division

from itertools import chain

from pygal import colors
from pygal.colors import darken, is_foreground_light, lighten


class Style(object):

    """Styling class containing colors for the css generation"""

    plot_background = 'rgba(255, 255, 255, 1)'
    background = 'rgba(249, 249, 249, 1)'
    value_background = 'rgba(229, 229, 229, 1)'
    foreground = 'rgba(0, 0, 0, .87)'
    foreground_strong = 'rgba(0, 0, 0, 1)'
    foreground_subtle = 'rgba(0, 0, 0, .54)'

    # Monospaced font is highly encouraged
    font_family = (
        'Consolas, "Liberation Mono", Menlo, Courier, monospace')

    label_font_family = None
    major_label_font_family = None
    value_font_family = None
    value_label_font_family = None
    tooltip_font_family = None
    title_font_family = None
    legend_font_family = None
    no_data_font_family = None

    label_font_size = 10
    major_label_font_size = 10
    value_font_size = 16
    value_label_font_size = 10
    tooltip_font_size = 14
    title_font_size = 16
    legend_font_size = 14
    no_data_font_size = 64

    # Guide line dash array style
    guide_stroke_dasharray = '4,4'
    major_guide_stroke_dasharray = '6,6'

    opacity = '.7'
    opacity_hover = '.8'

    stroke_opacity = '.8'
    stroke_opacity_hover = '.9'

    transition = '150ms'
    colors = (
        '#F44336',  # 0
        '#3F51B5',  # 4
        '#009688',  # 8
        '#FFC107',  # 13
        '#FF5722',  # 15
        '#9C27B0',  # 2
        '#03A9F4',  # 6
        '#8BC34A',  # 10
        '#FF9800',  # 14
        '#E91E63',  # 1
        '#2196F3',  # 5
        '#4CAF50',  # 9
        '#FFEB3B',  # 12
        '#673AB7',  # 3
        '#00BCD4',  # 7
        '#CDDC39',  # 11b
        '#9E9E9E',  # 17
        '#607D8B',  # 18
    )

    value_colors = ()
    ci_colors = ()

    def __init__(self, **kwargs):
        """Create the style"""
        self.__dict__.update(kwargs)
        self._google_fonts = set()
        if self.font_family.startswith('googlefont:'):
            self.font_family = self.font_family.replace('googlefont:', '')
            self._google_fonts.add(self.font_family.split(',')[0].strip())

        for name in dir(self):
            if name.endswith('_font_family'):
                fn = getattr(self, name)
                if fn is None:
                    setattr(self, name, self.font_family)
                elif fn.startswith('googlefont:'):
                    setattr(self, name, fn.replace('googlefont:', ''))
                    self._google_fonts.add(
                        getattr(self, name).split(',')[0].strip())

    def get_colors(self, prefix, len_):
        """Get the css color list"""
        def color(tupl):
            """Make a color css"""
            return ((
                '%s.color-{0}, %s.color-{0} a:visited {{\n'
                '  stroke: {1};\n'
                '  fill: {1};\n'
                '}}\n') % (prefix, prefix)).format(*tupl)

        def value_color(tupl):
            """Make a value color css"""
            return ((
                '%s .text-overlay .color-{0} text {{\n'
                '  fill: {1};\n'
                '}}\n') % (prefix,)).format(*tupl)

        def ci_color(tupl):
            """Make a value color css"""
            if not tupl[1]:
                return ''
            return ((
                '%s .color-{0} .ci {{\n'
                '  stroke: {1};\n'
                '}}\n') % (prefix,)).format(*tupl)

        if len(self.colors) < len_:
            missing = len_ - len(self.colors)
            cycles = 1 + missing // len(self.colors)
            colors = []
            for i in range(0, cycles + 1):
                for color_ in self.colors:
                    colors.append(darken(color_, 33 * i / cycles))
                    if len(colors) >= len_:
                        break
                else:
                    continue
                break
        else:
            colors = self.colors[:len_]

        # Auto compute foreground value color when color is missing
        value_colors = []
        for i in range(len_):
            if i < len(self.value_colors) and self.value_colors[i] is not None:
                value_colors.append(self.value_colors[i])
            else:
                value_colors.append('white' if is_foreground_light(
                    colors[i]) else 'black')

        return '\n'.join(chain(
            map(color, enumerate(colors)),
            map(value_color, enumerate(value_colors)),
            map(ci_color, enumerate(self.ci_colors))))

    def to_dict(self):
        """Convert instance to a serializable mapping."""
        config = {}
        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if not hasattr(value, '__call__'):
                    config[attr] = value
        return config


DefaultStyle = Style


class DarkStyle(Style):

    """A dark style (old default)"""

    background = 'black'
    plot_background = '#111'
    foreground = '#999'
    foreground_strong = '#eee'
    foreground_subtle = '#555'
    opacity = '.8'
    opacity_hover = '.4'
    transition = '250ms'
    colors = (
        '#ff5995', '#b6e354', '#feed6c', '#8cedff', '#9e6ffe',
        '#899ca1', '#f8f8f2', '#bf4646', '#516083', '#f92672',
        '#82b414', '#fd971f', '#56c2d6', '#808384', '#8c54fe',
        '#465457')


class LightStyle(Style):

    """A light style"""

    background = 'white'
    plot_background = 'rgba(0, 0, 255, 0.1)'
    foreground = 'rgba(0, 0, 0, 0.7)'
    foreground_strong = 'rgba(0, 0, 0, 0.9)'
    foreground_subtle = 'rgba(0, 0, 0, 0.5)'
    colors = ('#242424', '#9f6767', '#92ac68',
              '#d0d293', '#9aacc3', '#bb77a4',
              '#77bbb5', '#777777')


class NeonStyle(DarkStyle):

    """Similar to DarkStyle but with more opacity and effects"""

    opacity = '.1'
    opacity_hover = '.75'
    transition = '1s ease-out'


class CleanStyle(Style):

    """A rather clean style"""

    background = 'transparent'
    plot_background = 'rgba(240, 240, 240, 0.7)'
    foreground = 'rgba(0, 0, 0, 0.9)'
    foreground_strong = 'rgba(0, 0, 0, 0.9)'
    foreground_subtle = 'rgba(0, 0, 0, 0.5)'
    colors = (
        'rgb(12,55,149)', 'rgb(117,38,65)', 'rgb(228,127,0)', 'rgb(159,170,0)',
        'rgb(149,12,12)')


class DarkSolarizedStyle(Style):

    """Dark solarized popular theme"""

    background = '#073642'
    plot_background = '#002b36'
    foreground = '#839496'
    foreground_strong = '#fdf6e3'
    foreground_subtle = '#657b83'
    opacity = '.66'
    opacity_hover = '.9'
    transition = '500ms ease-in'
    colors = (
        '#b58900', '#cb4b16', '#dc322f', '#d33682',
        '#6c71c4', '#268bd2', '#2aa198', '#859900')


class LightSolarizedStyle(DarkSolarizedStyle):

    """Light solarized popular theme"""

    background = '#fdf6e3'
    plot_background = '#eee8d5'
    foreground = '#657b83'
    foreground_strong = '#073642'
    foreground_subtle = '#073642'


class RedBlueStyle(Style):

    """A red and blue theme"""

    background = lighten('#e6e7e9', 7)
    plot_background = lighten('#e6e7e9', 10)
    foreground = 'rgba(0, 0, 0, 0.9)'
    foreground_strong = 'rgba(0, 0, 0, 0.9)'
    foreground_subtle = 'rgba(0, 0, 0, 0.5)'
    opacity = '.6'
    opacity_hover = '.9'
    colors = (
        '#d94e4c', '#e5884f', '#39929a',
        lighten('#d94e4c', 10), darken('#39929a', 15), lighten('#e5884f', 17),
        darken('#d94e4c', 10), '#234547')


class LightColorizedStyle(Style):

    """A light colorized style"""

    background = '#f8f8f8'
    plot_background = lighten('#f8f8f8', 3)
    foreground = '#333'
    foreground_strong = '#666'
    foreground_subtle = 'rgba(0, 0 , 0, 0.5)'
    opacity = '.5'
    opacity_hover = '.9'
    transition = '250ms ease-in'
    colors = (
        '#fe9592', '#534f4c', '#3ac2c0', '#a2a7a1',
        darken('#fe9592', 15), lighten('#534f4c', 15), lighten('#3ac2c0', 15),
        lighten('#a2a7a1', 15), lighten('#fe9592', 15), darken('#3ac2c0', 10))


class DarkColorizedStyle(Style):

    """A dark colorized style"""

    background = darken('#3a2d3f', 5)
    plot_background = lighten('#3a2d3f', 2)
    foreground = 'rgba(255, 255, 255, 0.9)'
    foreground_strong = 'rgba(255, 255, 255, 0.9)'
    foreground_subtle = 'rgba(255, 255 , 255, 0.5)'
    opacity = '.2'
    opacity_hover = '.7'
    transition = '250ms ease-in'
    colors = (
        '#c900fe', '#01b8fe', '#59f500', '#ff00e4', '#f9fa00',
        darken('#c900fe', 20), darken('#01b8fe', 15), darken('#59f500', 20),
        darken('#ff00e4', 15), lighten('#f9fa00', 20))


class TurquoiseStyle(Style):

    """A turquoise style"""

    background = darken('#1b8088', 15)
    plot_background = darken('#1b8088', 17)
    foreground = 'rgba(255, 255, 255, 0.9)'
    foreground_strong = 'rgba(255, 255, 255, 0.9)'
    foreground_subtle = 'rgba(255, 255 , 255, 0.5)'
    opacity = '.5'
    opacity_hover = '.9'
    transition = '250ms ease-in'
    colors = (
        '#93d2d9', '#ef940f', '#8C6243', '#fff',
        darken('#93d2d9', 20), lighten('#ef940f', 15),
        lighten('#8c6243', 15), '#1b8088')


class LightGreenStyle(Style):

    """A light green style"""

    background = lighten('#f3f3f3', 3)
    plot_background = '#fff'
    foreground = '#333333'
    foreground_strong = '#666'
    foreground_subtle = '#222222'
    opacity = '.5'
    opacity_hover = '.9'
    transition = '250ms ease-in'
    colors = (
        '#7dcf30', '#247fab', lighten('#7dcf30', 10), '#ccc',
        darken('#7dcf30', 15), '#ddd', lighten('#247fab', 10),
        darken('#247fab', 15))


class DarkGreenStyle(Style):

    """A dark green style"""

    background = darken('#251e01', 3)
    plot_background = darken('#251e01', 1)
    foreground = 'rgba(255, 255, 255, 0.9)'
    foreground_strong = 'rgba(255, 255, 255, 0.9)'
    foreground_subtle = 'rgba(255, 255, 255, 0.6)'
    opacity = '.6'
    opacity_hover = '.9'
    transition = '250ms ease-in'
    colors = (
        '#adde09', '#6e8c06', '#4a5e04', '#fcd202', '#C1E34D',
        lighten('#fcd202', 25))


class DarkGreenBlueStyle(Style):

    """A dark green and blue style"""

    background = '#000'
    plot_background = lighten('#000', 8)
    foreground = 'rgba(255, 255, 255, 0.9)'
    foreground_strong = 'rgba(255, 255, 255, 0.9)'
    foreground_subtle = 'rgba(255, 255, 255, 0.6)'
    opacity = '.55'
    opacity_hover = '.9'
    transition = '250ms ease-in'
    colors = (lighten('#34B8F7', 15), '#7dcf30', '#247fab',
              darken('#7dcf30', 10), lighten('#247fab', 10),
              lighten('#7dcf30', 10), darken('#247fab', 10), '#fff')


class BlueStyle(Style):

    """A blue style"""

    background = darken('#f8f8f8', 3)
    plot_background = '#f8f8f8'
    foreground = 'rgba(0, 0, 0, 0.9)'
    foreground_strong = 'rgba(0, 0, 0, 0.9)'
    foreground_subtle = 'rgba(0, 0, 0, 0.6)'
    opacity = '.5'
    opacity_hover = '.9'
    transition = '250ms ease-in'
    colors = (
        '#00b2f0', '#43d9be', '#0662ab', darken('#00b2f0', 20),
        lighten('#43d9be', 20), lighten('#7dcf30', 10), darken('#0662ab', 15),
        '#ffd541', '#7dcf30', lighten('#00b2f0', 15), darken('#ffd541', 20))


class SolidColorStyle(Style):

    """A light style with strong colors"""

    background = '#FFFFFF'
    plot_background = '#FFFFFF'
    foreground = '#000000'
    foreground_strong = '#000000'
    foreground_subtle = '#828282'
    opacity = '.8'
    opacity_hover = '.9'
    transition = '400ms ease-in'
    colors = (
        '#FF9900', '#DC3912', '#4674D1', '#109618', '#990099',
        '#0099C6', '#DD4477', '#74B217', '#B82E2E', '#316395', '#994499')


styles = {'default': DefaultStyle,
          'dark': DarkStyle,
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


class ParametricStyleBase(Style):

    """Parametric Style base class for all the parametric operations"""

    _op = None

    def __init__(self, color, step=10, max_=None, base_style=None, **kwargs):
        """
        Initialization of the parametric style.

        This takes several parameters:
          * a `step` which correspond on how many colors will be needed
          * a `max_` which defines the maximum amplitude of the color effect
          * a `base_style` which will be taken as default for everything
            except colors
          * any keyword arguments setting other style parameters
        """

        if self._op is None:
            raise RuntimeError('ParametricStyle is not instanciable')

        defaults = {}
        if base_style is not None:
            if isinstance(base_style, type):
                base_style = base_style()
            defaults.update(base_style.to_dict())
        defaults.update(kwargs)

        super(ParametricStyleBase, self).__init__(**defaults)

        if max_ is None:
            violency = {
                'darken': 50,
                'lighten': 50,
                'saturate': 100,
                'desaturate': 100,
                'rotate': 360
            }
            max_ = violency[self._op]

        def modifier(index):
            percent = max_ * index / (step - 1)
            return getattr(colors, self._op)(color, percent)

        self.colors = list(map(modifier, range(0, max(2, step))))


class LightenStyle(ParametricStyleBase):

    """Create a style by lightening the given color"""

    _op = 'lighten'


class DarkenStyle(ParametricStyleBase):

    """Create a style by darkening the given color"""

    _op = 'darken'


class SaturateStyle(ParametricStyleBase):

    """Create a style by saturating the given color"""

    _op = 'saturate'


class DesaturateStyle(ParametricStyleBase):

    """Create a style by desaturating the given color"""

    _op = 'desaturate'


class RotateStyle(ParametricStyleBase):

    """Create a style by rotating the given color"""

    _op = 'rotate'


parametric_styles = {
    'lighten': LightenStyle,
    'darken': DarkenStyle,
    'saturate': SaturateStyle,
    'desaturate': DesaturateStyle,
    'rotate': RotateStyle
}
