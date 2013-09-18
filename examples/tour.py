"""
Copyright (c) 2013, Jonas Pfannschmidt
Licensed under the MIT license http://www.opensource.org/licenses/mit-license.php
"""
from simplemenus import *
from collections import OrderedDict

def example_tour():
	print("Your name is: " + str(get_string("Enter your name or leave empty for the default", 'guest')))

	print("Your choice: " + get_option(['dog', 'cat', 'mouse'], 'Which animal do you like most?'))

	print("Your birthday is: " + str(get_date("Enter your birthday in the format dd/mm/yyyy")))

	print("Your choice: " + str(get_integer("Enter any number or leave empty for 12345", 12345)))

	show_small_headline("Choose from an OrderedDict")
	example = OrderedDict()
	example['number 1'] = 'one'
	example['number 2'] = 'two'
	example['number 3'] = 'three'
	print("Your choice: " + get_from_dictionary(example, show_cancel=False))
	wait_for_enter()

	show_small_headline("Choose from a List")
	result = get_from_list(["one", "two", "three", "four"])
	if result is None:
		print("Your choice: Cancel")
	else:
		print("Your choice: " + result)
	wait_for_enter()

	if get_boolean("Do you want to do the tour again?"):
		example_tour()

def example_headlines():
	mymenu = OrderedDict()
	mymenu['Show headline'] = 'full'
	mymenu['Show small headline'] = 'small'

	result = start_menu(mymenu, "Example")

	if result == 'full':
		show_headline("Test headline")		
	elif result == 'small':
		show_small_headline("Test small headline")		

	wait_for_enter()

if __name__=="__main__":
	mymenu = OrderedDict()
	mymenu['Show submenu for headlines'] = example_headlines
	mymenu['Quick tour'] = example_tour
	mymenu['A useless option'] = lambda: None

	start_menu(mymenu, "Example")
