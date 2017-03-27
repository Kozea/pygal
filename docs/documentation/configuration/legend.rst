Legend
======

show_legend
-----------

You can remove legend by setting this to ``False``

.. pygal-code::

  chart = pygal.Line(show_legend=False)
  chart.add('Serie 1', [1, 2, 3])
  chart.add('Serie 2', [4, 2, 0])
  chart.add('Serie 3', [1, -1, 1])
  chart.add('Serie 4', [3, 1, 5])


legend_at_bottom
----------------

You can put legend at bottom by setting ``legend_at_bottom`` to True:

.. pygal-code::

  chart = pygal.Line(legend_at_bottom=True)
  chart.add('Serie 1', [1, 2, 3])
  chart.add('Serie 2', [4, 2, 0])
  chart.add('Serie 3', [1, -1, 1])
  chart.add('Serie 4', [3, 1, 5])


legend_at_bottom_columns
------------------------

Force the number of legend columns when set at bottom

.. pygal-code::

  chart = pygal.Line(legend_at_bottom=True, legend_at_bottom_columns=4)
  chart.add('Serie 1', [1, 2, 3])
  chart.add('Serie 2', [4, 2, 0])
  chart.add('Serie 3', [1, -1, 1])
  chart.add('Serie 4', [3, 1, 5])


legend_box_size
---------------

.. pygal-code::

  chart = pygal.Line(legend_box_size=18)
  chart.add('Serie 1', [1, 2, 3])
  chart.add('Serie 2', [4, 2, 0])
  chart.add('Serie 3', [1, -1, 1])
  chart.add('Serie 4', [3, 1, 5])


truncate_legend
---------------

By default long legends are automatically truncated at reasonable length to fit in the graph.

You can override that by setting truncation lenght with ``truncate_legend``.


.. pygal-code::

  chart = pygal.Line(truncate_legend=17)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])

or disable it by setting this to -1

.. pygal-code::

  chart = pygal.Line(truncate_legend=-1)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])

