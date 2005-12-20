#!/usr/bin/env python
import SVG

class Plot( SVG.Graph ):
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
	
	  [ 1, 2 ]    # A data set with 1 point: (1,2)
	  [ 1,2, 5,6] # A data set with 2 points: (1,2) and (5,6)  
	
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

	show_data_points = True
	area_fill = True
	stacked = True
	
	top_align = right_align = top_font = right_font = 1
	
	@apply
	def scale_x_divisions( self ):
		doc = """      # Determines the scaling for the X axis divisions.
			
			graph.scale_x_divisions = 2
			
			would cause the graph to attempt to generate labels stepped by 2; EG:
			0,2,4,6,8..."""
		def fget( self ):
			return self._scale_x_divisions
		def fset( self, val ):
			self._scale_x_divisions = val
		return property(**locals())

	def validate_data( self, data ):
		if len( data['data'] ) % 2 != 0:
			raise "Expecting x,y pairs for data points for %s." % self.__class__.__name__
		
		
	