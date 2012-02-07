from pygal.svg import Svg
from pygal.config import Config


def test_root():
    class RootConfig(Config):
        width = 800
        height = 600

    svg = Svg(RootConfig)
    assert svg.render().startswith('\n'.join((
        '<?xml version=\'1.0\' encoding=\'utf-8\'?>',
        '<svg xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns="http://www.w3.org/2000/svg" '
        'viewBox="0 0 800 600">',
        '')))
