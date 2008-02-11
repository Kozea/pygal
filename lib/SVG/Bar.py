#!python
from SVG import Graph
from itertools import chain

__all__ = ( 'VerticalBar', 'HorizontalBar' )

class Bar( Graph ):
	"A superclass for bar-style graphs.  Do not instantiate directly."

	# gap between bars
	bar_gap = True
	# how to stack adjacent dataset series
	# overlap - overlap bars with transparent colors
	# top - stack bars on top of one another
	# side - stack bars side-by-side
	stack = 'overlap'
	
	scale_divisions = None

	def __init__( self, fields, *args, **kargs ):
		self.fields = fields
		super( Bar, self ).__init__( *args, **kargs )

	def data_max( self ):
		return max( chain( *map( lambda set: set['data'], self.data ) ) )
		# above is same as
		# return max( map( lambda set: max( set['data'] ), self.data ) )
		
	def data_min( self ):
		if not self.min_scale_value is None: return self.min_scale_value
		min_value = min( chain( *map( lambda set: set['data'], self.data ) ) )
		min_value = min( min_value, 0 )
		return min_value

	def get_css( self ):
		return """\
/* default fill styles for multiple datasets (probably only use a single dataset on this graph though) */
.key1,.fill1{
	fill: #ff0000;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 0.5px;	
}
.key2,.fill2{
	fill: #0000ff;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
.key3,.fill3{
	fill: #00ff00;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
.key4,.fill4{
	fill: #ffcc00;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
.key5,.fill5{
	fill: #00ccff;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
.key6,.fill6{
	fill: #ff00ff;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
.key7,.fill7{
	fill: #00ffff;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
.key8,.fill8{
	fill: #ffff00;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
.key9,.fill9{
	fill: #cc6666;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
.key10,.fill10{
	fill: #663399;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
.key11,.fill11{
	fill: #339900;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
.key12,.fill12{
	fill: #9966FF;
	fill-opacity: 0.5;
	stroke: none;
	stroke-width: 1px;	
}
"""

def float_range( start = 0, stop = None, step = 1 ):
	"Much like the built-in function range, but accepts floats"
	while start < stop:
		yield float( start )
		start += step


class VerticalBar( Bar ):
	"""    # === Create presentation quality SVG bar graphs easily
    #
    # = Synopsis
    #
    #   require 'SVG/Graph/Bar'
    #
    #   fields = %w(Jan Feb Mar);
    #   data_sales_02 = [12, 45, 21]
    #
    #   graph = SVG::Graph::Bar.new(
    #     :height => 500,
    #     :width => 300,
    #     :fields => fields
    #   )
    #
    #   graph.add_data(
    #     :data => data_sales_02,
    #     :title => 'Sales 2002'
    #   )
    #
    #   print "Content-type: image/svg+xml\r\n\r\n"
    #   print graph.burn
    #
    # = Description
    #
    # This object aims to allow you to easily create high quality
    # SVG[http://www.w3c.org/tr/svg bar graphs. You can either use the default
    # style sheet or supply your own. Either way there are many options which
    # can be configured to give you control over how the graph is generated -
    # with or without a key, data elements at each point, title, subtitle etc.
    #
    # = Notes
    #
    # The default stylesheet handles upto 12 data sets, if you
    # use more you must create your own stylesheet and add the
    # additional settings for the extra data sets. You will know
    # if you go over 12 data sets as they will have no style and
    # be in black.
    #
    # = Examples
    #
    # * http://germane-software.com/repositories/public/SVG/test/test.rb
    #
    # = See also
    #
    # * SVG::Graph::Graph
    # * SVG::Graph::BarHorizontal
    # * SVG::Graph::Line
    # * SVG::Graph::Pie
    # * SVG::Graph::Plot
    # * SVG::Graph::TimeSeries
"""
	top_align = top_font = 1

	def get_x_labels( self ):
		return self.fields

	# adapted from plot (very much like calling data_range('y'))
	def data_range( self ):

		min_value = self.data_min( )
		max_value = self.data_max( )
		range = max_value - min_value

		top_pad = range / 20.0 or 10
		scale_range = ( max_value + top_pad ) - min_value
		
		scale_division = self.scale_divisions or ( scale_range / 10.0 )
		
		if self.scale_integers:
			scale_division = scale_division.round() or 1
			
		return min_value, max_value, scale_division

	# adapted from Plot
	def get_data_values( self ):
		return tuple( float_range( *self.data_range( ) ) )
	
	# adapted from Plot
	def get_y_labels( self ):
		return map( str, self.get_data_values() )

	def x_label_offset( self, width ):
		return width / 2.0

	def draw_data( self ):
		min_value = self.data_min()
		unit_size = (float(self.graph_height) - self.font_size*2*self.top_font)
		unit_size /= ( max( self.get_y_labels() ) - min( self.get_y_labels() ) )
		
		bar_gap = 0
		if self.bar_gap:
			bar_gap = 10
			if self.get_field_width() < 10:
				bar_gap = self.get_field_width() / 2

		bar_width = self.get_field_width() - bar_gap
		if self.stack == 'side':
			bar_width /= len( self.data )
		
		x_mod = ( self.graph_width - bar_gap )/2
		if self.stack == 'side':
			x_mod -= bar_width/2

		bottom = self.graph_height
		
		for field_count, field in enumerate( self.fields ):
			for dataset_count, dataset in enumerate( self.data ):
				# cases (assume 0 = +ve):
				#   value  min  length
				#    +ve   +ve  value - min
				#    +ve   -ve  value - 0
				#    -ve   -ve  value.abs - 0
				value = dataset['data'][field_count]
				
				left = self.get_field_width() * self.field_count
				
				length = ( abs(value) - max( min_value, 0 ) ) * unit_size
				# top is 0 if value is negative
				top = bottom - (( min(value,0) - min_value ) * unit_size )
				if self.stack == 'side':
					left += self.bar_width * dataset_count

				rect = self._create_element( 'rect', {
					'x': str(left),
					'y': str(top),
					'width': str(bar_width),
					'height': str(length),
					'class': 'fill%s' % dataset_count+1,
				} )
				self.graph.appendChild( rect )
				
				self.make_datapoint_text( left + bar_width/2.0, top-6, value )
