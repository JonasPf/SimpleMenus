"""
Copyright (c) 2013, Jonas Pfannschmidt
Licensed under the MIT license http://www.opensource.org/licenses/mit-license.php
"""
from __future__ import print_function
import unittest
import io
import datetime
import sys
import collections
import simplemenus.main
from simplemenus import *

def string_io_class():
	if sys.version_info >= (3, 0):
		return io.StringIO
	else:
		return io.BytesIO

class IOTestCase(unittest.TestCase):
	def setUp(self):
		sys.stdout = string_io_class()()
		self.single_character_index = -1

	def tearDown(self):
		reset_config()

	def mockInput(self, input):
		sys.stdin = string_io_class()(input)

	def mockSingleCharacterInput(self, input):
		def mock_result():
			self.single_character_index += 1
			if len(input) > self.single_character_index:
				return input[self.single_character_index]
			else:
				return input[-1:]

		simplemenus.main._getch = mock_result

	def assertOutput(self, expected):
		self.assertEqual(expected, sys.stdout.getvalue())



class Test_get_string(IOTestCase):

	def test_should_print_prompt(self):
		self.mockInput('\n')
		get_string('Enter text')
		self.assertOutput("Enter text> ")

	def test_should_return_input(self):
		self.mockInput('123')
		self.assertEqual("123", get_string())

	def test_should_return_default_when_no_input_given(self):
		self.mockInput('\n')
		self.assertEqual("123", get_string(default='123'))

	def test_should_return_empty_when_no_input_given_and_no_default_defined(self):
		self.mockInput('\n')
		self.assertIs('', get_string())

	def test_wait_for_enter_should_print_prompt(self):
		self.mockInput('\n')
		wait_for_enter()
		self.assertOutput("Press enter to continue> ")



class Test_get_character(IOTestCase):

	def test_should_print_prompt(self):
		self.mockSingleCharacterInput('x')
		get_character('Enter character')
		self.assertOutput("Enter character> x\n")

	def test_should_print_result_and_newline(self):
		self.mockSingleCharacterInput('x')
		get_character('Enter character')
		self.assertOutput("Enter character> x\n")

	def test_should_return_input(self):
		self.mockSingleCharacterInput('a')
		self.assertEqual("a", get_character())

	def test_should_return_default_when_return_given(self):
		self.mockSingleCharacterInput('\r')
		self.assertEqual("a", get_character(default='a'))

	def test_should_return_return_when_no_default_configure(self):
		self.mockSingleCharacterInput('\r')
		self.assertEqual("\r", get_character())



class Test_get_boolean(IOTestCase):

	def test_should_print_prompt(self):
		self.mockSingleCharacterInput('y')
		get_boolean('Answer yes or no')
		self.assertOutput("Answer yes or no> y\n")

	def test_should_return_true_when_yes(self):
		self.mockSingleCharacterInput('y')
		self.assertTrue(get_boolean())

	def test_should_return_false_when_no(self):
		self.mockSingleCharacterInput('n')
		self.assertFalse(get_boolean())

	def test_should_return_default_when_no_input_given(self):
		self.mockSingleCharacterInput('\r')
		self.assertTrue(get_boolean(default=True))
		self.assertFalse(get_boolean(default=False))

	def test_should_loop_until_valid_input(self):
		# \r is invalid if no default defined
		self.mockSingleCharacterInput("1\rn")
		self.assertIs(False, get_boolean())
		self.assertOutput("""> 1
Must be one of: ['y', 'n']
> \r
Must be one of: ['y', 'n']
> n
""")



class Test_get_integer(IOTestCase):

	def test_should_print_prompt(self):
		self.mockInput('123\n')
		get_integer('Enter a number')
		self.assertOutput("Enter a number> ")

	def test_should_return_integer(self):
		self.mockInput('123\n')
		self.assertEqual(123, get_integer())

	def test_should_return_default_when_no_input_given(self):
		self.mockInput('\n')
		self.assertEqual(123, get_integer(default=123))

	def test_should_loop_until_valid_input(self):
		self.mockInput('a\n\n123\n')
		self.assertEqual(123, get_integer())
		self.assertOutput("""> Not a number: a
> Not a number: 
> """)



