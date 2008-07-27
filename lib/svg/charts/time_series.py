#!/usr/bin/env python
import svg.charts.plot
import re
import pkg_resources
pkg_resources.require("python-dateutil>=1.1")
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from time import mktime
import datetime
fromtimestamp = datetime.datetime.fromtimestamp
from util import float_range

class Plot(svg.charts.plot.Plot):
	"""=== For creating SVG plots of scalar temporal data
		
		= Synopsis
		
		  import SVG.TimeSeries
		
		  # Data sets are x,y pairs
		  data1 = ["6/17/72", 11,    "1/11/72", 7,    "4/13/04 17:31", 11, 
				  "9/11/01", 9,    "9/1/85", 2,    "9/1/88", 1,    "1/15/95", 13]
		  data2 = ["8/1/73", 18,    "3/1/77", 15,    "10/1/98", 4, 
				  "5/1/02", 14,    "3/1/95", 6,    "8/1/91", 12,    "12/1/87", 6, 
				  "5/1/84", 17,    "10/1/80", 12]
		
		  graph = SVG::Graph::TimeSeries.new({
			:width => 640,
			:height => 480,
			:graph_title => title,
			:show_graph_title => true,
			:no_css => true,
			:key => true,
			:scale_x_integers => true,
			:scale_y_integers => true,
			:min_x_value => 0,
			:min_y_value => 0,
			:show_data_labels => true,
			:show_x_guidelines => true,
			:show_x_title => true,
			:x_title => "Time",
			:show_y_title => true,
			:y_title => "Ice Cream Cones",
			:y_title_text_direction => :bt,
			:stagger_x_labels => true,
			:x_label_format => "%m/%d/%y",
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
		
		Produces a graph of temporal scalar data.
		
		= Examples
		
		http://www.germane-software/repositories/public/SVG/test/timeseries.rb
		
		= Notes
		
		The default stylesheet handles upto 10 data sets, if you
		use more you must create your own stylesheet and add the
		additional settings for the extra data sets. You will know
		if you go over 10 data sets as they will have no style and
		be in black.
		
		Unlike the other types of charts, data sets must contain x,y pairs:
		
		  ["12:30", 2]          # A data set with 1 point: ("12:30",2)
		  ["01:00",2, "14:20",6] # A data set with 2 points: ("01:00",2) and 
								  #                           ("14:20",6)  
		
		Note that multiple data sets within the same chart can differ in length, 
		and that the data in the datasets needn't be in order; they will be ordered
		by the plot along the X-axis.
		
		The dates must be parseable by ParseDate, but otherwise can be
		any order of magnitude (seconds within the hour, or years)
		
		= See also
		
		* SVG::Graph::Graph
		* SVG::Graph::BarHorizontal
		* SVG::Graph::Bar
		* SVG::Graph::Line
		* SVG::Graph::Pie
		* SVG::Graph::Plot
		
		== Author
		
		Sean E. Russell <serATgermaneHYPHENsoftwareDOTcom>
		
		Copyright 2004 Sean E. Russell
		This software is available under the Ruby license[LICENSE.txt]
"""
	popup_format = x_label_format = '%Y-%m-%d %H:%M:%S'
	__doc_popup_format_ = "The formatting usped for the popups.  See x_label_format"
	__doc_x_label_format_ = "The format string used to format the X axis labels.  See strftime."
	
	timescale_divisions = None
	__doc_timescale_divisions_ = """Use this to set the spacing between dates on the axis.  The value
		must be of the form 
		"\d+ ?(days|weeks|months|years|hours|minutes|seconds)?"

		EG:

		graph.timescale_divisions = "2 weeks"

		will cause the chart to try to divide the X axis up into segments of
		two week periods."""
	
	def add_data(self, data):
		"""Add data to the plot.
			d1 = ["12:30", 2]          # A data set with 1 point: ("12:30",2)
			d2 = ["01:00",2, "14:20",6] # A data set with 2 points: ("01:00",2) and 
										 #                           ("14:20",6)  
			graph.add_data(
			  :data => d1,
			  :title => 'One'
			)
			graph.add_data(
			  :data => d2,
			  :title => 'Two'
			)
			
			Note that the data must be in time,value pairs, and that the date format
			may be any date that is parseable by ParseDate."""
		super(Plot, self).add_data(data)
		
	def process_data(self, data):
		super(Plot, self).process_data(data)
		# the date should be in the first element, so parse it out
		data['data'][0] = map(self.parse_date, data['data'][0])

	_min_x_value = svg.charts.plot.Plot.min_x_value	
	def get_min_x_value(self):
		return self._min_x_value
	def set_min_x_value(self, date):
		self._min_x_value = self.parse_date(date)
	min_x_value = property(get_min_x_value, set_min_x_value)
	
	def format(self, x, y):
		return fromtimestamp(x).strftime(self.popup_format)
	
	def get_x_labels(self):
		return map(lambda t: fromtimestamp(t).strftime(self.x_label_format), self.get_x_values())

	def get_x_values(self):
		result = self.get_x_timescale_division_values()
		if result: return result
		return tuple(float_range(*self.x_range()))
			
	def get_x_timescale_division_values(self):
		if not self.timescale_divisions: return
		min, max, scale_division = self.x_range()
		m = re.match('(?P<amount>\d+) ?(?P<division_units>days|weeks|months|years|hours|minutes|seconds)?', self.timescale_divisions)
		# copy amount and division_units into the local namespace
		division_units = m.groupdict()['division_units'] or 'days'
		amount = int(m.groupdict()['amount'])
		if not amount: return
		delta = relativedelta(**{division_units: amount})
		result = tuple(self.get_time_range(min, max, delta))
		return result
	
	def get_time_range(self, start, stop, delta):
		start, stop = map(fromtimestamp, (start, stop))
		current = start
		while current <= stop:
			yield mktime(current.timetuple())
			current += delta
			
	def parse_date(self, date_string):
		return mktime(parse(date_string).timetuple())