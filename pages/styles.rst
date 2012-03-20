===============
 Documentation
===============


Styles
======

pygal provides 6 different styles and 2 ways to add your own:

.. contents::


Default
-------

.. pygal-code::

  chart = pygal.StackedLine(fill=True, interpolate='cubic')
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


Custom
------

You can customize styles in two ways:

Using Style class
^^^^^^^^^^^^^^^^^

You can instantiate the Style class with some customizations for quick styling:

.. pygal-code::

  from pygal.style import Style
  custom_style = Style(
    background='transparent',
    plot_background='transparent',
    foreground='#53E89B',
    foreground_light='#53A0E8',
    foreground_dark='#630C0D',
    opacity='.6',
    opacity_hover='.9',
    transition='400ms ease-in',
    colors=('#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53'))

  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=custom_style)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Using a custom css
^^^^^^^^^^^^^^^^^^

You can also specify a file containing a custom css for more customization.
(See the `default css <https://github.com/Kozea/pygal/blob/master/pygal/css/graph.css>`_)

.. pygal-code::

  from tempfile import NamedTemporaryFile
  custom_css = '''
    text {
      fill: green;
      font-family: monospace;
    }
    .legends .legend text {
      font-size: {{ font_sizes.legend }};
    }
    .axis {
      stroke: #666;
    }
    .axis text {
      font-size: {{ font_sizes.label }};
      font-family: sans;
      stroke: none;
    }
    .axis.y text {
      text-anchor: end;
    }
    #tooltip text {
      font-size: {{ font_sizes.tooltip }};
    }
    .dot {
      fill: yellow;
    }
    .color-0 {
      stroke: #ff1100;
      fill: #ff1100;
    }
    .color-1 {
      stroke: #ffee00;
      fill: #ffee00;
    }
    .color-2 {
      stroke: #66bb44;
      fill: #66bb44;
    }
    .color-3 {
      stroke: #88bbdd;
      fill: #88bbdd;
    }
    .color-4 {
      stroke: #0000ff;
      fill: #0000ff;
    }
  '''
  custom_css_file = '/tmp/pygal_custom_style.css'
  with open(custom_css_file, 'w') as f:
    f.write(custom_css)
  chart = pygal.StackedLine(fill=True, interpolate='cubic', base_css=custom_css_file)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])