class Test_get_date(IOTestCase):

	def test_should_print_prompt(self):
		self.mockInput('15/12/2013\n')
		get_date('Enter a date')
		self.assertOutput("Enter a date> ")

	def test_should_return_date(self):
		self.mockInput('15/12/2013\n')
		self.assertEqual(datetime.date(2013, 12, 15), get_date())

	def test_should_return_default_when_no_input_given(self):
		self.mockInput('\n')
		self.assertEqual(datetime.date(2013, 12, 15), get_date(default=datetime.date(2013, 12, 15)))

	def test_should_loop_until_valid_input(self):
		self.mockInput('a\n33/12/2013\n\n15/12/2013\n')
		self.assertEqual(datetime.date(2013, 12, 15), get_date())
		self.assertOutput("""> Not a date: a
> Not a date: 33/12/2013
> Not a date: 
> """)

	def test_should_use_configured_date_format(self):
		configure('date_format', '%d-%m-%y')
		self.mockInput('15-12-13\n')
		self.assertEqual(datetime.date(2013, 12, 15), get_date())


class Test_get_option(IOTestCase):
	
	def setUp(self):
		IOTestCase.setUp(self)
		self.my_list = ["mouse", "elephant", "dog"]
		self.my_single_list = ["m", "e", "d"]

	def test_should_print_prompt(self):
		self.mockInput('mouse\n')
		get_option(self.my_list, "Choose an animal")
		self.assertOutput("Choose an animal> ")

	def test_should_return_selection_when_multiple_characters_are_entered(self):
		self.mockInput('mouse\n')
		self.assertEqual('mouse', get_option(self.my_list))

	def test_should_return_selection_when_single_character_is_entered(self):
		self.mockSingleCharacterInput('m')
		self.assertEqual('m', get_option(self.my_single_list))

	def test_should_force_return_when_configured(self):
		configure('force_return', True)
		self.mockInput('m\n')
		self.assertEqual('m', get_option(self.my_single_list))

	def test_should_return_default_when_no_input_given(self):
		self.mockInput('\n')
		self.assertEqual('mouse', get_option(self.my_list, default='mouse'))

	def test_should_loop_until_valid_input(self):
		self.mockInput('snake\n\nmouse\n')
		self.assertEqual('mouse', get_option(self.my_list))
		self.assertOutput("""> Must be one of: ['mouse', 'elephant', 'dog']
> Must be one of: ['mouse', 'elephant', 'dog']
> """)


class Test_get_from_list(IOTestCase):

	def setUp(self):
		IOTestCase.setUp(self)
		self.my_list = ["mouse", "elephant", "dog"]

	def test_should_print_list_and_prompt(self):
		self.mockSingleCharacterInput('a')
		get_from_list(self.my_list, "Choose an animal")
		self.assertOutput("""a) mouse
b) elephant
c) dog

0) Cancel
Choose an animal> a
""")

	def test_should_print_list_without_cancel_when_cancel_is_disabled(self):
		self.mockSingleCharacterInput('a')
		get_from_list(self.my_list, show_cancel=False)
		self.assertOutput("""a) mouse
b) elephant
c) dog
> a
""")

	def test_should_return_selection(self):
		self.mockSingleCharacterInput('a')
		self.assertEqual('mouse', get_from_list(self.my_list))

	def test_should_return_none_when_canceled(self):
		self.mockSingleCharacterInput('0')
		self.assertIs(None, get_from_list(self.my_list))

	def test_should_return_default_when_no_input_given(self):
		self.mockSingleCharacterInput('\r')
		self.assertEqual('mouse', get_from_list(self.my_list, default='mouse'))

	def test_should_loop_until_valid_input(self):
		self.mockSingleCharacterInput('d\rb')
		self.assertEqual('elephant', get_from_list(self.my_list))
		self.assertOutput("""a) mouse
b) elephant
c) dog

0) Cancel
> d
Must be one of: ['a', 'b', 'c', '0']
> \r
Must be one of: ['a', 'b', 'c', '0']
> b
""")

	def test_should_not_accept_cancel_when_cancel_is_disabled(self):
		self.mockSingleCharacterInput('0b')
		self.assertEqual('elephant', get_from_list(self.my_list, show_cancel=False))
		self.assertOutput("""a) mouse
b) elephant
c) dog
> 0
Must be one of: ['a', 'b', 'c']
> b
""")

	def test_should_force_return_when_configured(self):
		configure('force_return', True)
		self.mockInput('a\n')
		self.assertEqual('mouse', get_from_list(self.my_list))

	def test_should_return_configure_empty_text(self):
		configure('empty_text', 'Nothing')

		self.mockSingleCharacterInput('0')
		get_from_list([])
		self.assertOutput("""Nothing

0) Cancel
> 0
""")

	def test_should_show_configured_cancel(self):
		configure('cancel_option', 'x')
		configure('cancel_text', 'Exit')

		self.mockSingleCharacterInput('x')
		get_from_list(['a', 'b'])
		self.assertOutput("""a) a
b) b

x) Exit
> x
""")

	def test_should_show_configured_list_format(self):
		configure('list_format', '{option} >>> {text}')

		self.mockSingleCharacterInput('a')
		get_from_list(['a', 'b'])
		self.assertOutput("""a >>> a
b >>> b

0 >>> Cancel
> a
""")

