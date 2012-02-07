from pygal.style import DefaultStyle


class Config(object):
    width = 800
    height = 600
    scale = 1
    max_scale_step = 10
    base_css = None
    style = DefaultStyle
    label_font_size = 12
    x_labels = None
    y_labels = None
    title = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
