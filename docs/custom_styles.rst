===============
 Documentation
===============


Custom Styles
=============

pygal provides 2 ways to customize styles:

.. contents::


Using Style class
-----------------

You can instantiate the `Style` class with some customizations for quick styling:

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
------------------

You can also specify a file containing a custom css for more customization. The css option is an array containing included css by default (except from ``base.css`` which is always included).

It supports local file names and external stylesheet too, just append your URI in the list.

(See the `default css <https://github.com/Kozea/pygal/blob/master/pygal/css/>`_)

NB: Now the css rules are prefixed by an unique id, to prevent collisions when including several svg dirctly into a web page. You can disable it with the `no_prefix` option.


.. pygal-code::

  from tempfile import NamedTemporaryFile
  custom_css = '''
    {{ id }}text {
      fill: green;
      font-family: monospace;
    }
    {{ id }}.legends .legend text {
      font-size: {{ font_sizes.legend }};
    }
    {{ id }}.axis {
      stroke: #666;
    }
    {{ id }}.axis text {
      font-size: {{ font_sizes.label }};
      font-family: sans;
      stroke: none;
    }
    {{ id }}.axis.y text {
      text-anchor: end;
    }
    {{ id }}#tooltip text {
      font-size: {{ font_sizes.tooltip }};
    }
    {{ id }}.dot {
      fill: yellow;
    }
    {{ id }}.color-0 {
      stroke: #ff1100;
      fill: #ff1100;
    }
    {{ id }}.color-1 {
      stroke: #ffee00;
      fill: #ffee00;
    }
    {{ id }}.color-2 {
      stroke: #66bb44;
      fill: #66bb44;
    }
    {{ id }}.color-3 {
      stroke: #88bbdd;
      fill: #88bbdd;
    }
    {{ id }}.color-4 {
      stroke: #0000ff;
      fill: #0000ff;
    }
  '''
  custom_css_file = '/tmp/pygal_custom_style.css'
  with open(custom_css_file, 'w') as f:
    f.write(custom_css)
  config = pygal.Config(fill=True, interpolate='cubic')
  config.css.append(custom_css_file)
  chart = pygal.StackedLine(config)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])


Next: `Basic customizations </basic_customizations>`_

