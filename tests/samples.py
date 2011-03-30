"""
Samples of the various charts. Run this script to generate the reference
samples.
"""
import sys, os

from svg.charts.plot import Plot
from svg.charts import bar
from svg.charts import time_series
from svg.charts import pie
from svg.charts import schedule

def sample_Plot():
	g = Plot({
		'min_x_value': 0,
		'min_y_value': 0,
		'area_fill': True,
		'stagger_x_labels': True,
		'stagger_y_labels': True,
		'show_x_guidelines': True
	   })
	g.add_data({'data': [1, 25, 2, 30, 3, 45], 'title': 'series 1'})
	g.add_data({'data': [1,30, 2, 31, 3, 40], 'title': 'series 2'})
	g.add_data({'data': [.5,35, 1, 20, 3, 10.5], 'title': 'series 3'})
	return g

def sample_TimeSeries():
	g = time_series.Plot({})

	g.timescale_divisions = '4 hours'
	g.stagger_x_labels = True
	g.x_label_format = '%d-%b %H:%M'
	#g.max_y_value = 200

	g.add_data({'data': ['2005-12-21T00:00:00', 20, '2005-12-22T00:00:00', 21], 'title': 'series 1'})

	return g

def generate_samples():
	yield 'Plot', sample_Plot()
	yield 'TimeSeries', sample_TimeSeries()
	yield 'VerticalBar', SampleBar.vertical()
	yield 'HorizontalBar', SampleBar.horizontal()
	yield 'VerticalBarLarge', SampleBar.vertical_large()
	yield 'Pie', sample_Pie()


class SampleBar:
	fields = ['Internet', 'TV', 'Newspaper', 'Magazine', 'Radio']

	@classmethod
	def vertical(cls):

		g = bar.VerticalBar(cls.fields)

		g.stack = 'side'
		g.scale_integers = True
		g.width, g.height = 640,480
		g.graph_title = 'Question 7'
		g.show_graph_title = True

		g.add_data({'data': [-2, 3, 1, 3, 1], 'title': 'Female'})
		g.add_data({'data': [0, 2, 1, 5, 4], 'title': 'Male'})

		return g

	@classmethod
	def horizontal(cls):
		g = bar.HorizontalBar(cls.fields)

		g.stack = 'side'
		g.scale_integers = True
		g.width, g.height = 640,480
		g.graph_title = 'Question 7'
		g.show_graph_title = True

		g.add_data({'data': [-2, 3, 1, 3, 1], 'title': 'Female'})
		g.add_data({'data': [0, 2, 1, 5, 4], 'title': 'Male'})

		return g

	@classmethod
	def vertical_large(cls):
		g = bar.VerticalBar(cls.fields)
		options = dict(
			scale_integers=True,
			stack='side',
			width=640,
			height=480,
			graph_title='Question 8',
			show_graph_title=True,
			no_css=False,)
		g.__dict__.update(options)

		g.add_data(dict(data=[2,22,98,143,82], title='intermediate'))
		g.add_data(dict(data=[2,26,106,193,105], title='old'))
		return g

def sample_Pie():
	g = pie.Pie({})
	options = dict(
		width=640,
		height=480,
		fields=SampleBar.fields,
		graph_title='Question 7',
		expand_greatest = True,
		show_data_labels = True,
	)
	g.__dict__.update(options)
	g.add_data({'data': [-2, 3, 1, 3, 1], 'title': 'Female'})
	g.add_data({'data': [0, 2, 1, 5, 4], 'title': 'Male'})
	return g

def sample_Schedule():
	title = "Billy's Schedule"
	data1 = [
	  "History 107", "5/19/04", "6/30/04",
	  "Algebra 011", "6/2/04", "8/11/04",
	  "Psychology 101", "6/28/04", "8/9/04",
	  "Acting 105", "7/7/04", "8/16/04"
	  ]

	g = schedule.Schedule(dict(
		width = 640,
		height = 480,
		graph_title = title,
		show_graph_title = True,
		key = False,
		scale_x_integers = True,
		scale_y_integers = True,
		show_data_labels = True,
		show_y_guidelines = False,
		show_x_guidelines = True,
		# show_x_title = True, # not yet implemented
		x_title = "Time",
		show_y_title = False,
		rotate_x_labels = True,
		rotate_y_labels = False,
		x_label_format = "%m/%d",
		timescale_divisions = "1 week",
		add_popups = True,
		popup_format = "%m/%d/%y",
		area_fill = True,
		min_y_value = 0,
		))

	g.add_data(dict(data=data1, title="Data"))

	return g

def save_samples():
	root = os.path.dirname(__file__)
	for sample_name, sample in generate_samples():
		res = sample.burn()
		with open(os.path.join(root, sample_name+'.py.svg'), 'w') as f:
			f.write(res)

if __name__ == '__main__':
	save_samples()