class Test_get_from_dictionary(IOTestCase):

	def setUp(self):
		IOTestCase.setUp(self)

		self.my_dict = collections.OrderedDict()
		self.my_dict['Mickey Mouse'] = 'mouse'
		self.my_dict['Dumbo'] = 'elephant'
		self.my_dict['Lassie'] = 'dog'

	def test_should_print_list_and_prompt(self):
		self.mockSingleCharacterInput('a')
		get_from_dictionary(self.my_dict)
		self.assertOutput("""a) Mickey Mouse
b) Dumbo
c) Lassie

0) Cancel
> a
""")

	def test_should_print_list_without_cancel_when_cancel_is_disabled(self):
		self.mockSingleCharacterInput('a')
		get_from_dictionary(self.my_dict, show_cancel=False)
		self.assertOutput("""a) Mickey Mouse
b) Dumbo
c) Lassie
> a
""")

	def test_should_return_selection(self):
		self.mockSingleCharacterInput('a')
		self.assertEqual('mouse', get_from_dictionary(self.my_dict))

	def test_should_return_none_when_canceled(self):
		self.mockSingleCharacterInput('0')
		self.assertIs(None, get_from_dictionary(self.my_dict))

	def test_should_loop_until_valid_input(self):
		self.mockSingleCharacterInput('d\rb')
		self.assertEqual('elephant', get_from_dictionary(self.my_dict))
		self.assertOutput("""a) Mickey Mouse
b) Dumbo
c) Lassie

0) Cancel
> d
Must be one of: ['a', 'b', 'c', '0']
> \r
Must be one of: ['a', 'b', 'c', '0']
> b
""")

	def test_should_not_accept_cancel_when_cancel_is_disabled(self):
		self.mockSingleCharacterInput('0b')
		self.assertEqual('elephant', get_from_dictionary(self.my_dict, show_cancel=False))
		self.assertOutput("""a) Mickey Mouse
b) Dumbo
c) Lassie
> 0
Must be one of: ['a', 'b', 'c']
> b
""")

	def test_should_force_return_when_configured(self):
		configure('force_return', True)
		self.mockInput('b\n')
		self.assertEqual('elephant', get_from_dictionary(self.my_dict, show_cancel=False))



class Test_show_functions(IOTestCase):

	def test_show_enumerated_list(self):
		show_enumerated_list(['mouse', 'elephant', 'dog'])
		self.assertOutput("""a) mouse
b) elephant
c) dog
""")

	def test_show_enumerated_list_when_empty(self):
		show_enumerated_list([])
		self.assertOutput("No entries\n")

	def test_show_headline(self):
		show_headline("Hello World")
		self.assertOutput("""
+-------------+
| Hello World |
+-------------+

""")

	def test_show_small_headline(self):
		show_small_headline("Hello World")
		self.assertOutput("""+--- Hello World ---+
""")



