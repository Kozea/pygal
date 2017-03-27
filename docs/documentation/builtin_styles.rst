Built-in Styles
===============

pygal provides 14 built-in styles:


Default
-------

.. pygal-code::

  from pygal.style import DefaultStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle) # Setting style here is not necessary
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


DarkStyle
---------

.. pygal-code::

  from pygal.style import DarkStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DarkStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Neon
----

.. pygal-code::

  from pygal.style import NeonStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=NeonStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Dark Solarized
--------------

.. pygal-code::

  from pygal.style import DarkSolarizedStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DarkSolarizedStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Light Solarized
---------------

.. pygal-code::

  from pygal.style import LightSolarizedStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=LightSolarizedStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Light
-----

.. pygal-code::

  from pygal.style import LightStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=LightStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Clean
-----

.. pygal-code::

  from pygal.style import CleanStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=CleanStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Red Blue
--------

.. pygal-code::

  from pygal.style import RedBlueStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=RedBlueStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Dark Colorized
--------------

.. pygal-code::

  from pygal.style import DarkColorizedStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DarkColorizedStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Light Colorized
---------------

.. pygal-code::

  from pygal.style import LightColorizedStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=LightColorizedStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Turquoise
---------

.. pygal-code::

  from pygal.style import TurquoiseStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=TurquoiseStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Light green
-----------

.. pygal-code::

  from pygal.style import LightGreenStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=LightGreenStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Dark green
----------

.. pygal-code::

  from pygal.style import DarkGreenStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DarkGreenStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Dark green blue
---------------

.. pygal-code::

  from pygal.style import DarkGreenBlueStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DarkGreenBlueStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Blue
----

.. pygal-code::

  from pygal.style import BlueStyle
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=BlueStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])
