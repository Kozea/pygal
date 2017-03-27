Value configuration
===================

How
---

Values are customized by replacing the value with a dictionary containing the value as 'value':

.. code-block:: python

   chart = pygal.Line()
   chart.add('', [1, {'value': 2, 'label': 'two'}, 3])
   chart.add('', [3, 2, 1])


Labels
------

You can add per value metadata like labels, by specifying a dictionary instead of a value:

.. pygal-code::

  chart = pygal.Bar()
  chart.add('First', [{'value': 2, 'label': 'This is the first'}])
  chart.add('Second', [{'value': 4, 'label': 'This is the second'}])
  chart.add('Third', 7)
  chart.add('Fourth', [{'value': 5}])
  chart.add('Fifth', [{'value': 3, 'label': 'This is the fifth'}])


Style
-----

You can force the color of a value by specifying a color key:

.. pygal-code::

  chart = pygal.Bar()
  chart.add('Serie', [
   {'value': 2}, 3, 4,
   {'value': 10, 'color': 'red'},
   {'value': 11, 'color': 'rgba(255, 45, 20, .6)'}, 4, 2
  ])

The color key set the fill and the stroke style. You can also set the css style manually:

.. pygal-code::

  chart = pygal.Bar()
  chart.add('Serie', [
   {'value': 2}, 3, 4,
   {'value': 10, 'style': 'fill: red; stroke: black; stroke-width: 4'},
   {'value': 11, 'style': 'fill: rgba(255, 45, 20, .6); stroke: black; stroke-dasharray: 15, 10, 5, 10, 15'},
   4, 2
  ])


Value formatting
~~~~~~~~~~~~~~~~

You can add a `formatter` metadata for a specific value.


.. pygal-code::

  chart = pygal.Bar(print_values=True, value_formatter=lambda x: '{}$'.format(x))
  chart.add('bar', [.0002, .0005, .00035], formatter=lambda x: '<%s>' % x)
  chart.add('bar', [.0004, {'value': .0009, 'formatter': lambda x: '«%s»' % x}, .001])


Node attributes
---------------

It is possible to pass svg attribute to the node representing value.

.. pygal-code::

  chart = pygal.Line()
  chart.add('Serie', [
    {'value': 1, 'node': {'r': 2}},
    {'value': 2, 'node': {'r': 4}},
    {'value': 3, 'node': {'r': 6}},
    {'value': 4, 'node': {'r': 8}}
  ])


Links
-----

Basic
~~~~~

You can also add hyper links:

.. pygal-code::

  chart = pygal.Bar()
  chart.add('First', [{
    'value': 2,
    'label': 'This is the first',
    'xlink': 'http://en.wikipedia.org/wiki/First'}])

  chart.add('Second', [{
    'value': 4,
    'label': 'This is the second',
    'xlink': 'http://en.wikipedia.org/wiki/Second'}])

  chart.add('Third', 7)

  chart.add('Fourth', [{
    'value': 5,
    'xlink': 'http://en.wikipedia.org/wiki/Fourth'}])

  chart.add('Fifth', [{
    'value': 3,
    'label': 'This is the fifth',
    'xlink': 'http://en.wikipedia.org/wiki/Fifth'}])


Advanced
~~~~~~~~

You can specify a dictionary to xlink with all links attributes:

.. pygal-code::

  chart = pygal.Bar()
  chart.add('First', [{
    'value': 2,
    'label': 'This is the first',
    'xlink': {'href': 'http://en.wikipedia.org/wiki/First'}}])

  chart.add('Second', [{
    'value': 4,
    'label': 'This is the second',
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Second',
      'target': '_top'}
    }])

  chart.add('Third', 7)

  chart.add('Fourth', [{
    'value': 5,
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Fourth',
      'target': '_blank'}
    }])

  chart.add('Fifth', [{
    'value': 3,
    'label': 'This is the fifth',
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Fifth',
      'target': '_self'}
    }])

Legend
~~~~~~

Finally legends can be link with the same mechanism:


.. pygal-code::

  chart = pygal.Bar()
  chart.add({
    'title': 'First',
    'tooltip': 'It is the first actually',
    'xlink': {'href': 'http://en.wikipedia.org/wiki/First'}
  }, [{
    'value': 2,
    'label': 'This is the first',
    'xlink': {'href': 'http://en.wikipedia.org/wiki/First'}
  }])

  chart.add({
    'title': 'Second',
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Second',
      'target': '_top'
    }
  }, [{
    'value': 4,
    'label': 'This is the second',
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Second',
      'target': '_top'}
  }])

  chart.add('Third', 7)

  chart.add({
    'title': 'Fourth',
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Fourth',
      'target': '_blank'
    }
  }, [{
    'value': 5,
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Fourth',
      'target': '_blank'}
  }])

  chart.add({
    'title': 'Fifth',
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Fifth',
      'target': '_self'
    }
  }, [{
    'value': 3,
    'label': 'This is the fifth',
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Fifth',
      'target': '_self'}
  }])


Confidence Intervals
~~~~~~~~~~~~~~~~~~~~

.. pygal-code::

  chart = pygal.Bar(style=pygal.style.styles['default'](ci_colors=(
    'black', 'blue')))
  chart.add('First', [{'value': 2, 'ci': {
    'type': 'continuous', 'sample_size': 50, 'stddev': .5, 'confidence': .95}}])
  chart.add('Second', [{'value': 4, 'ci': {'low': 2, 'high': 5}}])
  chart.add('Third', 7)
  chart.add('Fourth', [{'value': 5}])
  chart.add('Fifth', [{'value': 3, 'ci': {
    'type': 'dichotomous', 'sample_size': 1000}}])
