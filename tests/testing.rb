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

require 'SVG/Graph/BarHorizontal'

g = SVG::Graph::BarHorizontal.new( {
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

f = File.new('HorizontalBar.rb.svg', 'w')
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

require 'SVG/Graph/Line'
g = SVG::Graph::Line.new( {
							:scale_integers=>true,
							:area_fill=>true,
							:width=>640,
							:height=>480,
							:fields=>fields,
							:graph_title=>'Question 7',
							:show_graph_title=>true,
							:no_css=>false
})

g.add_data({:data=>[-2,3,1,3,1], :title=>'Female'})
g.add_data({:data=>[0,2,1,5,4], :title=>'Male'})

f = File.new('Line.rb.svg', 'w')
f.write(g.burn())
f.close()

require 'SVG/Graph/Schedule'


title = "Billy's Schedule"
data1 = [
  "History 107", "5/19/04", "6/30/04",
  "Algebra 011", "6/2/04", "8/11/04",
  "Psychology 101", "6/28/04", "8/9/04",
  "Acting 105", "7/7/04", "8/16/04"
  ]
title2 = "Another Schedule"
data2 = [
	"Just one period", "5/19/04", "6/30/04"
]

g = SVG::Graph::Schedule.new( {
  :width => 640,
  :height => 480,
  :graph_title => title,
  :show_graph_title => true,
#  :no_css => true,
  :key => false,
  :scale_x_integers => true,
  :scale_y_integers => true,
  :show_data_labels => true,
  :show_y_guidelines => false,
  :show_x_guidelines => true,
  :show_x_title => true,
  :x_title => "Time",
  :show_y_title => false,
  :rotate_x_labels => true,
  :rotate_y_labels => false,
  :x_label_format => "%m/%d",
#  :timescale_divisions => "1 weeks",
  :add_popups => true,
  :popup_format => "%m/%d/%y",
  :area_fill => true,
  :min_y_value => 0,
})

g.add_data( 
  :data => data1,
  :title => "Data"
  )
g.add_data(
	:data => data2,
	:title => title2
)

f = File.new('Schedule.rb.svg', 'w')
f.write(g.burn())
f.close()
