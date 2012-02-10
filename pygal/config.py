from pygal.style import DefaultStyle


class FontSizes(object):
    """Container for font sizes"""


class Config(object):
    """Class holding config values"""

    # Graph width and height
    width, height = 800, 600
    # Scale order range
    x_scale = 1
    y_scale = 1
    # If set to a filename, this will replace the default css
    base_css = None
    # Style holding values injected in css
    style = DefaultStyle
    # Various font sizes
    label_font_size = 10
    values_font_size = 18
    title_font_size = 16
    legend_font_size = 14
    # Specify labels rotation angles in degrees
    x_label_rotation = 0
    y_label_rotation = 0
    # Set to false to remove legend
    show_legend = True
    # Size of legend boxes
    legend_box_size = 12
    # X labels, must have same len than data.
    # Leave it to None to disable x labels display.
    x_labels = None
    # You can specify explicit y labels (must be list(int))
    y_labels = None
    # Graph title
    # Leave it to None to disable title.
    title = None
    # Set this to the desired radius in px
    rounded_bars = False
    # Always include x axis
    x_start_at_zero = False

    def __init__(self, **kwargs):
        """Can be instanciated with config kwargs"""
        self.__dict__.update(kwargs)

    @property
    def font_sizes(self):
        fs = FontSizes()
        for name in dir(self):
            if name.endswith('_font_size'):
                setattr(fs,
                        name.replace('_font_size', ''),
                        '%dpx' % getattr(self, name))
        return fs
