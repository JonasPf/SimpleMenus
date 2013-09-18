SimpleMenus is a small and simple python package for creating interactive 
console applications. It allows to prompt the user for strings, integers,
dates, booleans, lets him choose between various options and offers 
lightweight menus.

I use it for small utilities and prototypes whenever I need a little bit of
interaction with the user. For more complex applications you should look at 
something like curses instead (http://docs.python.org/library/curses.html).

Examples:
	# print birthday
	print(get_date("Enter your birthday"))

	# print selection
	print(get_from_list(['One', 'Two', 'Three']))

	# return if user doesn't want to continue
	if not get_boolean('Continue?'):
		return


You can find more in the examples and test direcories and an API documentation at doc/simplemenus.html.

Tested with Python 2.7.5 and Python 3.3 on Windows and Linux.

Webpage: http://www.pulsedo.com/free/simplemenus

Copyright (c) 2013, Jonas Pfannschmidt
Licensed under the MIT license http://www.opensource.org/licenses/mit-license.php
