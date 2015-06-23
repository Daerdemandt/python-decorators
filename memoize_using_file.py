#!/usr/bin/env python3
from decorator import decorator
from memoize import memoize

from pickle import dump, load
from weakref import finalize

class file_dict(dict):
	'''
	Dictionary that is initiated from a given file (if it exists) and
	writes its own contents to the same file on deletion.
	'''
	def __init__(self, filename):
		''' Read contents of dictionary from file, set up deletion hook '''
		self.filename = filename
		dict.__init__(self)
		try:
			with open(self.filename, 'rb') as cache_file:
				self.update(load(cache_file))
		except FileNotFoundError:
			with open(self.filename, 'a'):
				pass # create the file if it does not exist
		# when object is deleted, update file
		finalize(self, lambda: self.dump_to_file())
	
	def dump_to_file(self):
		with open(self.filename, 'wb+') as cache_file:
			dump(self, cache_file)

def memoize_using_file(filename):
	'''
	Decorator. Caches a function's return value each time it is called.
	If called later with the same arguments, the cached value is returned
	(not reevaluated).
	During runtime, values are cached in a dictionary.
	Between runs of a program, this dictionary is stored in a file.
	'''
	@decorator
	def wrapper(func):
		memoized_func = memoize(func)
		file_cache = file_dict(filename)
		file_cache.update(memoized_func.cache)
		memoized_func.cache = file_cache
		return memoized_func
	return wrapper



def memoize_using_file_use_example():
	memfile = 'file_to_mem.bin'
	@memoize_using_file(memfile)
	def fibonacci(n):
		"Return the nth fibonacci number."
		if n in (0, 1):
			return n
		return fibonacci(n-1) + fibonacci(n-2)

	fibonacci.some_attr = 'attribute is preserved'

	assert fibonacci(50) == 12586269025
	assert fibonacci.__doc__ == 'Return the nth fibonacci number.'
	assert fibonacci.__name__ == 'fibonacci'
	assert fibonacci.some_attr == 'attribute is preserved'

if __name__ == '__main__':
	memoize_using_file_use_example()
