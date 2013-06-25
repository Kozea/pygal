===============
 Documentation
===============


Metadata
========

.. contents::


Labels
------

You can add per value metadata like labels, by specifying a dictionary instead of a value:

.. pygal-code::

  chart = pygal.Bar()
  chart.add('Red', [{'value': 2, 'label': 'This is red'}])
  chart.add('Green', [{'value': 4, 'label': 'This is green'}])
  chart.add('Yellow', 7)
  chart.add('Blue', [{'value': 5}])
  chart.add('Violet', [{'value': 3, 'label': 'This is violet'}])


Links
-----

Basic
~~~~~

You can also add hyper links:

.. pygal-code::

  chart = pygal.Bar()
  chart.add('Red', [{
    'value': 2,
    'label': 'This is red',
    'xlink': 'http://en.wikipedia.org/wiki/Red'}])

  chart.add('Green', [{
    'value': 4,
    'label': 'This is green',
    'xlink': 'http://en.wikipedia.org/wiki/Green'}])

  chart.add('Yellow', 7)

  chart.add('Blue', [{
    'value': 5,
    'xlink': 'http://en.wikipedia.org/wiki/Blue'}])

  chart.add('Violet', [{
    'value': 3,
    'label': 'This is violet',
    'xlink': 'http://en.wikipedia.org/wiki/Violet_(color)'}])


Advanced
~~~~~~~~

You can specify a dictionary to xlink with all links attributes:

.. pygal-code::

  chart = pygal.Bar()
  chart.add('Red', [{
    'value': 2,
    'label': 'This is red',
    'xlink': {'href': 'http://en.wikipedia.org/wiki/Red'}}])

  chart.add('Green', [{
    'value': 4,
    'label': 'This is green',
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Green',
      'target': '_top'}
    }])

  chart.add('Yellow', 7)

  chart.add('Blue', [{
    'value': 5,
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Blue',
      'target': '_blank'}
    }])

  chart.add('Violet', [{
    'value': 3,
    'label': 'This is violet',
    'xlink': {
      'href': 'http://en.wikipedia.org/wiki/Violet_(color)',
      'target': '_self'}
    }])


Next: `Other customizations </other_customizations>`_
