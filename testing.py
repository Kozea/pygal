import sys, os
sys.path.insert( 0, 'c:\documents and settings\jaraco\my documents\projects\jaraco' )
import SVG
from SVG import Plot
reload( SVG )
reload( Plot )
g = Plot.Plot({})
data1 = [ 1, 25, 2, 30, 3, 45 ]
g.add_data( { 'data': data1, 'title': 'foo' } )
res = g.burn()
f = open( r'c:\sample.svg', 'w' )
f.write( res )
f.close()
