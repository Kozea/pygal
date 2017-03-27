First steps
===========

.. caution::

  First you need to install pygal, see `installing <../installing.html>`_.

When it's done, you are ready to make your first chart:

.. code-block:: python

  import pygal                                                       # First import pygal
  bar_chart = pygal.Bar()                                            # Then create a bar graph object
  bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
  bar_chart.render_to_file('bar_chart.svg')                          # Save the svg to a file

Now you should have a svg file called ``bar_chart.svg`` in your current directory.

You can open it with various programs such as your web browser, inkscape or any svg compatible viewer.


The resulting chart will be tho following:

.. pygal-code::

  bar_chart = pygal.Bar()
  bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])


.. caution::

   pygal relies on svg css styling. This is sadly not fully supported by gnome `librsvg <https://wiki.gnome.org/action/show/Projects/LibRsvg>`_ and therefore can lead to black svg being displayed. This is not a bug in pygal. `See this bugzilla search <https://bugzilla.gnome.org/buglist.cgi?bug_status=__open__&content=css%20style&no_redirect=1&order=Importance&product=librsvg&query_format=specific>`_


To make a multiple series graph just add another one:

.. pygal-code::

  bar_chart = pygal.Bar()
  bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
  bar_chart.add('Padovan', [1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12])

If you want to stack them, use `StackedBar` instead of `Bar`:

.. pygal-code::

  bar_chart = pygal.StackedBar()
  bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
  bar_chart.add('Padovan', [1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12])


You can also make it horizontal with `HorizontalStackedBar`:

.. pygal-code::

  bar_chart = pygal.HorizontalStackedBar()
  bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
  bar_chart.add('Padovan', [1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12])


And finally add a title and some labels:

.. pygal-code::

  bar_chart = pygal.HorizontalStackedBar()
  bar_chart.title = "Remarquable sequences"
  bar_chart.x_labels = map(str, range(11))
  bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
  bar_chart.add('Padovan', [1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12])

The public API is chainable and can be simplified as call arguments, the last chart can be also written:

.. code-block:: python

  bar_chart = pygal.HorizontalStackedBar(
    title="Remarquable sequences", x_labels=map(str, range(11))(
    0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, title='Fibonacci')(
    1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12, title='Padovan')
