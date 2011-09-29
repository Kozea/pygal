# -*- coding: utf-8 -*-
from itertools import chain
from lxml import etree
from pygal.graph import Graph
from pygal.util import node

__all__ = ('VerticalBar', 'HorizontalBar')


class Bar(Graph):
    "A superclass for bar-style graphs.  Do not instantiate directly."

    # gap between bars
    bar_gap = True
    # how to stack adjacent dataset series
    # overlap - overlap bars with transparent colors
    # top - stack bars on top of one another
    # side - stack bars side-by-side
    stack = 'side'

    scale_divisions = None

    stylesheet_names = Graph.stylesheet_names + ['bar.css']

    def __init__(self, fields, *args, **kargs):
        self.fields = fields
        super(Bar, self).__init__(*args, **kargs)

    # adapted from Plot
    def get_data_values(self):
        min_value, max_value, scale_division = self.data_range()
        result = tuple(
            float_range(min_value, max_value + scale_division, scale_division))
        if self.scale_integers:
            result = map(int, result)
        return result

    # adapted from plot (very much like calling data_range('y'))
    def data_range(self):
        min_value = self.data_min()
        max_value = self.data_max()
        range = max_value - min_value

        data_pad = range / 20.0 or 10
        scale_range = (max_value + data_pad) - min_value

        scale_division = self.scale_divisions or (scale_range / 10.0)

        if self.scale_integers:
            scale_division = round(scale_division) or 1

        return min_value, max_value, scale_division

    def get_field_labels(self):
        return self.fields

    def get_data_labels(self):
        return map(str, self.get_data_values())

    def data_max(self):
        return max(chain(*map(lambda set: set['data'], self.data)))
        # above is same as
        # return max(map(lambda set: max(set['data']), self.data))

    def data_min(self):
        if not getattr(self, 'min_scale_value') is None:
            return self.min_scale_value
        min_value = min(chain(*map(lambda set: set['data'], self.data)))
        min_value = min(min_value, 0)
        return min_value

    def get_bar_gap(self, field_size):
        bar_gap = 10  # default gap
        if field_size < 10:
            # adjust for narrow fields
            bar_gap = field_size / 2
        # the following zero's out the gap if bar_gap is False
        bar_gap = int(self.bar_gap) * bar_gap
        return bar_gap


def float_range(start=0, stop=None, step=1):
    "Much like the built-in function range, but accepts floats"
    while start < stop:
        yield float(start)
        start += step


class VerticalBar(Bar):
    """ Vertical bar graph """
    top_align = top_font = 1

    def add_defs(self, defs):
        """
        Override and place code to add defs here. TODO: what are defs?
        """
        for id in range(12):
            idn = 'light%d' % (id + 1)
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
             {'offset': '2%', 'stop-color': '#fff', 'stop-opacity': 0})
        node(shadow, 'stop',
             {'offset': '98%', 'stop-color': '#fff', 'stop-opacity': 0})
        node(shadow, 'stop',
             {'offset': '100%', 'stop-color': '#aaa', 'stop-opacity': .7})

    def get_x_labels(self):
        return self.get_field_labels()

    def get_y_labels(self):
        return self.get_data_labels()

    def x_label_offset(self, width):
        return width / 2.0

    def draw_data(self):
        min_value = self.data_min()
        unit_size = (
            float(self.graph_height) - self.font_size * 2 * self.top_font)
        unit_size /= (
            max(self.get_data_values()) - min(self.get_data_values()))

        bar_gap = self.get_bar_gap(self.get_field_width())

        bar_width = self.get_field_width() - bar_gap
        if self.stack == 'side':
            bar_width /= len(self.data)

        x_mod = (self.graph_width - bar_gap) / 2
        if self.stack == 'side':
            x_mod -= bar_width / 2

        bottom = self.graph_height

        for field_count, field in enumerate(self.fields):
            for dataset_count, dataset in enumerate(self.data):
                # cases (assume 0 = +ve):
                #   value  min  length
                #    +ve   +ve  value - min
                #    +ve   -ve  value - 0
                #    -ve   -ve  value.abs - 0
                value = dataset['data'][field_count]

                left = self.get_field_width() * field_count

                length = (abs(value) - max(min_value, 0)) * unit_size
                # top is 0 if value is negative
                top = bottom - ((max(value, 0) - min_value) * unit_size)
                if self.stack == 'side':
                    left += bar_width * dataset_count

                rect_group = node(self.graph, "g",
                                              {'class': 'bar'})
                node(rect_group, 'rect', {
                    'x': left,
                    'y': top,
                    'width': bar_width,
                    'height': length,
                    'class': 'fill fill%s' % (dataset_count + 1),
                })

                self.make_datapoint_text(
                    rect_group, left + bar_width / 2.0, top - 6, value)


class HorizontalBar(Bar):
    """ Horizontal bar graph """
    rotate_y_labels = True
    show_x_guidelines = True
    show_y_guidelines = False
    right_align = right_font = True

    def get_x_labels(self):
        return self.get_data_labels()

    def get_y_labels(self):
        return self.get_field_labels()

    def y_label_offset(self, height):
        return height / -2.0

    def draw_data(self):
        min_value = self.data_min()

        unit_size = float(self.graph_width)
        unit_size -= self.font_size * 2 * self.right_font
        unit_size /= max(self.get_data_values()) - min(self.get_data_values())

        bar_gap = self.get_bar_gap(self.get_field_height())

        bar_height = self.get_field_height() - bar_gap
        if self.stack == 'side':
            bar_height /= len(self.data)

        y_mod = (bar_height / 2) + (self.font_size / 2)

        for field_count, field in enumerate(self.fields):
            for dataset_count, dataset in enumerate(self.data):
                value = dataset['data'][field_count]

                top = self.graph_height - (
                    self.get_field_height() * (field_count + 1))
                if self.stack == 'side':
                    top += (bar_height * dataset_count)
                # cases (assume 0 = +ve):
                #   value  min  length          left
                #    +ve   +ve  value.abs - min minvalue.abs
                #    +ve   -ve  value.abs - 0   minvalue.abs
                #    -ve   -ve  value.abs - 0   minvalue.abs + value
                length = (abs(value) - max(min_value, 0)) * unit_size
                # left is 0 if value is negative
                left = (abs(min_value) + min(value, 0)) * unit_size

                node(self.graph, 'rect', {
                    'x': left,
                    'y': top,
                    'width': length,
                    'height': bar_height,
                    'class': 'fill fill%s' % (dataset_count + 1),
                })

                self.make_datapoint_text(
                    left + length + 5, top + y_mod, value,
                    "text-anchor: start; ")
