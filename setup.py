from distutils.core import setup

version = '0.6'

setup(
	name='SimpleMenus',
	version=version,
	author='Jonas Pfannschmidt',
	author_email='jonas.pfannschmidt@gmail.com',
	license='MIT license http://www.opensource.org/licenses/mit-license.php',
	description='A few simple methods to create interactive console applications.',
	long_description=open('README.txt').read(),
	url = 'http://www.pulsedo.com/free/simplemenus',
	download_url = 'http://www.pulsedo.com/free/simplemenus/download/SimpleMenus-' + version + '.zip',
	packages=['simplemenus', 'simplemenus.test'],
	classifiers= [
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Environment :: Console"
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Topic :: Software Development :: User Interfaces",
		"Topic :: Software Development :: Libraries :: Python Modules"
		]
	)