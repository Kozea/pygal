# -*- coding: utf-8 -*-

"""
pygal.graph

The base module for `pygal` classes.
"""

from operator import itemgetter
from itertools import islice
from logging import getLogger
import os

from lxml import etree
from pygal.util import node
from pygal.util.boundary import (calculate_right_margin, calculate_left_margin,
                                 calculate_bottom_margin, calculate_top_margin,
                                 calculate_offsets_bottom)

log = getLogger('pygal')


def sort_multiple(arrays):
    "sort multiple lists (of equal size) "
    "using the first list for the sort keys"
    tuples = zip(*arrays)
    tuples.sort()
    return zip(*tuples)


class Graph(object):
    """
    Base object for generating SVG Graphs

        This class is only used as a superclass of specialized charts.  Do not
    attempt to use this class directly, unless creating a new chart type.

        For examples of how to subclass this class, see the existing specific
    subclasses, such as svn.charts.Pie.

    * pygal.bar
    * pygal.line
    * pygal.pie
    * pygal.plot
    * pygal.time_series

    """
    ratio = .7
    width = 600
    show_x_guidelines = False
    show_y_guidelines = True
    show_data_values = True
    min_scale_value = None
    show_x_labels = True
    stagger_x_labels = False
    x_label_rotation = 0
    step_x_labels = 1
    step_include_first_x_label = True
    show_y_labels = True
    rotate_y_labels = False
    stagger_y_labels = False
    step_include_first_y_label = True
    step_y_labels = 1
    scale_integers = False
    show_x_title = False
    x_title = 'X Field names'
    show_y_title = False
    # 'bt' for bottom to top; 'tb' for top to bottom
    y_title_text_direction = 'bt'
    y_title = 'Y Scale'
    show_graph_title = False
    graph_title = 'Graph Title'
    show_graph_subtitle = False
    graph_subtitle = 'Graph Subtitle'
    key = True
    # 'bottom' or 'right',
    key_position = 'right'

    font_size = 12
    title_font_size = 16
    subtitle_font_size = 14
    x_label_font_size = 12
    x_title_font_size = 14
    y_label_font_size = 12
    y_title_font_size = 14
    key_font_size = 10
    key_box_size = 10
    add_popups = False

    top_align = top_font = right_align = right_font = 0
    stylesheet_names = ['graph.css']
    compress = False
    colors = [
        "#2a4269", "#476fb2", "#38588e", "#698bc3",
        "#69c38b", "#588e38", "#47b26f", "#42692a",
        "#1a3259", "#375fa2", "#28487e", "#597bb3",
        "#59b37b", "#487e28", "#37a25f", "#32591a"]

    def __init__(self, config={}):
        """Initialize the graph object with the graph settings."""
        if self.__class__ is Graph:
            raise NotImplementedError("Graph is an abstract base class")
        self.load_config(config)
        self.clear_data()

    @property
    def height(self):
        return int(self.width * self.ratio)

    def load_config(self, config):
        self.__dict__.update(config)

    def add_data(self, conf):
        """
        Add data to the graph object. May be called several times to add
        additional data sets.

        >>> data_sales_02 = [12, 45, 21] # doctest: +SKIP
        >>> graph.add_data({ # doctest: +SKIP
        ...  'data': data_sales_02,
        ...  'title': 'Sales 2002'
        ... }) # doctest: +SKIP
        """
        self.validate_data(conf)
        self.process_data(conf)
        self.data.append(conf)

    def validate_data(self, conf):
        try:
            assert(isinstance(conf['data'], (tuple, list)))
        except TypeError:
            raise TypeError(
                "conf should be dictionary with 'data' and other items")
        except AssertionError:
            if not hasattr(conf['data'], '__iter__'):
                raise TypeError(
                    "conf['data'] should be tuple or list or iterable")

    def process_data(self, data):
        pass

    def clear_data(self):
        """
        This method removes all data from the object so that you can
        reuse it to create a new graph but with the same config options.

        >>> graph.clear_data() # doctest: +SKIP
        """
        self.data = []

    def burn(self):
        """
        Process the template with the data and
        config which has been set and return the resulting SVG.

        Raises ValueError when no data set has
        been added to the graph object.
        """

        log.info("Burning %s graph" % self.__class__.__name__)

        if not self.data:
            raise ValueError("No data available")

        if hasattr(self, 'calculations'):
            self.calculations()

        self.start_svg()
        self.calculate_graph_dimensions()
        self.foreground = etree.Element("g")

        self.draw_graph()
        self.draw_titles()
        self.draw_legend()
        self.draw_data()

        self.graph.append(self.foreground)

        data = etree.tostring(
            self.root, pretty_print=True,
            xml_declaration=True, encoding='utf-8')
        if self.compress:
            import zlib
            data = zlib.compress(data)

        return data

    def max_y_label_width_px(self):
        """
        Calculate the width of the widest Y label.  This will be the
        character height if the Y labels are rotated.
        """
        if self.rotate_y_labels:
            return self.font_size

    def draw_graph(self):
        """
        The central logic for drawing the graph.

        Sets self.graph (the 'g' element in the SVG root)
        """
        transform = 'translate (%s %s)' % (self.border_left, self.border_top)
        self.graph = node(self.root, 'g', transform=transform)
        self.back = node(self.graph, 'g', {'class': 'back'})
        node(self.back, 'rect', {
            'x': 0,
            'y': 0,
            'width': self.graph_width,
            'height': self.graph_height,
            'class': 'graphBackground'
            })

        #Axis
        node(self.foreground, 'path', {
            'd': 'M 0 0 v%s' % self.graph_height,
            'class': 'axis',
            'id': 'xAxis'
        })
        node(self.foreground, 'path', {
            'd': 'M 0 %s h%s' % (self.graph_height, self.graph_width),
            'class': 'axis',
            'id': 'yAxis'
        })

        self.draw_x_labels()
        self.draw_y_labels()

    def make_datapoint_text(self, group, x, y, value, style=None):
        """
        Add text for a datapoint
        """
        if not self.show_data_values:
            return

        e = node(group, 'text', {
            'x': x,
            'y': y,
            'class': 'dataPointLabel'})
        e.text = str(value)
        if style:
            e.set('style', style)

    def x_label_offset(self, width):
        return 0

    def draw_x_labels(self):
        "Draw the X axis labels"
        if not self.show_x_labels:
            return

        log.debug("Drawing x labels")
        self.xlabels = node(self.graph, 'g', {'class': 'xLabels'})
        labels = self.get_x_labels()
        count = len(labels)
        labels = enumerate(iter(labels))
        start = int(not self.step_include_first_x_label)
        labels = islice(labels, start, None, self.step_x_labels)
        map(self.draw_x_label, labels)
        self.draw_x_guidelines(self.field_width(), count)

    def draw_x_label(self, label):
        label_width = self.field_width()
        index, label = label
        text = node(self.xlabels, 'text', {'class': 'xAxisLabels'})
        text.text = label

        x = index * label_width + self.x_label_offset(label_width)
        y = self.graph_height + self.x_label_font_size + 3

        if self.stagger_x_labels and (index % 2):
            stagger = self.x_label_font_size + 5
            y += stagger
            graph_height = self.graph_height
            node(self.xlabels, 'path', {
                'd': 'M%f %f v%d' % (x, graph_height, stagger),
                'class': 'staggerGuideLine'
            })

        text.set('x', str(x))
        text.set('y', str(y))

        if self.x_label_rotation:
            transform = 'rotate(%d %d %d) translate(0 -%d)' % \
                (-self.x_label_rotation, x, y - self.x_label_font_size,
                 self.x_label_font_size / 4)
            text.set('transform', transform)
            text.set('style', 'text-anchor: end')
        else:
            text.set('style', 'text-anchor: middle')

    def y_label_offset(self, height):
        """
        Return an offset for drawing the y label. Currently returns 0.
        """
        # Consider height/2 to center within the field.
        return 0

    def get_field_width(self):
        divisor = (len(self.get_x_labels()) - self.right_align)
        if divisor == 0:
            return 0
        return float(
            self.graph_width - self.font_size * 2 * self.right_font) / divisor
    field_width = get_field_width

    def get_field_height(self):
        divisor = (len(self.get_y_labels()) - self.top_align)
        if divisor == 0:
            return 0
        return float(
            self.graph_height - self.font_size * 2 * self.top_font) / divisor
    field_height = get_field_height

    def draw_y_labels(self):
        "Draw the Y axis labels"
        if not self.show_y_labels:
            return
        log.debug("Drawing y labels")

        self.ylabels = node(self.graph, 'g', {'class': 'yLabels'})
        labels = self.get_y_labels()
        count = len(labels)

        labels = enumerate(iter(labels))
        start = int(not self.step_include_first_y_label)
        labels = islice(labels, start, None, self.step_y_labels)
        map(self.draw_y_label, labels)
        self.draw_y_guidelines(self.field_height(), count)

    def get_y_offset(self):
        result = self.graph_height + self.y_label_offset(self.field_height())
        if not self.rotate_y_labels:
            result += self.font_size / 1.2
        return result
    y_offset = property(get_y_offset)

    def draw_y_label(self, label):
        label_height = self.field_height()
        index, label = label
        text = node(self.ylabels, 'text', {'class': 'yAxisLabels'})
        text.text = label

        y = self.y_offset - (label_height * index)
        x = {True: 0, False: -3}[self.rotate_y_labels]

        if self.stagger_y_labels and  (index % 2):
            stagger = self.y_label_font_size + 5
            x -= stagger
            node(self.ylabels, 'path', {
                'd': 'M%f %f h%d' % (x, y, stagger),
                'class': 'staggerGuideLine'
            })

        text.set('x', str(x))
        text.set('y', str(y))

        if self.rotate_y_labels:
            transform = 'translate(-%d 0) rotate (90 %d %d)' % \
                (self.font_size, x, y)
            text.set('transform', transform)
            text.set('style', 'text-anchor: middle')
        else:
            text.set('y', str(y - self.y_label_font_size / 2))
            text.set('style', 'text-anchor: end')

    def draw_x_guidelines(self, label_height, count):
        "Draw the X-axis guidelines"
        if not self.show_x_guidelines:
            return
        log.debug("Drawing x guidelines")
        self.xguidelines = node(self.graph, 'g', {'class': 'xGuideLines'})
        # skip the first one
        for count in range(1, count):
            start = label_height * count
            stop = self.graph_height
            node(self.xguidelines, 'path', {
                'd': 'M %s 0 v%s' % (start, stop),
                'class': 'guideLines'})

    def draw_y_guidelines(self, label_height, count):
        "Draw the Y-axis guidelines"
        if not self.show_y_guidelines:
            return
        log.debug("Drawing y guidelines")
        self.yguidelines = node(self.graph, 'g', {'class': 'yGuideLines'})
        for count in range(1, count):
            start = self.graph_height - label_height * count
            stop = self.graph_width
            node(self.yguidelines, 'path', {
                'd': 'M 0 %s h%s' % (start, stop),
                'class': 'guideLines'})

    def draw_titles(self):
        "Draws the graph title and subtitle"
        log.debug("Drawing titles")
        if self.show_graph_title:
            self.draw_graph_title()
        if self.show_graph_subtitle:
            self.draw_graph_subtitle()
        if self.show_x_title:
            self.draw_x_title()
        if self.show_y_title:
            self.draw_y_title()

    def draw_graph_title(self):
        text = node(self.root, 'text', {
            'x': self.width / 2,
            'y': self.title_font_size,
            'class': 'mainTitle'})
        text.text = self.graph_title

    def draw_graph_subtitle(self):
        y_subtitle_options = [self.subtitle_font_size,
                              self.title_font_size + 10]
        y_subtitle = y_subtitle_options[self.show_graph_title]
        text = node(self.root, 'text', {
            'x': self.width / 2,
            'y': y_subtitle,
            'class': 'subTitle',
            })
        text.text = self.graph_title

    def draw_x_title(self):
        log.debug("Drawing x title")
        y = self.graph_height + self.border_top + self.x_title_font_size
        if self.show_x_labels:
            y_size = self.x_label_font_size + 5
            if self.stagger_x_labels:
                y_size *= 2
            y += y_size
        x = self.width / 2

        text = node(self.root, 'text', {
            'x': x,
            'y': y,
            'class': 'xAxisTitle',
            })
        text.text = self.x_title

    def draw_y_title(self):
        log.debug("Drawing y title")
        x = self.y_title_font_size
        if self.y_title_text_direction == 'bt':
                x += 3
                rotate = -90
        else:
                x -= 3
                rotate = 90
        y = self.height / 2
        text = node(self.root, 'text', {
            'x': x,
            'y': y,
            'class': 'yAxisTitle',
        })
        text.text = self.y_title
        text.set('transform', 'rotate(%d, %s, %s)' % (rotate, x, y))

    def keys(self):
        return map(itemgetter('title'), self.data)

    def draw_legend(self):
        if not self.key:
            return
        log.debug("Drawing legend")

        group = node(self.root, 'g')

        for key_count, key_name in enumerate(self.keys()):
            y_offset = (self.key_box_size * key_count) + (key_count * 5)
            node(group, 'rect', {
                'x': 0,
                'y': y_offset,
                'width': self.key_box_size,
                'height': self.key_box_size,
                'class': 'key key%s' % key_count,
            })
            text = node(group, 'text', {
                'x': self.key_box_size + 5,
                'y': y_offset + self.key_box_size,
                'class': 'keyText'})
            text.text = key_name

        if self.key_position == 'right':
            x_offset = self.graph_width + self.border_left + 10
            y_offset = self.border_top + 20
        if self.key_position == 'bottom':
            x_offset, y_offset = calculate_offsets_bottom(self)
        group.set('transform', 'translate(%d %d)' % (x_offset, y_offset))

    def add_defs(self, defs):
        """
        Override and place code to add defs here. TODO: what are defs?
        """
        for id in range(len(self.colors)):
            idn = 'line-color-%d' % id
            light = node(defs, 'linearGradient', {
                'id': idn,
                'x1': 0,
                'x2': '50%',
                'y1': 0,
                'y2': '100%'})
            node(light, 'stop',
                 {'class': 'upGradientLight %s' % idn, 'offset': 0})
            node(light, 'stop',
                 {'class': 'downGradientLight %s' % idn, 'offset': '100%'})

        shadow = node(defs, 'linearGradient', {
            'id': 'shadow',
            'x1': 0,
            'x2': '100%',
            'y1': 0,
            'y2': 0})
        node(shadow, 'stop',
             {'offset': 0, 'stop-color': '#aaa', 'stop-opacity': 0.7})
        node(shadow, 'stop',
             {'offset': '1%', 'stop-color': '#fff', 'stop-opacity': 1})
        node(shadow, 'stop',
             {'offset': '99%', 'stop-color': '#fff', 'stop-opacity': 1})
        node(shadow, 'stop',
             {'offset': '100%', 'stop-color': '#aaa', 'stop-opacity': .7})

    def start_svg(self):
        "Base SVG Document Creation"
        log.debug("Creating root node")
        svg_ns = 'http://www.w3.org/2000/svg'
        nsmap = {
            None: svg_ns,
            'xlink': 'http://www.w3.org/1999/xlink',
            }
        self.root = etree.Element("{%s}svg" % svg_ns, attrib={
            'viewBox': '0 0 %d %d' % (self.width, self.height)
            }, nsmap=nsmap)

        if hasattr(self, 'style_sheet_href'):
            pi = etree.ProcessingInstruction(
                'xml-stylesheet',
                'href="%s" type="text/css"' % self.style_sheet_href
                )
            self.root.addprevious(pi)

        comment_strings = (
            u'Generated with pygal ©Kozea 2011',
            'Based upon SVG.Graph by Jason R. Coombs',
        )
        map(self.root.append, map(etree.Comment, comment_strings))

        defs = node(self.root, 'defs')
        self.add_defs(defs)

        if not hasattr(self, 'style_sheet_href'):
            self.root.append(etree.Comment(
                ' include default stylesheet if none specified '))
            style = node(defs, 'style', type='text/css')
            style.text = ''
            opts = self.__dict__.copy()
            opts.update(Graph.__dict__)
            opts.update(self.__class__.__dict__)
            for stylesheet in self.stylesheet_names:
                with open(
                    os.path.join(os.path.dirname(__file__), 'css',
                                 stylesheet)) as f:
                    style.text += f.read() % opts
            for n, color in enumerate(self.colors):
                style.text += (
"""
.key%d, .fill%d, .dot%d {
    fill: url(#line-color-%d);
}
.key%d, .line%d {
    stroke: url(#line-color-%d);
}

.line-color-%d {
  stop-color: %s;
}

""" % (n, n, n, n, n, n, n, n, color))

        if hasattr(self, 'stylesheet_file'):
            with open(self.stylesheet_file) as f:
                style.text += f.read() % opts

        self.root.append(etree.Comment('SVG Background'))
        node(self.root, 'rect', {
            'width': self.width,
            'height': self.height,
            'x': 0,
            'y': 0,
            'class': 'svgBackground'})

    def calculate_graph_dimensions(self):
        log.debug("Computing sizes")
        self.border_right = calculate_right_margin(self)
        self.border_top = calculate_top_margin(self)
        self.border_left = calculate_left_margin(self)
        self.border_bottom = calculate_bottom_margin(self)

        self.graph_width = self.width - self.border_left - self.border_right
        self.graph_height = self.height - self.border_top - self.border_bottom
