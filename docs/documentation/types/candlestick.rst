Candlestick
-----------

Candlestick charts display financial OHLC data. Each value is a 5-item tuple:
``(x, open, high, low, close)``.

.. pygal-code::

  candlestick = pygal.Candlestick()
  candlestick.title = 'OHLC sample'
  candlestick.add('Price', [
      (1, 10, 15, 8, 12),
      (2, 12, 18, 11, 9),
      (3, 9, 13, 7, 13),
  ])
