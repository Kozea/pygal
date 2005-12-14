#!/usr/bin/env python

from xml.dom import minidom as dom

try:
	import zlib
	__have_zlib = True
except ImportError:
	__have_zlib = False

def CreateElement( nodeName, attributes={} ):
	"Create an XML node and set the attributes from a dict"
	node = dom.Element( nodeName )
	map( lambda a: node.setAttribute( *a ), attributes.items() )
	return node

class Graph( object ):
	"""=== Base object for generating SVG Graphs

== Synopsis

This class is only used as a superclass of specialized charts.  Do not
attempt to use this class directly, unless creating a new chart type.

For examples of how to subclass this class, see the existing specific
subclasses, such as SVG.Pie.

== Examples

For examples of how to use this package, see either the test files, or
the documentation for the specific class you want to use.

* file:test/plot.rb
* file:test/single.rb
* file:test/test.rb
* file:test/timeseries.rb

== Description

This package should be used as a base for creating SVG graphs.

== Acknowledgements

Sean E. Russel for creating the SVG::Graph Ruby package from which this
Python port is derived.

Leo Lapworth for creating the SVG::TT::Graph package which the Ruby
port is based on.

Stephen Morgan for creating the TT template and SVG.

== See

* SVG.BarHorizontal
* SVG.Bar
* SVG.Line
* SVG.Pie
* SVG.Plot
* SVG.TimeSeries

== Author

Jason R. Coombs <jaraco@jaraco.com>

Copyright 2005 Sandia National Laboratories
"""
	defaults = {
		'width':                500,
		'height':               300,
		'show_x_guidelines':    False,
		'show_y_guidelines':    True,
		'show_data_values':     True,
		'min_scale_value':      0,
		'show_x_labels':        True,
		'stagger_x_labels':     False,
		'rotate_x_labels':      False,
		'step_x_labels':        1,
		'step_include_first_x_label':   True,
		'show_y_labels':        True,
		'rotate_y_labels':		False,
		'stagger_y_labels':		False,
		'scale_integers':		False,
		'show_x_title':			False,
		'x_title':				'X Field names',
		'show_y_title':			False,
		'y_title_text_direction':	'bt',
		'y_title':				'Y Scale',
		'show_graph_title':		False,
		'graph_title':			'Graph Title',
		'show_graph_subtitle':	False,
		'graph_subtitle':		'Graph Subtitle',
		'key':					True,
		'key_position':			'right', # 'bottom' or 'right',
		
		'font_size':			12,
		'title_font_size':		16,
		'subtitle_font_size':	14,
		'x_label_font_size':	12,
		'x_title_font_size':	14,
		'y_label_font_size':	12,
		'y_title_font_size':	14,
		'key_font_size':		10,
		
		'no_css':				False,
		'add_popups':			False,
		}
	#__slots__ = tuple( defaults ) + ( '__dict__', '__weakref__' )

	def __init__( self, config ):
		"""Initialize the graph object with the graph settings.  You won't
instantiate this class directly; see the subclass for options.
"""
		self.top_align = self.top_font = self.right_align = self.right_font = 0
		self.load_config()
		self.load_config( config )
		self.clear_data()

	def load_config( self, config = None ):
		if not config: config = self.defaults
		map( lambda pair: setattr( self, *pair ), config.items() )
		
	def add_data( self, conf ):
		"""This method allows you do add data to the graph object.
It can be called several times to add more data sets in.

>>> data_sales_02 = [12, 45, 21]
>>> graph.add_data({
...  'data': data_sales_02,
...  'title': 'Sales 2002'
... })
"""
		try:
			assert( isinstance( conf['data'], ( tuple, list ) ) )
		except TypeError, e:
			raise TypeError, "conf should be dictionary with 'data' and other items"
		except AssertionError:
			if not hasattr( conf['data'], '__iter__' ):
				raise TypeError, "conf['data'] should be tuple or list or iterable"
			
		self.data.append( conf )
		
	def clear_data( self ):
		"""This method removes all data from the object so that you can
reuse it to create a new graph but with the same config options.

>>> graph.clear_data()
"""
		self.data = []
		
	def burn( self ):
		"""      # This method processes the template with the data and
config which has been set and returns the resulting SVG.

This method will croak unless at least one data set has
been added to the graph object.

Ex: graph.burn()
"""
		if not self.data: raise ValueError( "No data available" )
		
		if hasattr( self, 'calculations' ): self.calculations()
		
		self.start_svg()
		self.calculate_graph_dimensions()
		self.foreground = dom.Element( "g" )
		self.draw_graph()
		self.draw_titles()
		self.draw_legend()
		self.draw_data()
		self.graph.add_element( self.foreground )
		self.style()
		
		data = self._doc.toprettyxml()
		
		if self.compress:
			if __have_zlib:
				data = zlib.compress( data )
			else:
				data += '<!-- Python zlib not available for SVGZ -->'
				
		return data
	
	KEY_BOX_SIZE = 12
	
	def calculate_left_margin( self ):
		"""Override this (and call super) to change the margin to the left
of the plot area.  Results in border_left being set."""
		bl = 7
		# Check for Y labels
		if self.rotate_y_labels:
			max_y_label_height_px = self.y_label_font_size
		else:
			label_lengths = map( len, self.get_y_labels() )
			max_y_label_len = reduce( max, label_lengths )
			max_y_label_height_px = 0.6 * max_y_label_len * self.y_label_font_size
		if show_y_labels: bl += max_y_label_height_px
		if stagger_y_labels: bl += max_y_label_height_px + 10
		if show_y_title: bl += self.y_title_font_size + 5
		self.border_left = bl
		
	def max_y_label_width_px( self ):
		"""Calculates the width of the widest Y label.  This will be the
character height if the Y labels are rotated."""
		if self.rotate_y_labels:
			return self.font_size
		
	def calculate_right_margin( self ):
		"""Override this (and call super) to change the margin to the right
of the plot area.  Results in border_right being set."""
		br = 7
		if self.key and self.key_position == 'right':
			max_key_len = max( map( len, self.keys ) )
			br += max_key_len * self.key_font_size * 0.6
			br += self.KEY_BOX_SIZE
			br += 10		# Some padding around the box
		self.border_right = br
		
	def calculate_top_margin( self ):
		"""Override this (and call super) to change the margin to the top
of the plot area.  Results in border_top being set."""
		self.border_top = 5
		if self.show_graph_title: self.border_top += self.title_font_size
		self.border_top += 5
		if self.show_graph_subtitle: self.border_top += self.subtitle_font_size
		
	def add_popup( self, x, y, label ):
		"Adds pop-up point information to a graph."
		txt_width = len( label ) * self.font_size * 0.6 + 10
		tx = x + [5,-5](x+txt_width > width)
		t = dom.Element( 'text' )
		anchor = ['start', 'end'][x+txt_width > self.width]
		style = 'fill: #000; text-anchor: %s;' % anchor
		id = 'label-%s' % label
		attributes = { 'x': str( tx ),
					  'y': str( y - self.font_size ),
					  'visibility': 'hidden',
					  'style': style,
					  'text': label,
					  'id': id
					   }
		map( lambda a: t.setAttribute( *a ), attributes.items() )
		self.foreground.appendChild( t )
		
		visibility = "document.getElementById(%s).setAttribute('visibility', %%s )" % id
		t = dom.Element( 'circle' )
		attributes = { 'cx': str( x ),
					  'cy': str( y ),
					  'r': 10,
					  'style': 'opacity: 0;',
					  'onmouseover': visibility % 'visible',
					  'onmouseout': visibility % 'hidden',
		}
		map( lambda a: t.setAttribute( *a ), attributes.items() )

	def calculate_bottom_margin( self ):
		"""Override this (and call super) to change the margin to the bottom
of the plot area.  Results in border_bottom being set."""
		bb = 7
		if self.key and self.key_position == 'bottom':
			bb += len( self.data ) * ( self.font_size + 5 )
			bb += 10
		if self.show_x_labels:
			max_x_label_height_px = self.x_label_font_size
			if self.rotate_x_labels:
				label_lengths = map( len, self.get_x_labels() )
				max_x_label_len = reduce( max, label_lengths )
				max_x_label_height_px *= 0.6 * max_x_label_len
			bb += max_x_label_height_px
			if self.stagger_x_labels: bb += max_x_label_height_px + 10
		if self.show_x_title: bb += self.x_title_font_size + 5
		self.border_bottom = bb
		
	def draw_graph:
		transform = 'translate ( %s %s )' % ( self.border_left, self.border_top )
		self.graph = CreateElement( 'g', { 'transform': transform } )
		self.root.appendChild( self.graph )
		
		self.graph.appendChild( CreateElement( 'rect', {
			'x': '0',
			'y': '0',
			'width': str( self.graph_width )
			'height': str( self.graph_height )
			'class': 'graphBackground'
			} ) )
		
		#Axis
		self.graph.appendChild( CreateElement( 'path', {
			'd': 'M 0 0 v%s' % self.graph_height,
			'class': 'axis',
			'id': 'xAxis'
		} ) )
		self.graph.appendChild( CreateElement( 'path', {
			'd': 'M 0 %s h%s' % ( self.graph_height, self.graph_width ),
			'class': 'axis',
			'id': 'yAxis'
		} ) )
		
		self.draw_x_labels()
		self.draw_y_labels()
	
	def x_label_offset( self, width ):
		"""Where in the X area the label is drawn
Centered in the field, should be width/2.  Start, 0."""
		return 0

	def make_datapoint_text( self, x, y, value, style='' ):
		if self.show_data_values:
			e = CreateElement( 'text', {
				'x': str( x ),
				'y': str( y ),
				'class': 'dataPointLabel',
				'style': '%(style)s stroke: #fff; stroke-width: 2;' % vars(),
			} )
			e.nodeValue = value
			self.foreground.appendChild( e )

	def draw_x_labels( self ):
		"Draw the X axis labels"
		stagger = self.x_label_font_size + 5
		if self.show_x_labels:
			label_width = self.field_width
			
			labels = self.get_x_labels()
			count = len( labels )
			
			labels = enumerate( iter( labels ) )
			start = int( !self.step_include_first_x_label )
			labels = itertools.islice( labels, start, None, self.step_x_labels )
			map( self.draw_x_label, labels )
			self.draw_x_guidelines( label_width, count )
	
	def draw_x_label( self, label ):
		index, label = label
		text = CreateElement( 'text', { 'class': 'xAxisLabels' } )
		self.graph.appendChild( text )
		
	def start_svg( self ):
		"Base SVG Document Creation"
		impl = dom.getDOMImplementation()
		#dt = impl.createDocumentType( 'svg', 'PUBLIC'
		self._doc = impl.createDocument( None, 'svg', None )
		self.root = self._doc.getDocumentElement()
		
