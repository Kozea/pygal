class Style(object):
    def __init__(self,
        background='black',
        plot_background='#111',
        foreground='#999',
        foreground_light='#eee',
        foreground_dark='#555',
        colors=(
                '#ff5995', '#b6e354', '#feed6c', '#8cedff', '#9e6ffe',
                '#899ca1', '#f8f8f2', '#808384', '#bf4646', '#516083',
                '#f92672', '#82b414', '#fd971f', '#56c2d6', '#8c54fe',
                '#465457')):
            self.background = background
            self.plot_background = plot_background
            self.foreground = foreground
            self.foreground_light = foreground_light
            self.foreground_dark = foreground_dark
            self._colors = colors

    @property
    def colors(self):
        def color(tupl):
            return (
                    '.color-{0} {{\n'
                    '  stroke: {1};\n'
                    '  fill: {1};\n'
                    '}}\n'.format(*tupl))
        return '\n'.join(map(color, enumerate(self._colors)))

DefaultStyle = Style()
LightStyle = Style(
    background='transparent',
    plot_background='rgba(0, 0, 255, 0.1)',
    foreground='rgba(0, 0, 0, 0.7)',
    foreground_light='rgba(0, 0, 0, 0.9)',
    foreground_dark='rgba(0, 0, 0, 0.5)',
    colors=('#242424', '#9f6767', '#92ac68',
            '#d0d293', '#9aacc3', '#bb77a4',
            '#77bbb5', '#777777'))
