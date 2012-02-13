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


class Box(object):
    def __init__(self):
        self.xmin = self.ymin = 0
        self.xmax = self.ymax = 1

    @property
    def width(self):
        return self.xmax - self.xmin

    @property
    def height(self):
        return self.ymax - self.ymin

    def fix(self):
        if not self.width:
            self.xmax = self.xmin + 1
        if not self.height:
            self.ymin -= .5
            self.ymax = self.ymin + 1


class View(object):
    def __init__(self, width, height, box):
        self.width = width
        self.height = height
        self.box = box

    def x(self, x):
        return self.width * (x - self.box.xmin) / float(self.box.width)

    def y(self, y):
        return (self.height - self.height *
                (y - self.box.ymin) / float(self.box.height))

    def __call__(self, xy):
        x, y = xy
        return (self.x(x), self.y(y))
