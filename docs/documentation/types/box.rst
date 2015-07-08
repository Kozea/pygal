Box
---

Basic
~~~~~

Here's some whiskers:

.. pygal-code::

  box_plot = pygal.Box()
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

and variations:

.. pygal-code::

  box_plot = pygal.Box(box_mode="1.5IQR")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

.. pygal-code::

  box_plot = pygal.Box(box_mode="tukey")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

.. pygal-code::

  box_plot = pygal.Box(box_mode="stdev")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

.. pygal-code::

  box_plot = pygal.Box(box_mode="pstdev")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
