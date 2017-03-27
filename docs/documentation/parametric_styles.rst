Parametric Styles
=================

pygal provides 5 parametric styles:


Usage
-----

A parametric style is initiated with a default color and the other are generated from this one:

.. pygal-code::

  from pygal.style import LightenStyle
  dark_lighten_style = LightenStyle('#336676')
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=dark_lighten_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


You can set the `step` parameter to tell between how much colors the color modifier will be applied

.. pygal-code::

  from pygal.style import LightenStyle
  dark_lighten_style = LightenStyle('#336676', step=5)
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=dark_lighten_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])

and the `max_` to limit the amplitude at a certain value (in % for all color operation except rotate which is 360):

.. pygal-code::

  from pygal.style import LightenStyle
  dark_lighten_style = LightenStyle('#336676', step=5, max_=10)
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=dark_lighten_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


You can tell the style to inheritate all the styles from another theme:

.. pygal-code::

  from pygal.style import LightenStyle, LightColorizedStyle
  dark_lighten_style = LightenStyle('#336676', base_style=LightColorizedStyle)
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=dark_lighten_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


And you can manually set the properties just like any other theme:

.. pygal-code::

  from pygal.style import LightenStyle, LightColorizedStyle
  dark_lighten_style = LightenStyle('#336676', base_style=LightColorizedStyle)
  dark_lighten_style.background = '#ffcccc'
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=dark_lighten_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Styles
------


Rotate
~~~~~~

.. pygal-code::

  from pygal.style import RotateStyle
  dark_rotate_style = RotateStyle('#9e6ffe')
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=dark_rotate_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])

.. pygal-code::

  from pygal.style import RotateStyle, LightColorizedStyle
  dark_rotate_style = RotateStyle('#75ff98', base_style=LightColorizedStyle)
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=dark_rotate_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Lighten
~~~~~~~

.. pygal-code::

  from pygal.style import LightenStyle
  dark_lighten_style = LightenStyle('#004466')
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=dark_lighten_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Darken
~~~~~~

.. pygal-code::

  from pygal.style import DarkenStyle
  darken_style = DarkenStyle('#ff8723')
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=darken_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Saturate
~~~~~~~~

.. pygal-code::

  from pygal.style import SaturateStyle
  saturate_style = SaturateStyle('#609f86')
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=saturate_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Desaturate
~~~~~~~~~~

.. pygal-code::

  from pygal.style import DesaturateStyle
  desaturate_style = DesaturateStyle('#8322dd', step=8)
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=desaturate_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])
