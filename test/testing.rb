require 'SVG/Graph/Graph'
require 'SVG/Graph/Plot'

g = SVG::Graph::Plot.new( {
	:min_x_value=>0,
	:min_y_value=>0,
	:area_fill=> true,
	:stagger_x_labels=>true,
	:stagger_y_labels=>true,
	:show_x_guidelines=>true,
})

g.add_data( { :data=>[ 1, 25, 2, 30, 3, 45 ], :title=>'series 1' } )
g.add_data( { :data=>[ 1, 30, 2, 31, 3, 40 ], :title=>'series 2' } )
g.add_data( { :data=>[ 0.5, 35, 1, 20, 3, 10.5], :title=>'series 3' } )

res = g.burn()

f = File.new( 'Plot.rb.svg', 'w' )
f.write( res )
f.close()

require 'SVG/Graph/TimeSeries'

g = SVG::Graph::TimeSeries.new( {
								   :timescale_divisions => '4 hours',
								   :stagger_x_labels => true,
								   :x_label_format => '%d-%b %H:%M',
								   :max_y_value => 200,
							   } )
g.add_data( { :data=> [ '2005-12-21T00:00:00', 20, '2005-12-22T00:00:00', 21 ], :title=> 'series 1' } )

res = g.burn()

f = File.new( 'TimeSeries.rb.svg', 'w' )
f.write( res )
f.close()

require 'SVG/Graph/Bar'

fields = ['Internet', 'TV', 'Newspaper', 'Magazine', 'Radio']

g = SVG::Graph::Bar.new( {
							:scale_integers=>true,
							:stack=>:side,
							:width=>640,
							:height=>480,
							:fields=>fields,
							:graph_title=>'Question 7',
							:show_graph_title=>true,
							:no_css=>false
})

g.add_data({:data=>[-2,3,1,3,1], :title=>'Female'})
g.add_data({:data=>[0,2,1,5,4], :title=>'Male'})

f = File.new('VerticalBar.rb.svg', 'w')
f.write(g.burn())
f.close()

g = SVG::Graph::Bar.new({
	:scale_integers=>true,
	:stack=>:side,
	:width=>640,
	:height=>480,
	:fields=>fields,
	:graph_title=>'Question 8',
	:show_graph_title=>true,
	:no_css=>false,
})

g.add_data({:data=>[2,22,98,143,82], :title=>'intermediate'})
g.add_data({:data=>[2,26,106,193,105], :title=>'old'})

f = File.new('VerticalBarLarge.rb.svg', 'w')
f.write(g.burn())
f.close()

require 'SVG/Graph/Pie'

g = SVG::Graph::Pie.new({
	:width=>640,
	:height=>480,
	:fields=>fields,
	:graph_title=>'Question 7',
	:expand_greatest=>true,
	:show_data_labels=>true,
})

g.add_data({:data=>[-2,3,1,3,1], :title=>'Female'})
g.add_data({:data=>[0,2,1,5,4], :title=>'Male'})

f = File.new('Pie.rb.svg', 'w')
f.write(g.burn())
f.close()

