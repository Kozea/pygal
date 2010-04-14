#!/usr/bin/env python
from itertools import izip, count, chain
from lxml import etree

from svg.charts.graph import Graph

from util import float_range

def get_pairs(i):
	i = iter(i)
	while True:	yield i.next(), i.next()
	
class Plot(Graph):
	"""=== For creating SVG plots of scalar data
	
	= Synopsis
	
	  require 'SVG/Graph/Plot'
	
	  # Data sets are x,y pairs
	  # Note that multiple data sets can differ in length, and that the
	  # data in the datasets needn't be in order; they will be ordered
	  # by the plot along the X-axis.
	  projection = [
		6, 11,    0, 5,   18, 7,   1, 11,   13, 9,   1, 2,   19, 0,   3, 13,
		7, 9 
	 ]
	  actual = [
		0, 18,    8, 15,    9, 4,   18, 14,   10, 2,   11, 6,  14, 12,   
		15, 6,   4, 17,   2, 12
	 ]
	  
	  graph = SVG::Graph::Plot.new({
	   :height => 500,
		   :width => 300,
		:key => true,
		:scale_x_integers => true,
		:scale_y_integerrs => true,
	 })
	  
	  graph.add_data({
	   :data => projection
		 :title => 'Projected',
	 })
	
	  graph.add_data({
	   :data => actual,
		 :title => 'Actual',
	 })
	  
	  print graph.burn()
	
	= Description
	
	Produces a graph of scalar data.
	
	This object aims to allow you to easily create high quality
	SVG[http://www.w3c.org/tr/svg] scalar plots. You can either use the
	default style sheet or supply your own. Either way there are many options
	which can be configured to give you control over how the graph is
	generated - with or without a key, data elements at each point, title,
	subtitle etc.
	
	= Examples
	
	http://www.germane-software/repositories/public/SVG/test/plot.rb
	
	= Notes
	
	The default stylesheet handles upto 10 data sets, if you
	use more you must create your own stylesheet and add the
	additional settings for the extra data sets. You will know
	if you go over 10 data sets as they will have no style and
	be in black.
	
	Unlike the other types of charts, data sets must contain x,y pairs:
	
	  [1, 2]    # A data set with 1 point: (1,2)
	  [1,2, 5,6] # A data set with 2 points: (1,2) and (5,6)  
	
	= See also
	
	* SVG::Graph::Graph
	* SVG::Graph::BarHorizontal
	* SVG::Graph::Bar
	* SVG::Graph::Line
	* SVG::Graph::Pie
	* SVG::Graph::TimeSeries
	
	== Author
	
	Sean E. Russell <serATgermaneHYPHENsoftwareDOTcom>
	
	Copyright 2004 Sean E. Russell
	This software is available under the Ruby license[LICENSE.txt]"""

	top_align = right_align = top_font = right_font = 1

	
	"""Determines the scaling for the Y axis divisions.
	
	  graph.scale_y_divisions = 0.5
	
	would cause the graph to attempt to generate labels stepped by 0.5; EG:
	0, 0.5, 1, 1.5, 2, ..."""
	scale_y_divisions = None
	"Make the X axis labels integers"
	scale_x_integers = False 
	"Make the Y axis labels integers"
	scale_y_integers = False
	"Fill the area under the line"
	area_fill = False
	"""Show a small circle on the graph where the line
	goes from one point to the next."""
	show_data_points = True
	"Indicate whether the lines should be drawn between points"
	draw_lines_between_points = True
	"Set the minimum value of the X axis"
	min_x_value = None
	"Set the minimum value of the Y axis"
	min_y_value = None
	"Set the maximum value of the X axis"
	max_x_value = None
	"Set the maximum value of the Y axis"
	max_y_value = None

	stacked = False

	@apply
	def scale_x_divisions():
		doc = """Determines the scaling for the X axis divisions.
			
			graph.scale_x_divisions = 2
			
			would cause the graph to attempt to generate labels stepped by 2; EG:
			0,2,4,6,8..."""
		def fget(self):
			return getattr(self, '_scale_x_divisions', None)
		def fset(self, val):
			self._scale_x_divisions = val
		return property(**locals())

	def validate_data(self, data):
		if len(data['data']) % 2 != 0:
			raise ValueError("Expecting x,y pairs for data points for %s." % self.__class__.__name__)

	def process_data(self, data):
		pairs = list(get_pairs(data['data']))
		pairs.sort()
		data['data'] = zip(*pairs)

	def calculate_left_margin(self):
		super(Plot, self).calculate_left_margin()
		label_left = len(str(self.get_x_labels()[0])) / 2 * self.font_size * 0.6
		self.border_left = max(label_left, self.border_left)
	
	def calculate_right_margin(self):
		super(Plot, self).calculate_right_margin()
		label_right = len(str(self.get_x_labels()[-1])) / 2 * self.font_size * 0.6
		self.border_right = max(label_right, self.border_right)

	def data_max(self, axis):
		data_index = getattr(self, '%s_data_index' % axis)
		max_value = max(chain(*map(lambda set: set['data'][data_index], self.data)))
		# above is same as
		#max_value = max(map(lambda set: max(set['data'][data_index]), self.data))
		spec_max = getattr(self, 'max_%s_value' % axis)
		max_value = max(max_value, spec_max)
		return max_value

	def data_min(self, axis):
		data_index = getattr(self, '%s_data_index' % axis)
		min_value = min(chain(*map(lambda set: set['data'][data_index], self.data)))
		spec_min = getattr(self, 'min_%s_value' % axis)
		if spec_min is not None:
			min_value = min(min_value, spec_min)
		return min_value
		
	x_data_index = 0
	y_data_index = 1
	def data_range(self, axis):
		side = {'x': 'right', 'y': 'top'}[axis]

		min_value = self.data_min(axis)
		max_value = self.data_max(axis)
		range = max_value - min_value
		
		side_pad = range / 20.0 or 10
		scale_range = (max_value + side_pad) - min_value
		
		scale_division = getattr(self, 'scale_%s_divisions' % axis) or (scale_range / 10.0)
		
		if getattr(self, 'scale_%s_integers' % axis):
			scale_division = round(scale_division) or 1
			
		return min_value, max_value, scale_division

	def x_range(self): return self.data_range('x')
	def y_range(self): return self.data_range('y')
	
	def get_data_values(self, axis):
		min_value, max_value, scale_division = self.data_range(axis)
		return tuple(float_range(*self.data_range(axis)))
	
	def get_x_values(self): return self.get_data_values('x')
	def get_y_values(self): return self.get_data_values('y')

	def get_x_labels(self):
		return map(str, self.get_x_values())
	def get_y_labels(self):
		return map(str, self.get_y_values())
	
	def field_size(self, axis):
		size = {'x': 'width', 'y': 'height'}[axis]
		side = {'x': 'right', 'y': 'top'}[axis]
		values = getattr(self, 'get_%s_values' % axis)()
		max_d = self.data_max(axis)
		dx = len(values) > 1 and float(max_d - values[-1]) / \
			(values[-1] - values[-2]) or max_d
		graph_size = getattr(self, 'graph_%s' % size)
		side_font = getattr(self, '%s_font' % side)
		side_align = getattr(self, '%s_align' % side)
		result = (float(graph_size) - self.font_size*2*side_font) / \
		   (len(values) + dx - side_align)
		return result
	
	def field_width(self): return self.field_size('x')
	def field_height(self): return self.field_size('y')

	def draw_data(self):
		self.load_transform_parameters()
		for line, data in izip(count(1), self.data):
			x_start, y_start = self.transform_output_coordinates(
				(data['data'][self.x_data_index][0],
				data['data'][self.y_data_index][0])
			)
			data_points = zip(*data['data'])
			graph_points = self.get_graph_points(data_points)
			lpath = self.get_lpath(graph_points)
			if self.area_fill:
				graph_height = self.graph_height
				path = etree.SubElement(self.graph, 'path', {
					'd': 'M%(x_start)f %(graph_height)f %(lpath)s V%(graph_height)f Z' % vars(),
					'class': 'fill%(line)d' % vars()})
			if self.draw_lines_between_points:
				path = etree.SubElement(self.graph, 'path', {
					'd': 'M%(x_start)f %(y_start)f %(lpath)s' % vars(),
					'class': 'line%(line)d' % vars()})
			self.draw_data_points(line, data_points, graph_points)
		self._draw_constant_lines()
		del self.__transform_parameters

	def add_constant_line(self, value, label = None, style = None):
		self.constant_lines = getattr(self, 'constant_lines', [])
		self.constant_lines.append((value, label, style))

	def _draw_constant_lines(self):
		if hasattr(self, 'constant_lines'):
			map(self.__draw_constant_line, self.constant_lines)

	def __draw_constant_line(self, (value, label, style)):
		"Draw a constant line on the y-axis with the label"
		start = self.transform_output_coordinates((0, value))[1]
		stop = self.graph_width
		path = etree.SubElement(self.graph, 'path', {
			'd': 'M 0 %(start)s h%(stop)s' % vars(),
			'class': 'constantLine'})
		if style:
			path.set('style', style)
		text = etree.SubElement(self.graph, 'text', {
			'x': str(2),
			'y': str(start - 2),
			'class': 'constantLine'})
		text.text = label

	def load_transform_parameters(self):
		"Cache the parameters necessary to transform x & y coordinates"
		x_min, x_max, x_div = self.x_range()
		y_min, y_max, y_div = self.y_range()
		x_step = (float(self.graph_width) - self.font_size*2) / \
			(x_max - x_min)
		y_step = (float(self.graph_height) - self.font_size*2) / \
			(y_max - y_min)
		self.__transform_parameters = dict(vars())
		del self.__transform_parameters['self']
		
	def get_graph_points(self, data_points):
		return map(self.transform_output_coordinates, data_points)

	def get_lpath(self, points):
		points = map(lambda p: "%f %f" % p, points)
		return 'L' + ' '.join(points)
	
	def transform_output_coordinates(self, (x,y)):
		x_min = self.__transform_parameters['x_min']
		x_step = self.__transform_parameters['x_step']
		y_min = self.__transform_parameters['y_min']
		y_step = self.__transform_parameters['y_step']
		#locals().update(self.__transform_parameters)
		#vars().update(self.__transform_parameters)
		x = (x - x_min) * x_step
		y = self.graph_height - (y - y_min) * y_step
		return x,y
	
	def draw_data_points(self, line, data_points, graph_points):
		if not self.show_data_points \
			and not self.show_data_values: return
		for ((dx,dy),(gx,gy)) in izip(data_points, graph_points):
			if self.show_data_points:
				etree.SubElement(self.graph, 'circle', {
					'cx': str(gx),
					'cy': str(gy),
					'r': '2.5',
					'class': 'dataPoint%(line)s' % vars()})
			if self.show_data_values:
				self.add_popup(gx, gy, self.format(dx, dy))
			self.make_datapoint_text(gx, gy-6, dy)
	
	def format(self, x, y):
		return '(%0.2f, %0.2f)' % (x,y)
