#!/usr/bin/env python3

from decorator import decorator

@decorator
def test_decorator(func):
	def inner_func(*args, **kwargs):
		print('Test decorator approves {}'.format(func.__name__))
		return func(*args, **kwargs)
	return inner_func

@test_decorator
def sample_function(arg1, arg2=None, arg3=None):
	''' Sample function to test whether decorator behaves or not '''
	print('Sample function here! Called with {}, {} and {}.'.format(arg1, arg2, arg3))

sample_function.crazy_attribute = 'True'

def main():
	sample_function('a1')
	sample_function('a1', 'a2')
	sample_function('a1', 'a2', 'a3')
	sample_function('a1', arg3='a3')
	print('Name:', sample_function.__name__)
	print('Docstring:', sample_function.__doc__)
	print('CrazyAttr:', sample_function.crazy_attribute)


if __name__ == '__main__':
	main()
