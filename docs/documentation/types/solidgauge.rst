SolidGauge
----------

SolidGauge charts

Normal
~~~~~~

.. pygal-code::

    gauge = pygal.SolidGauge(inner_radius=0.70)
    percent_formatter = lambda x: '{:.10g}%'.format(x)
    dollar_formatter = lambda x: '{:.10g}$'.format(x)
    gauge.value_formatter = percent_formatter

    gauge.add('Series 1', [{'value': 225000, 'max_value': 1275000}],
              formatter=dollar_formatter)
    gauge.add('Series 2', [{'value': 110, 'max_value': 100}])
    gauge.add('Series 3', [{'value': 3}])
    gauge.add(
        'Series 4', [
            {'value': 51, 'max_value': 100},
            {'value': 12, 'max_value': 100}])
    gauge.add('Series 5', [{'value': 79, 'max_value': 100}])
    gauge.add('Series 6', 99)
    gauge.add('Series 7', [{'value': 100, 'max_value': 100}])


Half
~~~~

.. pygal-code::

    gauge = pygal.SolidGauge(
        half_pie=True, inner_radius=0.70,
        style=pygal.style.styles['default'](value_font_size=10))

    percent_formatter = lambda x: '{:.10g}%'.format(x)
    dollar_formatter = lambda x: '{:.10g}$'.format(x)
    gauge.value_formatter = percent_formatter

    gauge.add('Series 1', [{'value': 225000, 'max_value': 1275000}],
              formatter=dollar_formatter)
    gauge.add('Series 2', [{'value': 110, 'max_value': 100}])
    gauge.add('Series 3', [{'value': 3}])
    gauge.add(
        'Series 4', [
            {'value': 51, 'max_value': 100},
            {'value': 12, 'max_value': 100}])
    gauge.add('Series 5', [{'value': 79, 'max_value': 100}])
    gauge.add('Series 6', 99)
    gauge.add('Series 7', [{'value': 100, 'max_value': 100}])
