Treemap
-------

Basic
~~~~~

Treemap:

.. pygal-code::

  treemap = pygal.Treemap()
  treemap.title = 'Binary TreeMap'
  treemap.add('A', [2, 1, 12, 4, 2, 1, 1, 3, 12, 3, 4, None, 9])
  treemap.add('B', [4, 2, 5, 10, 3, 4, 2, 7, 4, -10, None, 8, 3, 1])
  treemap.add('C', [3, 8, 3, 3, 5, 3, 3, 5, 4, 12])
  treemap.add('D', [23, 18])
  treemap.add('E', [1, 2, 1, 2, 3, 3, 1, 2, 3,
        4, 3, 1, 2, 1, 1, 1, 1, 1])
  treemap.add('F', [31])
  treemap.add('G', [5, 9.3, 8.1, 12, 4, 3, 2])
  treemap.add('H', [12, 3, 3])