class Test_start_menu(IOTestCase):

	def test_start_menu(self):
		def first():
			print("first called")

		def second():
			print("second called")

		self.menu = collections.OrderedDict()
		self.menu['First Entry'] = first
		self.menu['Second Entry'] = second

		self.mockSingleCharacterInput('a0')
		start_menu(self.menu, "Hello World")

		self.assertOutput("""
+-------------+
| Hello World |
+-------------+

a) First Entry
b) Second Entry

0) Cancel
> a
first called

+-------------+
| Hello World |
+-------------+

a) First Entry
b) Second Entry

0) Cancel
> 0
""")

	def test_start_menu(self):
		def first():
			print("first called")

		def second():
			print("second called")

		self.menu = collections.OrderedDict()
		self.menu['First Entry'] = first
		self.menu['Second Entry'] = second

		self.mockSingleCharacterInput('ab0')
		start_menu(self.menu, "Hello World")

		self.assertOutput("""
+-------------+
| Hello World |
+-------------+

a) First Entry
b) Second Entry

0) Cancel
> a
first called

+-------------+
| Hello World |
+-------------+

a) First Entry
b) Second Entry

0) Cancel
> b
second called

+-------------+
| Hello World |
+-------------+

a) First Entry
b) Second Entry

0) Cancel
> 0
""")

	def test_start_menu_non_repeat(self):
		def first():
			print("first called")

		def second():
			print("second called")

		self.menu = collections.OrderedDict()
		self.menu['First Entry'] = first
		self.menu['Second Entry'] = second

		self.mockSingleCharacterInput('ab0')
		start_menu(self.menu, "Hello World", repeat=False)

		self.assertOutput("""
+-------------+
| Hello World |
+-------------+

a) First Entry
b) Second Entry

0) Cancel
> a
first called
""")

	def test_start_menu_hide_cancel(self):
		def first():
			print("first called")

		self.menu = collections.OrderedDict()
		self.menu['First Entry'] = first

		self.mockSingleCharacterInput('a')
		start_menu(self.menu, "Hello World", repeat=False, show_cancel=False)

		self.assertOutput("""
+-------------+
| Hello World |
+-------------+

a) First Entry
> a
first called
""")

	def test_start_menu_with_arguments(self):
		def first(firstname, surname):
			print("first called with {} {}".format(firstname, surname))

		self.menu = collections.OrderedDict()
		self.menu['First Entry'] = first

		self.mockSingleCharacterInput('a0')
		start_menu(self.menu, "Hello World", args=('Mickey', 'Mouse'))

		self.assertOutput("""
+-------------+
| Hello World |
+-------------+

a) First Entry

0) Cancel
> a
first called with Mickey Mouse

+-------------+
| Hello World |
+-------------+

a) First Entry

0) Cancel
> 0
""")

	def test_start_menu_with_keyword_arguments(self):
		def first(surname, firstname): # deliberately in the wrong order to test keyword args
			print("first called with {} {}".format(firstname, surname))

		self.menu = collections.OrderedDict()
		self.menu['First Entry'] = first

		self.mockSingleCharacterInput('a0')
		start_menu(self.menu, "Hello World", kwargs={'firstname': 'Mickey', 'surname': 'Mouse'})

		self.assertOutput("""
+-------------+
| Hello World |
+-------------+

a) First Entry

0) Cancel
> a
first called with Mickey Mouse

+-------------+
| Hello World |
+-------------+

a) First Entry

0) Cancel
> 0
""")

class Test_configure(IOTestCase):
	"""
	These are just the general configuration tests. EVerything specific to a particular function in the related test class
	"""

	def test_should_throw_exception_for_unknown_configuration(self):
		self.assertRaises(Exception, configure, 'unknown', 'value')

	def test_prompt(self):
		configure('prompt', '-->')

		self.mockInput('\n')
		get_string()
		self.assertOutput("-->")
