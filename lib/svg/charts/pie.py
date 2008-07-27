#!python

# $Id$

import math
from operator import add
from svg.charts.graph import Graph

def robust_add(a,b):
	"Add numbers a and b, treating None as 0"
	if a is None: a = 0
	if b is None: b = 0
	return a+b

RADIANS = math.pi/180

class Pie(Graph):
	# === Create presentation quality SVG pie graphs easily
	# 
	# == Synopsis
	# 
	#   require 'SVG/Graph/Pie'
	# 
	#   fields = %w(Jan Feb Mar)
	#   data_sales_02 = [12, 45, 21]
	#   
	#   graph = SVG::Graph::Pie.new({
	#   	:height => 500,
	# 	  :width  => 300,
	# 	  :fields => fields,
	#  })
	#   
	#   graph.add_data({
	#   	:data => data_sales_02,
	# 	  :title => 'Sales 2002',
	#  })
	#   
	#   print "Content-type: image/svg+xml\r\n\r\n"
	#   print graph.burn();
	# 
	# == Description
	# 
	# This object aims to allow you to easily create high quality
	# SVG pie graphs. You can either use the default style sheet
	# or supply your own. Either way there are many options which can
	# be configured to give you control over how the graph is
	# generated - with or without a key, display percent on pie chart,
	# title, subtitle etc.
	#
	# = Examples
	# 
	# http://www.germane-software/repositories/public/SVG/test/single.rb
	# 
	# == See also
	#
	# * SVG::Graph::Graph
	# * SVG::Graph::BarHorizontal
	# * SVG::Graph::Bar
	# * SVG::Graph::Line
	# * SVG::Graph::Plot
	# * SVG::Graph::TimeSeries
	#
	# == Author
	#
	# Sean E. Russell <serATgermaneHYPHENsoftwareDOTcom>
	#
	# Copyright 2004 Sean E. Russell
	# This software is available under the Ruby license[LICENSE.txt]
	#

	"if true, displays a drop shadow for the chart"
	show_shadow	= True
	"Sets the offset of the shadow from the pie chart"
	shadow_offset = 10 

	show_data_labels = False
	"If true, display the actual field values in the data labels"	
	show_actual_values = False
	"If true, display the percentage value of each pie wedge in the data labels"
	show_percent = True
	
	"If true, display the labels in the key"
	show_key_data_labels = True
	"If true, display the actual value of the field in the key"
	show_key_actual_values = True
	"If true, display the percentage value of the wedges in the key"
	show_key_percent = False

	"If true, explode the pie (put space between the wedges)"	
	expanded = False
	"If true, expand the largest pie wedge"
	expand_greatest	= False
	"The amount of space between expanded wedges"
	expand_gap = 10
	
	show_x_labels = False
	show_y_labels = False

	"The font size of the data point labels"
	datapoint_font_size = 12

	def add_data(self, data_descriptor):
		"""
		Add a data set to the graph
		
		>>> graph.add_data({data:[1,2,3,4]}) # doctest: +SKIP
		
		Note that a 'title' key is ignored.
		
		Multiple calls to add_data will sum the elements, and the pie will
		display the aggregated data.  e.g.
		
		>>> graph.add_data({data:[1,2,3,4]}) # doctest: +SKIP
		>>> graph.add_data({data:[2,3,5,7]}) # doctest: +SKIP
		
		is the same as:
		
		graph.add_data({data:[3,5,8,11]}) # doctest: +SKIP
		"""
		self.data = map(robust_add, self.data, data_descriptor['data'])

	def add_defs(self, defs):
		"Add svg definitions"
		gradient = self._create_element(
			'filter',
			dict(
				id='dropshadow',
				width='1.2',
				height='1.2',
				)
			)
		defs.appendChild(gradient)
		blur = self._create_element(
			'feGaussianBlur',
			dict(
				stdDeviation='4',
				result='blur',
				)
			)
		gradient.appendChild(blur)

	def draw_graph(self):
		"Here we don't need the graph (consider refactoring)"
		pass

	def get_y_labels(self):
		"Definitely consider refactoring"
		return ['']

	def get_x_labels(self):
		"Okay.  I'll refactor after this"
		['']

	def keys(self):
		total = reduce(add, self.data)
		percent_scale = 100.0 / total
		def key(field, value):
			result = [field]
			result.append('[%s]' % value)
			if self.show_key_percent:
				percent = str(round((v/total*100))) + '%'
				result.append(percent)
			return ' '.join(result)
		return map(key, self.fields, self.data)
	
	def draw_data(self):
		self.graph = self._create_element('g')
		self.root.appendChild(self.graph)
		background = self._create_element('g')
		self.graph.appendChild(background)
		midground = self._create_element('g')
		self.graph.appendChild(midground)
		
		is_expanded = (self.expanded or self.expand_greatest)
		diameter = min(self.graph_width, self.graph_height)
		# the following assumes int(True)==1 and int(False)==0
		diameter -= self.expand_gap * int(is_expanded)
		diameter -= self.datapoint_font_size * int(self.show_data_labels)
		diameter -= 10 * int(self.show_shadow)
		radius = diameter / 2.0

		xoff = (self.width - diameter) / 2
		yoff = (self.height - self.border_bottom - diameter)
		yoff -= 10 * int(self.show_shadow)
		transform = 'translate(%(xoff)s %(yoff)s)' % vars()
		self.graph.setAttribute('transform', transform)

		wedge_text_pad = 5
		wedge_text_pad = 20 * int(self.show_percent) * int(self.show_data_labels)

		total = reduce(add, self.data)
		max_value = max(self.data)

		percent_scale = 100.0 / total

		prev_percent = 0
		rad_mult = 3.6 * RADIANS
		for index, (field, value) in enumerate(zip(self.fields, self.data)):
			percent = percent_scale * value
			
			radians = prev_percent * rad_mult
			x_start = radius+(math.sin(radians) * radius)
			y_start = radius-(math.cos(radians) * radius)
			radians = (prev_percent+percent) * rad_mult
			x_end = radius+(math.sin(radians) * radius)
			y_end = radius-(math.cos(radians) * radius)
			percent_greater_fifty = int(percent>=50)
			path = ' '.join((
				"M%(radius)s,%(radius)s",
				"L%(x_start)s,%(y_start)s",
				"A%(radius)s,%(radius)s",
				"0,",
				"%(percent_greater_fifty)s,1,",
				"%(x_end)s %(y_end)s Z"))
			path = path % vars()
			
			wedge = self._create_element(
				'path',
				dict({
					'd': path,
					'class': 'fill%s' % (index+1),
					})
				)
			self.foreground.appendChild(wedge)
			
			translate = None
			tx = 0
			ty = 0
			half_percent = prev_percent + percent / 2
			radians = half_percent * rad_mult
			
			if self.show_shadow:
				shadow = self._create_element(
					'path',
					dict(
						d=path,
						filter='url(#dropshadow)',
						style='fill: #ccc; stroke: none',
					)
				)
				background.appendChild(shadow)
				clear = self._create_element(
					'path',
					dict(
						d=path,
						# note, this probably only works when the background
						#  is also #fff
						style="fill:#fff; stroke:none;",
					)
				)
				midground.appendChild(clear)
			
			if self.expanded or (self.expand_greatest and value == max_value):
				tx = (math.sin(radians) * self.expand_gap)
				ty = -(math.cos(radians) * self.expand_gap)
				translate = "translate(%(tx)s %(ty)s)" % vars()
				wedge.setAttribute('transform', translate)
				clear.setAttribute('transform', translate)
			
			if self.show_shadow:
				shadow_tx = self.shadow_offset + tx
				shadow_ty = self.shadow_offset + ty
				translate = 'translate(%(shadow_tx)s %(shadow_ty)s)' % vars()
				shadow.setAttribute('transform', translate)
			
			if self.show_data_labels and value != 0:
				label = []
				if self.show_key_data_labels:
					label.append(field)
				if self.show_actual_values:
					label.append('[%s]' % value)
				if self.show_percent:
					label.append('%d%%' % round(percent))
				label = ' '.join(label)

				msr = math.sin(radians)
				mcr = math.cos(radians)
				tx = radius + (msr * radius)
				ty = radius -(mcr * radius)
				
				if self.expanded or (self.expand_greatest and value == max_value):
				  tx += (msr * self.expand_gap)
				  ty -= (mcr * self.expand_gap)

				label_node = self._create_element(
					'text',
					dict({
						'x':str(tx),
						'y':str(ty),
						'class':'dataPointLabel',
						'style':'stroke: #fff; stroke-width: 2;',
					})
				)
				label_node.appendChild(self._doc.createTextNode(label))
				self.foreground.appendChild(label_node)

				label_node = self._create_element(
					'text',
					dict({
						'x':str(tx),
						'y':str(ty),
						'class': 'dataPointLabel',
					})
				)
				label_node.appendChild(self._doc.createTextNode(label))
				self.foreground.appendChild(label_node)
			
			prev_percent += percent

	def round(self, val, to):
		return round(val,to)

	def get_css(self):
		return """\
.dataPointLabel{
	fill: #000000;
	text-anchor:middle;
	font-size: #{datapoint_font_size}px;
	font-family: "Arial", sans-serif;
	font-weight: normal;
}

/* key - MUST match fill styles */
.key1,.fill1{
	fill: #ff0000;
	fill-opacity: 0.7;
	stroke: none;
	stroke-width: 1px;	
}
.key2,.fill2{
	fill: #0000ff;
	fill-opacity: 0.7;
	stroke: none;
	stroke-width: 1px;	
}
.key3,.fill3{
	fill-opacity: 0.7;
	fill: #00ff00;
	stroke: none;
	stroke-width: 1px;	
}
.key4,.fill4{
	fill-opacity: 0.7;
	fill: #ffcc00;
	stroke: none;
	stroke-width: 1px;	
}
.key5,.fill5{
	fill-opacity: 0.7;
	fill: #00ccff;
	stroke: none;
	stroke-width: 1px;	
}
.key6,.fill6{
	fill-opacity: 0.7;
	fill: #ff00ff;
	stroke: none;
	stroke-width: 1px;	
}
.key7,.fill7{
	fill-opacity: 0.7;
	fill: #00ff99;
	stroke: none;
	stroke-width: 1px;	
}
.key8,.fill8{
	fill-opacity: 0.7;
	fill: #ffff00;
	stroke: none;
	stroke-width: 1px;	
}
.key9,.fill9{
	fill-opacity: 0.7;
	fill: #cc6666;
	stroke: none;
	stroke-width: 1px;	
}
.key10,.fill10{
	fill-opacity: 0.7;
	fill: #663399;
	stroke: none;
	stroke-width: 1px;	
}
.key11,.fill11{
	fill-opacity: 0.7;
	fill: #339900;
	stroke: none;
	stroke-width: 1px;	
}
.key12,.fill12{
	fill-opacity: 0.7;
	fill: #9966FF;
	stroke: none;
	stroke-width: 1px;	
}
"""