ruby = """      
      # Draws the background, axis, and labels.
      def draw_graph
        @graph = @root.add_element( "g", {
          "transform" => "translate( #@border_left #@border_top )"
        })

        # Background
        @graph.add_element( "rect", {
          "x" => "0",
          "y" => "0",
          "width" => @graph_width.to_s,
          "height" => @graph_height.to_s,
          "class" => "graphBackground"
        })

        # Axis
        @graph.add_element( "path", {
          "d" => "M 0 0 v#@graph_height",
          "class" => "axis",
          "id" => "xAxis"
        })
        @graph.add_element( "path", {
          "d" => "M 0 #@graph_height h#@graph_width",
          "class" => "axis",
          "id" => "yAxis"
        })

        draw_x_labels
        draw_y_labels
      end


      # Where in the X area the label is drawn
      # Centered in the field, should be width/2.  Start, 0.
      def x_label_offset( width )
        0
      end

      def make_datapoint_text( x, y, value, style="" )
        if show_data_values
          @foreground.add_element( "text", {
            "x" => x.to_s,
            "y" => y.to_s,
            "class" => "dataPointLabel",
            "style" => "#{style} stroke: #fff; stroke-width: 2;"
          }).text = value.to_s
          text = @foreground.add_element( "text", {
            "x" => x.to_s,
            "y" => y.to_s,
            "class" => "dataPointLabel"
          })
          text.text = value.to_s
          text.attributes["style"] = style if style.length > 0
        end
      end


      # Draws the X axis labels
      def draw_x_labels
        stagger = x_label_font_size + 5
        if show_x_labels
          label_width = field_width

          count = 0
          for label in get_x_labels
            if step_include_first_x_label == true then
              step = count % step_x_labels
            else
              step = (count + 1) % step_x_labels
            end

            if step == 0 then
              text = @graph.add_element( "text" )
              text.attributes["class"] = "xAxisLabels"
              text.text = label.to_s

              x = count * label_width + x_label_offset( label_width )
              y = @graph_height + x_label_font_size + 3
              t = 0 - (font_size / 2)

              if stagger_x_labels and count % 2 == 1
                y += stagger
                @graph.add_element( "path", {
                  "d" => "M#{x} #@graph_height v#{stagger}",
                  "class" => "staggerGuideLine"
                })
              end

              text.attributes["x"] = x.to_s
              text.attributes["y"] = y.to_s
              if rotate_x_labels
                text.attributes["transform"] = 
                  "rotate( 90 #{x} #{y-x_label_font_size} )"+
                  " translate( 0 -#{x_label_font_size/4} )"
                text.attributes["style"] = "text-anchor: start"
              else
                text.attributes["style"] = "text-anchor: middle"
              end
            end

            draw_x_guidelines( label_width, count ) if show_x_guidelines
            count += 1
          end
        end
      end


      # Where in the Y area the label is drawn
      # Centered in the field, should be width/2.  Start, 0.
      def y_label_offset( height )
        0
      end


      def field_width
        (@graph_width.to_f - font_size*2*right_font) /
           (get_x_labels.length - right_align)
      end


      def field_height
        (@graph_height.to_f - font_size*2*top_font) /
           (get_y_labels.length - top_align)
      end


      # Draws the Y axis labels
      def draw_y_labels
        stagger = y_label_font_size + 5
        if show_y_labels
          label_height = field_height

          count = 0
          y_offset = @graph_height + y_label_offset( label_height )
          y_offset += font_size/1.2 unless rotate_y_labels
          for label in get_y_labels
            y = y_offset - (label_height * count)
            x = rotate_y_labels ? 0 : -3

            if stagger_y_labels and count % 2 == 1
              x -= stagger
              @graph.add_element( "path", {
                "d" => "M#{x} #{y} h#{stagger}",
                "class" => "staggerGuideLine"
              })
            end

            text = @graph.add_element( "text", {
              "x" => x.to_s,
              "y" => y.to_s,
              "class" => "yAxisLabels"
            })
            text.text = label.to_s
            if rotate_y_labels
              text.attributes["transform"] = "translate( -#{font_size} 0 ) "+
                "rotate( 90 #{x} #{y} ) "
              text.attributes["style"] = "text-anchor: middle"
            else
              text.attributes["y"] = (y - (y_label_font_size/2)).to_s
              text.attributes["style"] = "text-anchor: end"
            end
            draw_y_guidelines( label_height, count ) if show_y_guidelines
            count += 1
          end
        end
      end


      # Draws the X axis guidelines
      def draw_x_guidelines( label_height, count )
        if count != 0
          @graph.add_element( "path", {
            "d" => "M#{label_height*count} 0 v#@graph_height",
            "class" => "guideLines"
          })
        end
      end


      # Draws the Y axis guidelines
      def draw_y_guidelines( label_height, count )
        if count != 0
          @graph.add_element( "path", {
            "d" => "M0 #{@graph_height-(label_height*count)} h#@graph_width",
            "class" => "guideLines"
          })
        end
      end


      # Draws the graph title and subtitle
      def draw_titles
        if show_graph_title
          @root.add_element( "text", {
            "x" => (width / 2).to_s,
            "y" => (title_font_size).to_s,
            "class" => "mainTitle"
          }).text = graph_title.to_s
        end

        if show_graph_subtitle
          y_subtitle = show_graph_title ? 
            title_font_size + 10 :
            subtitle_font_size
          @root.add_element("text", {
            "x" => (width / 2).to_s,
            "y" => (y_subtitle).to_s,
            "class" => "subTitle"
          }).text = graph_subtitle.to_s
        end

        if show_x_title
          y = @graph_height + @border_top + x_title_font_size
          if show_x_labels
            y += x_label_font_size + 5 if stagger_x_labels
            y += x_label_font_size + 5
          end
          x = width / 2

          @root.add_element("text", {
            "x" => x.to_s,
            "y" => y.to_s,
            "class" => "xAxisTitle",
          }).text = x_title.to_s
        end

        if show_y_title
          x = y_title_font_size + (y_title_text_direction==:bt ? 3 : -3)
          y = height / 2

          text = @root.add_element("text", {
            "x" => x.to_s,
            "y" => y.to_s,
            "class" => "yAxisTitle",
          })
          text.text = y_title.to_s
          if y_title_text_direction == :bt
            text.attributes["transform"] = "rotate( -90, #{x}, #{y} )"
          else
            text.attributes["transform"] = "rotate( 90, #{x}, #{y} )"
          end
        end
      end

      def keys 
        return @data.collect{ |d| d[:title] }
      end

      # Draws the legend on the graph
      def draw_legend
        if key
          group = @root.add_element( "g" )

          key_count = 0
          for key_name in keys
            y_offset = (KEY_BOX_SIZE * key_count) + (key_count * 5)
            group.add_element( "rect", {
              "x" => 0.to_s,
              "y" => y_offset.to_s,
              "width" => KEY_BOX_SIZE.to_s,
              "height" => KEY_BOX_SIZE.to_s,
              "class" => "key#{key_count+1}"
            })
            group.add_element( "text", {
              "x" => (KEY_BOX_SIZE + 5).to_s,
              "y" => (y_offset + KEY_BOX_SIZE).to_s,
              "class" => "keyText"
            }).text = key_name.to_s
            key_count += 1
          end

          case key_position
          when :right
            x_offset = @graph_width + @border_left + 10
            y_offset = @border_top + 20
          when :bottom
            x_offset = @border_left + 20
            y_offset = @border_top + @graph_height + 5
            if show_x_labels
              max_x_label_height_px = rotate_x_labels ? 
                get_x_labels.max{|a,b| 
                  a.length<=>b.length
                }.length * x_label_font_size :
                x_label_font_size
              y_offset += max_x_label_height_px
              y_offset += max_x_label_height_px + 5 if stagger_x_labels
            end
            y_offset += x_title_font_size + 5 if show_x_title
          end
          group.attributes["transform"] = "translate(#{x_offset} #{y_offset})"
        end
      end


      private

      def sort_multiple( arrys, lo=0, hi=arrys[0].length-1 )
        if lo < hi
          p = partition(arrys,lo,hi)
          sort_multiple(arrys, lo, p-1)
          sort_multiple(arrys, p+1, hi)
        end
        arrys 
      end

      def partition( arrys, lo, hi )
        p = arrys[0][lo]
        l = lo
        z = lo+1
        while z <= hi
          if arrys[0][z] < p
            l += 1
            arrys.each { |arry| arry[z], arry[l] = arry[l], arry[z] }
          end
          z += 1
        end
        arrys.each { |arry| arry[lo], arry[l] = arry[l], arry[lo] }
        l
      end

      def style
        if no_css
          styles = parse_css
          @root.elements.each("//*[@class]") { |el|
            cl = el.attributes["class"]
            style = styles[cl]
            style += el.attributes["style"] if el.attributes["style"]
            el.attributes["style"] = style
          }
        end
      end

      def parse_css
        css = get_style
        rv = {}
        while css =~ /^(\.(\w+)(?:\s*,\s*\.\w+)*)\s*\{/m
          names_orig = names = $1
          css = $'
          css =~ /([^}]+)\}/m
          content = $1
          css = $'

          nms = []
          while names =~ /^\s*,?\s*\.(\w+)/
            nms << $1
            names = $'
          end

          content = content.tr( "\n\t", " ")
          for name in nms
            current = rv[name]
            current = current ? current+"; "+content : content
            rv[name] = current.strip.squeeze(" ")
          end
        end
        return rv
      end


      # Override and place code to add defs here
      def add_defs defs
      end


      def start_svg
        # Base document
        @doc = Document.new
        @doc << XMLDecl.new
        @doc << DocType.new( %q{svg PUBLIC "-//W3C//DTD SVG 1.0//EN" } +
          %q{"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"} )
        if style_sheet && style_sheet != ''
          @doc << ProcessingInstruction.new( "xml-stylesheet",
            %Q{href="#{style_sheet}" type="text/css"} )
        end
        @root = @doc.add_element( "svg", {
          "width" => width.to_s,
          "height" => height.to_s,
          "viewBox" => "0 0 #{width} #{height}",
          "xmlns" => "http://www.w3.org/2000/svg",
          "xmlns:xlink" => "http://www.w3.org/1999/xlink",
          "xmlns:a3" => "http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/",
          "a3:scriptImplementation" => "Adobe"
        })
        @root << Comment.new( " "+"\\"*66 )
        @root << Comment.new( " Created with SVG::Graph " )
        @root << Comment.new( " SVG::Graph by Sean E. Russell " )
        @root << Comment.new( " Losely based on SVG::TT::Graph for Perl by"+
        " Leo Lapworth & Stephan Morgan " )
        @root << Comment.new( " "+"/"*66 )

        defs = @root.add_element( "defs" )
        add_defs defs
        if not(style_sheet && style_sheet != '') and !no_css
          @root << Comment.new(" include default stylesheet if none specified ")
          style = defs.add_element( "style", {"type"=>"text/css"} )
          style << CData.new( get_style )
        end

        @root << Comment.new( "SVG Background" )
        @root.add_element( "rect", {
          "width" => width.to_s,
          "height" => height.to_s,
          "x" => "0",
          "y" => "0",
          "class" => "svgBackground"
        })
      end


      def calculate_graph_dimensions
        calculate_left_margin
        calculate_right_margin
        calculate_bottom_margin
        calculate_top_margin
        @graph_width = width - @border_left - @border_right
        @graph_height = height - @border_top - @border_bottom
      end

      def get_style
        return <<EOL
/* Copy from here for external style sheet */
.svgBackground{
  fill:#ffffff;
}
.graphBackground{
  fill:#f0f0f0;
}

/* graphs titles */
.mainTitle{
  text-anchor: middle;
  fill: #000000;
  font-size: #{title_font_size}px;
  font-family: "Arial", sans-serif;
  font-weight: normal;
}
.subTitle{
  text-anchor: middle;
  fill: #999999;
  font-size: #{subtitle_font_size}px;
  font-family: "Arial", sans-serif;
  font-weight: normal;
}

.axis{
  stroke: #000000;
  stroke-width: 1px;
}

.guideLines{
  stroke: #666666;
  stroke-width: 1px;
  stroke-dasharray: 5 5;
}

.xAxisLabels{
  text-anchor: middle;
  fill: #000000;
  font-size: #{x_label_font_size}px;
  font-family: "Arial", sans-serif;
  font-weight: normal;
}

.yAxisLabels{
  text-anchor: end;
  fill: #000000;
  font-size: #{y_label_font_size}px;
  font-family: "Arial", sans-serif;
  font-weight: normal;
}

.xAxisTitle{
  text-anchor: middle;
  fill: #ff0000;
  font-size: #{x_title_font_size}px;
  font-family: "Arial", sans-serif;
  font-weight: normal;
}

.yAxisTitle{
  fill: #ff0000;
  text-anchor: middle;
  font-size: #{y_title_font_size}px;
  font-family: "Arial", sans-serif;
  font-weight: normal;
}

.dataPointLabel{
  fill: #000000;
  text-anchor:middle;
  font-size: 10px;
  font-family: "Arial", sans-serif;
  font-weight: normal;
}

.staggerGuideLine{
  fill: none;
  stroke: #000000;
  stroke-width: 0.5px;  
}

#{get_css}

.keyText{
  fill: #000000;
  text-anchor:start;
  font-size: #{key_font_size}px;
  font-family: "Arial", sans-serif;
  font-weight: normal;
}
/* End copy for external style sheet */
EOL
      end

    end
  end
end
"""