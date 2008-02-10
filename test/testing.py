import sys, os
from SVG import Plot
g = Plot.Plot( {
    'min_x_value': 0,
    'min_y_value': 0,
    'area_fill': True,
    'stagger_x_labels': True,
    'stagger_y_labels': True,
    'show_x_guidelines': True
    })
g.add_data( { 'data': [ 1, 25, 2, 30, 3, 45 ], 'title': 'series 1' } )
g.add_data( { 'data': [ 1,30, 2, 31, 3, 40 ], 'title': 'series 2' } )
g.add_data( { 'data': [ .5,35, 1, 20, 3, 10.5 ], 'title': 'series 3' } )
res = g.burn()
f = open( r'Plot.py.svg', 'w' )
f.write( res )
f.close()

from SVG import TimeSeries

g = TimeSeries.Plot( { } )

g.timescale_divisions = '4 hours'
g.stagger_x_labels = True
g.x_label_format = '%d-%b %H:%M'
g.max_y_value = 200

g.add_data( { 'data': [ '2005-12-21T00:00:00', 20, '2005-12-22T00:00:00', 21 ], 'title': 'series 1' } )

res = g.burn()
print g.field_width
print g.font_size
print g.right_font
print g.right_align
print g.get_x_labels()

f = open( r'TimeSeries.py.svg', 'w' )
f.write( res )
f.close()
