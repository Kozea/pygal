#!python

# $Id$

from operator import itemgetter, add
from lxml import etree

from util import flatten, float_range
from svg.charts.graph import Graph

class Line(Graph):
	"""     === Create presentation quality SVG line graphs easily
     
     = Synopsis
     
       require 'SVG/Graph/Line'
     
       fields = %w(Jan Feb Mar);
       data_sales_02 = [12, 45, 21]
       data_sales_03 = [15, 30, 40]
       
       graph = SVG::Graph::Line.new({
       	:height => 500,
        	:width => 300,
     	  :fields => fields,
      })
       
       graph.add_data({
       	:data => data_sales_02,
     	  :title => 'Sales 2002',
      })
     
       graph.add_data({
       	:data => data_sales_03,
     	  :title => 'Sales 2003',
      })
       
       print "Content-type: image/svg+xml\r\n\r\n";
       print graph.burn();
     
     = Description
     
     This object aims to allow you to easily create high quality
     SVG line graphs. You can either use the default style sheet
     or supply your own. Either way there are many options which can
     be configured to give you control over how the graph is
     generated - with or without a key, data elements at each point,
     title, subtitle etc.
     
     = Examples
     
     http://www.germane-software/repositories/public/SVG/test/single.rb
     
     = Notes
     
     The default stylesheet handles upto 10 data sets, if you
     use more you must create your own stylesheet and add the
     additional settings for the extra data sets. You will know
     if you go over 10 data sets as they will have no style and
     be in black.
     
     = See also
     
     * SVG::Graph::Graph
     * SVG::Graph::BarHorizontal
     * SVG::Graph::Bar
     * SVG::Graph::Pie
     * SVG::Graph::Plot
     * SVG::Graph::TimeSeries

     == Author

     Sean E. Russell <serATgermaneHYPHENsoftwareDOTcom>

     Copyright 2004 Sean E. Russell
     This software is available under the Ruby license[LICENSE.txt]

"""

	"""Show a small circle on the graph where the line goes from one point to
	the next"""
	show_data_points = True
	show_data_values = True
	"""Accumulates each data set. (i.e. Each point increased by sum of all
	previous series at same point)."""
	stacked = False
	"Fill in the area under the plot"
	area_fill = False

	#override some defaults
	top_align = top_font = right_align = right_font = True
	
	css_file = 'plot.css'

	def max_value(self):
		data = map(itemgetter('data'), self.data)
		if self.stacked:
			data = self.get_cumulative_data()
		return max(flatten(data))

	def min_value(self):
		if self.min_scale_value:
			return self.min_scale_value
		data = map(itemgetter('data'), self.data)
		if self.stacked:
			data = self.get_cumulative_data()
		return min(flatten(data))

	def get_cumulative_data():
		"""Get the data as it will be charted.  The first set will be
		the actual first data set.  The second will be the sum of the
		first and the second, etc."""
		sets = map(itemgetter('data'), self.data)
		if not sets: return
		sum = sets.pop(0)
		yield sum
		while sets:
			sum = map(add, sets.pop(0))
			yield sum

	def get_x_labels(self):
		return self.fields

	def calculate_left_margin(self):
		super(self.__class__, self).calculate_left_margin()
		label_left = self.fields[0].length / 2 * self.font_size * 0.6
		self.border_left = max(label_left, self.border_left)

	def get_y_labels(self):
		max_value = self.max_value()
		min_value = self.min_value()
		range = max_value - min_value
		top_pad = (range / 20.0) or 10
		scale_range = (max_value + top_pad) - min_value
		
		scale_division = self.scale_divisions or (scale_range / 10.0)
		
		if self.scale_integers:
		  scale_division = min(1, round(scale_division))
		
		#maxvalue = maxvalue%scale_division == 0 ? 
		#  maxvalue : maxvalue + scale_division
		labels = tuple(float_range(min_value, max_value, scale_division))
		return labels

	def calc_coords(self, field, value, width = None, height = None):
		if width is None: width = self.field_width
		if height is None: height = self.field_height
		coords = dict(
			x = width * field,
			y = self.graph_height - value * height,
			)
		return coords

	def draw_data(self):
		min_value = self.min_value()
		field_height = self.graph_height - self.font_size*2*self.top_font
		y_label_span = max(self.get_y_labels()) - min(self.get_y_labels())
		field_height /= float(y_label_span)
		
		field_width = self.field_width
		#line = len(self.data)
		
		prev_sum = [0]*len(self.fields)
		cum_sum = [-min_value]*len(self.fields)

		coord_format = lambda c: '%(x)s %(y)s' % c
		
		for line_n, data in list(enumerate(self.data)).reversed():
			apath = ''
			
			if not self.stacked: cum_sum = [-min_value]*len(self.fields)
		
			cum_sum = map(add, cum_sum, data['data'])
			get_coords = lambda (i, val): self.calc_coords(i,
														 val,
														 field_width,
														 field_height)
			coords = map(get_coords, enumerate(cum_sum))
			paths = map(coord_format, coords)
			line_path = ' '.join(paths)

			if self.area_fill:
				# to draw the area, we'll use the line above, followed by
				#  tracing the bottom from right to left
				if self.stacked:
					prev_sum_rev = list(enumerate(prev_sum)).reversed()
					coords = map(get_coords, prev_sum_rev)
					paths = map(coord_format, coords)
					area_path = ' '.join(paths)
					origin = paths[-1]
				else:
					area_path = "V#@graph_height"
					origin = coord_format(get_coords(0,0))

				d = ' '.join((
					'M',
					origin,
					'L',
					line_path,
					area_path,
					'Z'
				))
				etree.SubElement(self.graph, 'path', {
					'class': 'fill%(line_n)s' % vars(),
					'd': d,
					})

			# now draw the line itself
			etree.SubElement(self.graph, 'path', {
				'd': 'M0 '+self.graph_height+' L'+line_path,
				'class': 'line%(line_n)s' % vars(),
				})
			
			if self.show_data_points or self.show_data_values:
				for i, value in enumerate(cum_sum):
					if self.show_data_points:
						circle = etree.SubElement(
							self.graph,
							'circle',
							{'class': 'dataPoint%(line_n)s' % vars()},
							cx = str(field_width*i),
							cy = str(self.graph_height - value*field_height),
							r = '2.5',
							)
					self.make_datapoint_text(
						field_width*i,
						self.graph_height - value*field_height - 6,
						value + min_value
						)

			prev_sum = list(cum_sum)		
