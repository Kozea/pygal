from decimal import Decimal
from math import floor


def round_to_int(number, precision):
    rounded = (int(number) + precision / 2) / precision * precision
    return str(int(rounded)), rounded


# def round_to_float(number, precision):
#     decimal = Decimal(str(number))
#     rounded = decimal.quantize(Decimal(str(precision)))
#     return str(rounded), float(rounded)

def round_to_float(number, precision):
    rounded = Decimal(
        floor((number + precision / 2) / precision)) * Decimal(str(precision))
    return str(rounded), float(rounded)
