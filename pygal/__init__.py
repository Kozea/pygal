from collections import namedtuple

Serie = namedtuple('Serie', ('title', 'values', 'index'))
Label = namedtuple('Label', ('label', 'pos'))


class Margin(object):
    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    @property
    def x(self):
        return self.left + self.right

    @property
    def y(self):
        return self.top + self.bottom
