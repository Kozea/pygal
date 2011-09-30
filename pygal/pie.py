import math
import itertools
from pygal.util import node
from pygal.graph import Graph


def robust_add(a, b):
    "Add numbers a and b, treating None as 0"
    if a is None:
        a = 0
    if b is None:
        b = 0
    return a + b

RADIANS = math.pi / 180


class Pie(Graph):
    """
    A presentation-quality SVG pie graph

    Synopsis
    ========

    from pygal.pie import Pie
    fields = ['Jan', 'Feb', 'Mar']

    data_sales_02 = [12, 45, 21]

    graph = Pie(dict(
        height = 500,
        width = 300,
        fields = fields))
    graph.add_data({'data': data_sales_02, 'title': 'Sales 2002'})
    print "Content-type" image/svg+xml\r\n\r\n'
    print graph.burn()

    Description
    ===========
    This object aims to allow you to easily create high quality
    SVG pie graphs. You can either use the default style sheet
    or supply your own. Either way there are many options which can
    be configured to give you control over how the graph is
    generated - with or without a key, display percent on pie chart,
    title, subtitle etc.
    """

    "if true, displays a drop shadow for the chart"
    show_shadow = False
    "Sets the offset of the shadow from the pie chart"
    shadow_offset = 10

    show_data_labels = True
    "If true, display the actual field values in the data labels"
    show_actual_values = False

    ("If true, display the percentage value of"
     "each pie wedge in the data labels")
    show_percent = True

    "If true, display the labels in the key"
    show_key_data_labels = True
    "If true, display the actual value of the field in the key"
    show_key_actual_values = True
    "If true, display the percentage value of the wedges in the key"
    show_key_percent = False

    "If true, explode the pie (put space between the wedges)"
    expanded = False
    "If true, expand the largest pie wedge"
    expand_greatest = False
    "The amount of space between expanded wedges"
    expand_gap = 10

    show_x_labels = False
    show_y_labels = False

    "The font size of the data point labels"
    datapoint_font_size = 12

    stylesheet_names = Graph.stylesheet_names + ['pie.css']

    def add_data(self, data_descriptor):
        """
        Add a data set to the graph

        >>> graph.add_data({data:[1,2,3,4]}) # doctest: +SKIP

        Note that a 'title' key is ignored.

        Multiple calls to add_data will sum the elements, and the pie will
        display the aggregated data.  e.g.

        >>> graph.add_data({data:[1,2,3,4]}) # doctest: +SKIP
        >>> graph.add_data({data:[2,3,5,7]}) # doctest: +SKIP

        is the same as:

        >>> graph.add_data({data:[3,5,8,11]}) # doctest: +SKIP

        If data is added of with differing lengths, the corresponding
        values will be assumed to be zero.

        >>> graph.add_data({data:[1,2,3,4]}) # doctest: +SKIP
        >>> graph.add_data({data:[5,7]}) # doctest: +SKIP

        is the same as:

        >>> graph.add_data({data:[5,7]}) # doctest: +SKIP
        >>> graph.add_data({data:[1,2,3,4]}) # doctest: +SKIP

        and

        >>> graph.add_data({data:[6,9,3,4]}) # doctest: +SKIP
        """
        pairs = itertools.izip_longest(self.data, data_descriptor['data'])
        self.data = list(itertools.starmap(robust_add, pairs))

    # def add_defs(self, defs):
    #     "Add svg definitions"
    #     node(
    #         defs,
    #         'filter',
    #         id='dropshadow',
    #         width='1.2',
    #         height='1.2',
    #         )
    #     node(
    #         defs,
    #         'feGaussianBlur',
    #         stdDeviation='4',
    #         result='blur',
    #         )

    def draw_graph(self):
        "Here we don't need the graph (consider refactoring)"
        pass

    def get_y_labels(self):
        "Definitely consider refactoring"
        return ['']

    def get_x_labels(self):
        "Okay.  I'll refactor after this"
        return ['']

    def keys(self):
        total = sum(self.data)

        def key(field, value):
            result = [field]
            result.append('[%s]' % value)
            if self.show_key_percent:
                percent = str(round((value / total * 100))) + '%'
                result.append(percent)
            return ' '.join(result)
        return map(key, self.fields, self.data)

    def draw_data(self):
        self.graph = node(self.root, 'g')
        background = node(self.graph, 'g')
        # midground is somewhere between the background and the foreground
        midground = node(self.graph, 'g')

        is_expanded = (self.expanded or self.expand_greatest)
        diameter = min(self.graph_width, self.graph_height)
        # the following assumes int(True)==1 and int(False)==0
        diameter -= self.expand_gap * int(is_expanded)
        diameter -= self.datapoint_font_size * int(self.show_data_labels)
        diameter -= 10 * int(self.show_shadow)
        radius = diameter / 2.0

        xoff = (self.width - diameter) / 2
        yoff = (self.height - self.border_bottom - diameter)
        yoff -= 10 * int(self.show_shadow)
        transform = 'translate(%s %s)' % (xoff, yoff)
        self.graph.set('transform', transform)

        total = sum(self.data)
        max_value = max(self.data)

        percent_scale = 100.0 / total

        prev_percent = 0
        rad_mult = 3.6 * RADIANS
        for index, (field, value) in enumerate(zip(self.fields, self.data)):
            percent = percent_scale * value

            radians = prev_percent * rad_mult
            x_start = radius + (math.sin(radians) * radius)
            y_start = radius - (math.cos(radians) * radius)
            radians = (prev_percent + percent) * rad_mult
            x_end = radius + (math.sin(radians) * radius)
            y_end = radius - (math.cos(radians) * radius)
            percent_greater_fifty = int(percent >= 50)
            path = "M%s,%s L%s,%s A%s,%s 0, %s, 1, %s %s Z" % (
                radius, radius, x_start, y_start, radius, radius,
                percent_greater_fifty, x_end, y_end)

            wedge_group = node(self.foreground, "g",
                               {'class': 'pie'})
            wedge = node(
                wedge_group,
                'path', {
                    'd': path,
                    'class': 'fill fill%s' % (index + 1)}
            )

            translate = None
            tx = 0
            ty = 0
            half_percent = prev_percent + percent / 2
            radians = half_percent * rad_mult

            if self.show_shadow:
                shadow = node(
                    background,
                    'path',
                    d=path,
                    filter='url(#dropshadow)',
                    style='fill: #ccc; stroke: none',
                )
                clear = node(
                    midground,
                    'path',
                    d=path,
                    # note, this probably only works when the background
                    #  is also #fff
                    # consider getting the style from the stylesheet
                    style="fill:#fff; stroke:none;",
                )

            if self.expanded or (self.expand_greatest and value == max_value):
                tx = (math.sin(radians) * self.expand_gap)
                ty = -(math.cos(radians) * self.expand_gap)
                translate = "translate(%s %s)" % (tx, ty)
                wedge.set('transform', translate)
                clear.set('transform', translate)

            if self.show_shadow:
                shadow_tx = self.shadow_offset + tx
                shadow_ty = self.shadow_offset + ty
                translate = 'translate(%s %s)' % (shadow_tx, shadow_ty)
                shadow.set('transform', translate)

            if self.show_data_labels and value != 0:
                label = []
                if self.show_key_data_labels:
                    label.append(field)
                if self.show_actual_values:
                    label.append('[%s]' % value)
                if self.show_percent:
                    label.append('%d%%' % round(percent))
                label = ' '.join(label)

                msr = math.sin(radians)
                mcr = math.cos(radians)
                tx = radius + (msr * radius)
                ty = radius - (mcr * radius)

                if self.expanded or (
                    self.expand_greatest and value == max_value):
                    tx += (msr * self.expand_gap)
                    ty -= (mcr * self.expand_gap)

                label_node = node(
                    wedge_group,
                    'text',
                    {
                        'x': tx,
                        'y': ty,
                        'class': 'dataPointLabel',
                    }
                )
                label_node.text = label

            prev_percent += percent

    def round(self, val, to):
        return round(val, to)
