Histogram
---------

Basic
~~~~~

Histogram are special bars that take 3 values for a bar: the ordinate height, the abscissa start and the abscissa end.


.. pygal-code::

  hist = pygal.Histogram()
  hist.add('Wide bars', [(5, 0, 10), (4, 5, 13), (2, 0, 15)])
  hist.add('Narrow bars',  [(10, 1, 2), (12, 4, 4.5), (8, 11, 13)])
