import sys, os
sys.path.insert( 0, 'c:\documents and settings\jaraco\my documents\projects\jaraco' )
import SVG
from SVG import Plot
reload( SVG )
reload( Plot )
g = Plot.Plot( {
    'min_x_value': 0,
    'min_y_value': 0,
    'area_fill': True,
    'stagger_x_labels': True,
    'stagger_y_labels': True,
    'show_x_guidelines': True
    })
g.add_data( { 'data': [ 1, 25, 2, 30, 3, 45 ], 'title': 'foo' } )
g.add_data( { 'data': [ 1,30, 2, 31, 3, 40 ], 'title': 'foo2' } )
g.add_data( { 'data': [ .5,35, 1, 20, 3, 10.5 ], 'title': 'foo2' } )
res = g.burn()
f = open( r'c:\sample.svg', 'w' )
f.write( res )
f.close()

from SVG import TimeSeries
reload( TimeSeries )

g = TimeSeries.Plot( { } )
#g.timescale_divisions = '4 hours'
g.stagger_x_labels = True
g.add_data( { 'data': [ '2005-12-21T00:00:00', 20, '2005-12-22T00:00:00', 21 ], 'title': 'foo' } )

res = g.burn()
f = open( r'c:\timeseries.py.svg', 'w' )
f.write( res )
f.close()
