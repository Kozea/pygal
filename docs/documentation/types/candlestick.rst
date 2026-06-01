Candlestick
===========

Candlestick charts display open-high-low-close values, typically used for
financial prices.

Candles accept five values: x, open, high, low, close.

.. pygal-code::

  candlestick = pygal.Candlestick()
  candlestick.title = 'OHLC prices'
  candlestick.add('Price', [
      (1, 10, 15, 8, 14),
      (2, 14, 16, 11, 12),
      (3, 12, 18, 10, 12),
  ])

Four-value tuples are also supported and use the value index as x.
