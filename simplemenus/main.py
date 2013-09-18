"""
The main module. All of its public functions get exported by the package (see __init__.py)

Copyright (c) 2013, Jonas Pfannschmidt
Licensed under the MIT license http://www.opensource.org/licenses/mit-license.php
"""
from __future__ import print_function
import datetime
import string
import types
import sys
from .xgetch import getch as _getch

# Python 2.7 compatibility: Map input() to raw_input()
try:
	import __builtin__
	input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
	pass

_config = {}
def reset_config():
	"""Resets the configuration to the default"""

	global _config
	_config['prompt'] = "> "
	_config['cancel_option'] = "0"
	_config['cancel_text'] = "Cancel"
	_config['list_format'] = "{option}) {text}"
	_config['empty_text'] = "No entries"
	_config['date_format'] = '%d/%m/%Y'
	_config['force_return'] = False

reset_config()

def configure(key, value):
	"""
	Change the configuration.

	Args:
		key: One of the following strings
			prompt        - Displayed when the user gets prompted for an input.
			cancel_option - Which text needs to be entered to cancel an operation.
			cancel_text   - Which text gets displayed for the cancel option.
			list_format   - How to display lists. Uses str.format() syntax. Use {option} and {text} as placeholders.
			empty_text    - Text that gets displayed when a list is empty
			date_format   - strptime format to parse dates. See docs.python.org/library/datetime.html#strftime-strptime-behavior
			force_return  - Always confirm input by pressing the return key
		value: The configuration value. See reset_config() for the defaults
	"""

	if key not in _config:
		raise Exception("Unknown configuration key:{}".format(key))

	_config[key] = value

def wait_for_enter():
	"""Waits for the user to press enter."""
	input("Press enter to continue" + _config['prompt'])

def get_string(text = '', default = None):
	"""Get string or default value."""
	user_input = input(text + _config['prompt'])

	if _use_default(user_input, default):
		return default
	else:
		return user_input

def get_character(text = '', default = None):
	"""Get character without waiting for the enter key."""
	sys.stdout.write(text + _config['prompt'])

	user_input = _getch()

	sys.stdout.write(user_input + "\n")

	if _use_default(user_input, default):
		return default
	else:
		return user_input

def get_boolean(text = '', default = None):
	"""Repeat until the user enters 'y' or 'n' or a string starting with 'y' or 'n' (i.e. 'yes' and 'no')."""

	options = ['y', 'n']

	if default is not None:
		options.append('\r')

	user_input = get_option(options, text)

	if _use_default(user_input, default):
		return default
	elif user_input[0] =='y':
		return True
	elif user_input[0] == 'n':
		return False

def get_integer(text = '', default = None):
	"""Repeat until the user enters a valid number."""

	user_input = input(text + _config['prompt'])

	if _use_default(user_input, default):
		return default
	elif user_input.isdigit():
		return int(user_input)
	else:
		print("Not a number: {}".format(user_input))
		return get_integer(text, default)

def get_date(text = '', default = None):
	"""Repeat until the user enters a valid date."""

	user_input = input(text + _config['prompt'])

	if _use_default(user_input, default):
		return default
	else:
		try:
			return datetime.datetime.strptime(user_input, _config['date_format']).date()
		except ValueError:
			print("Not a date: {}".format(user_input))
			return get_date(text, default)

def get_option(options, text = '', default = None):
	"""Repeat until the user chooses a valid option.

	   If there are only single-letter options the input is accepted directly otherwise the user has to confirm by pressing the return key

	Args:
		options: a list of strings that are valid options
	"""

	if not _config['force_return'] and not [x for x in options if len(x) > 1]:
		# if all options are only one character, we can use get_character instead of get_string
		user_input = get_character(text, default)
	else:
		user_input = get_string(text, default)
	
	if user_input in options or user_input == default:
		return user_input
	else:
		print("Must be one of: {}".format(options))
		return get_option(options, text)

def get_from_list(my_list, text = '', show_cancel = True, default = None):
	"""
	Enumerates a list of strings and lets the user choose one value.

	Example:

		a) one
		b) two
		c) three
		d) four
	
		0) Cancel
		>

	"""

	options = _enumerate_list(my_list)
	show_enumerated_list(my_list)

	if show_cancel:
		print("")
		options.append(_config['cancel_option'])
		print(_config['list_format'].format(option=_config['cancel_option'], text=_config['cancel_text']))

	chosen = get_option(options, text, default=default)

	if chosen == default:
		return default
	elif chosen == _config['cancel_option']:
		None
	else:
		return my_list[_letter_to_number(chosen)]

def get_from_dictionary(dictionary, show_cancel = True):
	"""Let the user choose a key and return the corresponding value.

	Note: Use OrderedDict to preserve the option order
	"""

	key = get_from_list(list(dictionary.keys()), show_cancel=show_cancel)

	return dictionary[key] if key else key

def show_enumerated_list(my_list):
	"""Shows a list enumerated by a, b, c, ..."""

	if (my_list):
		for option, value in zip(_enumerate_list(my_list), my_list):
		     print(_config['list_format'].format(option=option, text=value)	)
	else:
		print(_config['empty_text'])

def show_headline(headline):
	""" Show a headline.

	Example:

		+------+
		| Test |
		+------+

	"""

	line = "+" + "-" * (len(headline) + 2) + "+"
	print("")
	print(line)
	print("| " + headline + " |")
	print(line)
	print("")

def show_small_headline(headline):
	""" Show a smaller headline.

	Example:
		+-- Test --+
	"""

	print("+--- " + headline + " ---+")

def start_menu(menu, headline):
	"""Show a menu and run a function if the user chooses one menu entry.

	Args:
		menu: an OrderedDict dictionary. The keys are shown as menu entries. If a value is a functions 
			  it gets called when the user chooses the corresponding menu entry otherwise it gets returned.
		headline: the title for the menu
	"""
	show_headline(headline)
	chosen = get_from_dictionary(menu)
	while isinstance(chosen, types.FunctionType):
		chosen()
		show_headline(headline)
		chosen = get_from_dictionary(menu)

	return chosen

def _number_to_letter(i):
	l = i % 26
	n = int(i / 26) + 1

	return n * string.ascii_letters[:26][l]

def _letter_to_number(l):
	i = string.ascii_letters[:26].index(l[0])

	return i + ((len(l) - 1) * 26)

def _enumerate_list(my_list):
	return [_number_to_letter(i) for i, x in enumerate(my_list)]

def _use_default(user_input, default):
	return default is not None and (len(user_input) == 0 or user_input == '\r')
