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


class Style(object):
    def __init__(self,
        background='black',
        plot_background='#111',
        foreground='#999',
        foreground_light='#eee',
        foreground_dark='#555',
        opacity='.8',
        opacity_hover='1',
        transition='250ms',
        colors=(
                '#ff5995', '#b6e354', '#feed6c', '#8cedff', '#9e6ffe',
                '#899ca1', '#f8f8f2', '#808384', '#bf4646', '#516083',
                '#f92672', '#82b414', '#fd971f', '#56c2d6', '#8c54fe',
                '#465457')):
            self.background = background
            self.plot_background = plot_background
            self.foreground = foreground
            self.foreground_light = foreground_light
            self.foreground_dark = foreground_dark
            self.opacity = opacity
            self.opacity_hover = opacity_hover
            self.transition = transition
            self._colors = colors

    @property
    def colors(self):
        def color(tupl):
            return (
                    '.color-{0} {{\n'
                    '  stroke: {1};\n'
                    '  fill: {1};\n'
                    '}}\n'.format(*tupl))
        return '\n'.join(map(color, enumerate(self._colors)))

DefaultStyle = Style()
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

styles = {'default': DefaultStyle,
          'light': LightStyle,
          'neon': NeonStyle}
