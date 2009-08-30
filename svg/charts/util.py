#!python

from itertools import chain, repeat, izip
import datetime

# from itertools recipes (python documentation)
def grouper(n, iterable, padvalue=None):
	"""
	>>> tuple(grouper(3, 'abcdefg', 'x'))
	(('a', 'b', 'c'), ('d', 'e', 'f'), ('g', 'x', 'x'))
	"""
	return izip(*[chain(iterable, repeat(padvalue, n-1))]*n)

def reverse_mapping(mapping):
	"""
	For every key, value pair, return the mapping for the
	equivalent value, key pair
	>>> reverse_mapping({'a': 'b'}) == {'b': 'a'}
	True
	"""
	keys, values = zip(*mapping.items())
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
	"""
	Much like the built-in function range, but accepts floats
	>>> tuple(float_range(0, 9, 1.5))
	(0.0, 1.5, 3.0, 4.5, 6.0, 7.5)
	"""
	start = float(start)
	while start < stop:
		yield start
		start += step

def date_range(start=None, stop=None, step=None):
	"""
	Much like the built-in function range, but works with dates
	>>> my_range = tuple(date_range(datetime.datetime(2005,12,21), datetime.datetime(2005,12,25)))
	>>> datetime.datetime(2005,12,21) in my_range
	True
	>>> datetime.datetime(2005,12,22) in my_range
	True
	>>> datetime.datetime(2005,12,25) in my_range
	False
	"""
	if step is None: step = datetime.timedelta(days=1)
	if start is None: start = datetime.datetime.now()
	while start < stop:
		yield start
		start += step

# copied from jaraco.datetools
def divide_timedelta_float(td, divisor):
	"""
	Meant to work around the limitation that Python datetime doesn't support
	floats as divisors or multiplicands to datetime objects
	>>> one_day = datetime.timedelta(days=1)
	>>> half_day = datetime.timedelta(days=.5)
	>>> divide_timedelta_float(one_day, 2.0) == half_day
	True
	>>> divide_timedelta_float(one_day, 2) == half_day
	False
	"""
	# td is comprised of days, seconds, microseconds
	dsm = [getattr(td, attr) for attr in ('days', 'seconds', 'microseconds')]
	dsm = map(lambda elem: elem/divisor, dsm)
	return datetime.timedelta(*dsm)

def get_timedelta_total_microseconds(td):
	seconds = td.days*86400 + td.seconds
	microseconds = td.microseconds + seconds*(10**6)
	return microseconds

def divide_timedelta(td1, td2):
	"""
	Get the ratio of two timedeltas
	>>> one_day = datetime.timedelta(days=1)
	>>> one_hour = datetime.timedelta(hours=1)
	>>> divide_timedelta(one_hour, one_day) == 1/24.0
	True
	"""
	
	td1_total = float(get_timedelta_total_microseconds(td1))
	td2_total = float(get_timedelta_total_microseconds(td2))
	return td1_total/td2_total

class TimeScale(object):
	"Describes a scale factor based on time instead of a scalar"
	def __init__(self, width, range):
		self.width = width
		self.range = range

	def __mul__(self, delta):
		scale = divide_timedelta(delta, self.range)
		return scale*self.width

# the following three functions were copied from jaraco.util.iter_

# todo, factor out caching capability
class iterable_test(dict):
	"Test objects for iterability, caching the result by type"
	def __init__(self, ignore_classes=(basestring,)):
		"""ignore_classes must include basestring, because if a string
		is iterable, so is a single character, and the routine runs
		into an infinite recursion"""
		assert basestring in ignore_classes, 'basestring must be in ignore_classes'
		self.ignore_classes = ignore_classes

	def __getitem__(self, candidate):
		return dict.get(self, type(candidate)) or self._test(candidate)
			
	def _test(self, candidate):
		try:
			if isinstance(candidate, self.ignore_classes):
				raise TypeError
			iter(candidate)
			result = True
		except TypeError:
			result = False
		self[type(candidate)] = result
		return result

def iflatten(subject, test=None):
	if test is None:
		test = iterable_test()
	if not test[subject]:
		yield subject
	else:
		for elem in subject:
			for subelem in iflatten(elem, test):
				yield subelem
				
def flatten(subject, test=None):
	"""flatten an iterable with possible nested iterables.
	Adapted from
	http://mail.python.org/pipermail/python-list/2003-November/233971.html
	>>> flatten(['a','b',['c','d',['e','f'],'g'],'h']) == ['a','b','c','d','e','f','g','h']
	True

	Note this will normally ignore string types as iterables.
	>>> flatten(['ab', 'c'])
	['ab', 'c']
	"""
	return list(iflatten(subject, test))

