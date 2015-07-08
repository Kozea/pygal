Serie configuration
===================

How
---

Series are customized using keyword args set in the ``add`` function:

.. code-block:: python

   chart = pygal.Line()
   chart.add([1, 2, 3], fill=True)
   chart.add([3, 2, 1], dot=False)


Options
-------


secondary
~~~~~~~~~

You can plot your values to 2 separate axes, thanks to `wiktorn <https://github.com/wiktorn>`_

.. pygal-code::

  chart = pygal.Line(title=u'Some different points')
  chart.add('line', [.0002, .0005, .00035])
  chart.add('other line', [1000, 2000, 7000], secondary=True)
