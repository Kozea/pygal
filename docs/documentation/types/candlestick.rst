Candlestick
===========

Candlestick charts display open-high-low-close (OHLC) data, commonly used for
financial market prices.

Each value is a tuple in the form ``(open, high, low, close)``:

.. pygal-code::

  candlestick_chart = pygal.Candlestick()
  candlestick_chart.title = 'OHLC sample'
  candlestick_chart.x_labels = ['Mon', 'Tue', 'Wed', 'Thu']
  candlestick_chart.add('AAPL', [
      (10, 15, 8, 12),
      (12, 18, 10, 11),
      (11, 14, 9, 14),
      (14, 16, 12, 13),
  ])
  candlestick_chart.render()

Missing values can be represented with ``None`` and are rendered as gaps.
Single numeric values are also accepted and are rendered as doji candles.
