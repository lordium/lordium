import os
import sys
import subprocess

import install as Iscript

def after_install():
	msg = """
	Site setup is complete.
	"""
	print msg

def main(argv):
	#site name
	name = "lordium"
	#os.path.realpath(__file__) it will get the file path
	root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) # get the directory path

	#join path for virtual environment
	venv = os.path.join(root_folder, '.venv')

	#get the requirements path
	requirements_path = os.path.join(root_folder, 'requirements.txt')
	print "REQUIREMENTS PATH"
	print requirements_path

	#get the python version
	python_version = "python%s.%s" % (sys.version_info[0], sys.version_info[1])

	install = Iscript.Install(root_folder, venv, python_version,
							  requirements_path, name)
	options = install.parse_argv(argv)
	install.confirm_python_version()
	install.confirm_dependencies()
	install.create_venv(no_packages=options.no_site_packages)
	install.intall_dep()

	after_install()

if __name__ == '__main__':
	main(sys.argv)
