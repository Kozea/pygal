require 'SVG/Graph/Graph'
require 'SVG/Graph/Plot'

graph = SVG::Graph::Plot.new( {
	:min_x_value=>0,
	:min_y_value=>0,
	:area_fill=> true,
	:stagger_x_labels=>true,
	:stagger_y_labels=>true
})

#data1 = [ 1,25, 2,30, 3,45 ]

graph.add_data( { :data=>[ 1,25, 2,30, 3,45 ], :title=>'foo' } )

graph.add_data( { :data=>[ 1,30, 2, 31, 3, 40 ], :title=>'foo2' } )

res = graph.burn()

f = File.new( 'c:\ruby.svg', 'w' )
f.write( res )
f.close()

require 'SVG/Graph/TimeSeries'

g = SVG::Graph::TimeSeries.new( { } )
g.add_data( { :data=> [ '2005-12-21T00:00:00', 20, '2005-12-22T00:00:00', 21 ], :title=> 'foo' } )

res = g.burn()
f = File.new( 'c:\timeseries.rb.svg', 'w' )
f.write( res )
f.close()