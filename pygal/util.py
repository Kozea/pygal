from decimal import Decimal
from math import floor, pi


def round_to_int(number, precision):
    precision = int(precision)
    rounded = (int(number) + precision / 2) / precision * precision
    return rounded


def round_to_float(number, precision):
    rounded = Decimal(
        floor((number + precision / 2) / precision)) * Decimal(str(precision))
    return float(rounded)


def round_to_scale(number, precision):
    if precision < 1:
        return round_to_float(number, precision)
    return round_to_int(number, precision)


def cut(list_, index=0):
    if isinstance(index, int):
        cut = lambda x: x[index]
    else:
        cut = lambda x: getattr(x, index)
    return map(cut, list_)


def rad(deg):
    return pi * deg / 180.


def _swap_curly(string):
    """Swap single and double curly brackets"""
    return (string
            .replace('{{ ', '{{')
            .replace('{{', '\x00')
            .replace('{', '{{')
            .replace('\x00', '{')
            .replace(' }}', '}}')
            .replace('}}', '\x00')
            .replace('}', '}}')
            .replace('\x00', '}'))


def template(string, **kwargs):
    """Format a string using double braces"""
    return _swap_curly(string).format(**kwargs)

swap = lambda tuple_: tuple(reversed(tuple_))
ident = lambda x: x
