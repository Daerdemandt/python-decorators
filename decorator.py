#!/usr/bin/env python3


from functools import wraps
def decorator(raw_decorator):
	'''This decorator can be used to turn simple functions
	into well-behaved decorators, so long as the decorators
	are fairly simple. If a decorator expects a function and
	returns a function (no descriptors), and if it doesn't
	modify function attributes or docstring, then it is
	eligible to use this. Simply apply @decorator to your
	decorator and it will automatically preserve the docstring
	and function attributes of functions to which it is applied.
	'''
	@wraps(raw_decorator)
	def wrapper(func):
		@wraps(func)
		@raw_decorator
		def wrapped(*args, **kwargs):
			return func(*args, **kwargs)
		return wrapped
	return wrapper
	
def decorator_use_example():
	''' Example of usage of 'decorator' decorator '''
	@decorator
	def my_simple_logging_decorator(func):
		def you_will_never_see_this_name(*args, **kwargs):
			print('calling {}'.format(func.__name__))
			return func(*args, **kwargs)
		return you_will_never_see_this_name

	@my_simple_logging_decorator
	def double(x):
		'Doubles a number.'
		return 2 * x

	double.multiplier = 2

	assert double.__name__ == 'double'
	assert double.__doc__ == 'Doubles a number.'
	assert double.multiplier == 2


