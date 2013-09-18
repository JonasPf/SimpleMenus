"""
SimpleMenus is a small and simple python module for creating interactive 
console applications. It allows to prompt the user for strings, integers,
dates, booleans, lets him choose between various options and offers 
lightweight menus.

I use it for small utilities and prototypes whenever I need a little bit of
interaction with the user. For more complicated applications you should look
at something like curses instead (http://docs.python.org/library/curses.html).

Examples:
	# print birthday
	print(get_date("Enter your birthday"))

	# print selection
	print(get_from_list(['One', 'Two', 'Three']))

	# return if user doesn't want to continue
	if not get_boolean('Continue?'):
		return


You can find more at the examples and the test direcory.

Copyright (c) 2013, Jonas Pfannschmidt
Licensed under the MIT license http://www.opensource.org/licenses/mit-license.php
"""
from .main import *
__all__=['reset_config', 
	'configure', 
	'wait_for_enter', 
	'get_string', 
	'get_character', 
	'get_boolean', 
	'get_integer', 
	'get_date', 
	'get_option', 
	'get_from_list', 
	'get_from_dictionary', 
	'show_enumerated_list', 
	'show_headline', 
	'show_small_headline', 
	'start_menu']
