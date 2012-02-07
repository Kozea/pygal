from decimal import Decimal
from math import floor


def round_to_int(number, precision):
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
