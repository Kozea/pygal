from svg.charts import time_series

def test_field_width():
	"""
	cking reports in a comment on PyPI that the X-axis labels all
	bunch up on the left. This tests confirms the bug and tests for its
	correctness.
	"""
	g = time_series.Plot({})

	g.timescale_divisions = '4 hours'
	g.stagger_x_labels = True
	g.x_label_format = '%d-%b %H:%M'

	g.add_data({'data': ['2005-12-21T00:00:00', 20, '2005-12-22T00:00:00', 21], 'title': 'series 1'})
	g.burn()
	assert g.field_width() > 1
