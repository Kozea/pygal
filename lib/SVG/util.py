#!python

from itertools import chain, repeat, izip

# from itertools recipes (python documentation)
def grouper(n, iterable, padvalue=None):
	"grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
	return izip(*[chain(iterable, repeat(padvalue, n-1))]*n)

def reverse_mapping(mapping):
	"""
	For every key, value pair, return the mapping for the
	equivalent value, key pair
	"""
	keys, values = mapping.items()
	return dict(zip(values, keys))

def flatten_mapping(mapping):
	"""
	For every key that has an __iter__ method, assign the values
	to a key for each.
	>>> flatten_mapping({'ab': 3, ('c','d'): 4}) == {'ab': 3, 'c': 4, 'd': 4}
	True
	"""
	return dict(flatten_items(mapping.items()))

def flatten_items(items):
	for keys, value in items:
		if hasattr(keys, '__iter__'):
			for key in keys:
				yield (key, value)
		else:
			yield (keys, value)

def float_range(start=0, stop=None, step=1):
	"Much like the built-in function range, but accepts floats"
	start = float(start)
	while start < stop:
		yield start
		start += step

def date_range(start=None, stop=None, step=None):
	"Much like the built-in function range, but works with floats"
	if step is None: step = relativedelta(days=1)
	if start is None: start = datetime.datetime.now()
	while start < stop:
		yield start
		start += step
	