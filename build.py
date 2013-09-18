"""
Copyright (c) 2013, Jonas Pfannschmidt
Licensed under the MIT license http://www.opensource.org/licenses/mit-license.php
"""
import subprocess
import shutil
import os
from simplemenus import *
from collections import OrderedDict

def build():
	document()
	subprocess.check_call(['python', 'setup.py', 'build'])

def dist():
	document()
	subprocess.check_call(['python', 'setup.py', 'sdist'])
	subprocess.check_call(['python', 'setup.py', 'bdist_wininst'])

def install():
	subprocess.check_call(['python', 'setup.py', 'install'])

def clean():
	subprocess.check_call(['python', 'setup.py', 'clean', '--all'])

def test():
	subprocess.check_call(['python', '-m', 'unittest', 'discover'])

def run_pydoc(module):
	subprocess.check_call(['python', '-m', 'pydoc', '-w', module])
	shutil.move(module + '.html', 'docs/' + module + '.html')

def document():
	run_pydoc('simplemenus')
	run_pydoc('simplemenus.main')
	run_pydoc('simplemenus.xgetch')
	run_pydoc('simplemenus.test')

def tour():
	# Add the current directory to the PYTHONPATH to allow "import simplemenus" in the example.
	# It worked automatically for build.py because the current path is always in PYTHONPATH.
	env = os.environ.copy()
	env["PYTHONPATH"] = "." + (";" + env["PYTHONPATH"] if "PYTHONPATH" in env else "")
	subprocess.check_call(['python', 'examples/tour.py'], env=env)

if __name__=="__main__":
	mymenu = OrderedDict()
	mymenu['Build'] = build
	mymenu['Install'] = install
	mymenu['Clean'] = clean
	mymenu['Dist'] = dist
	mymenu['Run Tests'] = test
	mymenu['Export Documentation'] = document
	mymenu['Tour'] = tour

	start_menu(mymenu, "SimpleMenus Build Tool")