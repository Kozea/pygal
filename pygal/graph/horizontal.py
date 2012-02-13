from pygal.graph.bar import Bar
from pygal.graph.stackedbar import StackedBar


class HorizontalGraph(object):
    """Horizontal graph"""
    def __init__(self, *args, **kwargs):
        kwargs['horizontal'] = True
        super(HorizontalGraph, self).__init__(*args, **kwargs)

    def _compute(self):
        super(HorizontalGraph, self)._compute()
        self._x_labels, self._y_labels = self._y_labels, self._x_labels
        self._box.swap()
        # Y axis is inverted
        for serie in self.series:
            serie.values = reversed(serie.values)


class HorizontalBar(HorizontalGraph, Bar):
    """Horizontal Bar graph"""


class HorizontalStackedBar(HorizontalGraph, StackedBar):
    """Horizontal Stacked Bar graph"""
