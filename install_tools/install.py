from __future__ import print_function

import os
import sys
import optparse
import subprocess


class Install(object):

	def __init__(self, root_path, venv_path,
				python_version, requirements_path,
				name):

		self.root_path = root_path
		self.venv_path = venv_path
		self.python_version = python_version
		self.requirements_path = requirements_path
		self.name = name

	def terminate(self, mesg, *args):
		print(mesg % args, file=sys.stderr)
		sys.exit(1)

	def confirm_python_version(self):
		if sys.version_info < (2, 6): #python2.6 and above
			self.terminate("Python version below 2.6 is not supported.")

	def get_os_type(self):
		if (os.path.exists('/etc/fedora-release') or
				os.path.exists('/etc/redhat-release')):
			return Fedora(
				self.root_path, self.venv_path, self.requirements_path,
				self.python_version, self.name)
		else:
			return Distro(
				self.root_path, self.venv_path, self.requirements_path,
				self.python_version, self.name)

	def confirm_dependencies(self):
		self.get_os_type().install_venv()

	def execute_command_abs(self, command, redirect=True, check_exit=True):
		"""
		Executes commands and displays the output
		"""
		if redirect:
			std_out = subprocess.PIPE
		else:
			std_out = None

		pros = subprocess.Popen(command, cwd=self.root_path, stdout=std_out)
		output = pros.communicate()[0]

		if check_exit and pros.returncode != 0:
			self.terminate("Command '%s' failed.\n%s", ' '.join(command), output)
		return (output, pros.returncode)

	def execute_command(self, command, redirect=True, check_exit=True):
		return self.execute_command_abs(command, redirect, check_exit)[0]

	def create_venv(self, no_packages = True):
		"""
		Create virtual environment here and install PIP.
		"""
		if not os.path.isdir(self.venv_path):
			print('Creating Virtual Environment')
			if no_packages:
				self.execute_command(['virtualenv', '-q', '--no-site-package',
									 self.venv_path])
			else:
				self.execute_command(['virtualenv', '-q', self.venv_path])
			print('Done')
		else:
			print("venv already exists")

	def pip_install(self, *args):
		self.execute_command(['install_tools/act_venv.sh',
							  'pip', 'install', '--upgrade'] + list(args),
							  redirect=False)

	def intall_dep(self):
		print("Installing dependencies with pip...")

		self.pip_install('pip>=1.4')
		self.pip_install('setuptools')
		# self.pip_install('pbr')

		self.pip_install('-r', self.requirements_path)

	def parse_argv(self, argv):
		parser = optparse.OptionParser()
		parser.add_option('-n', '--no-site-packages',
						  action='store_true',
						  help='')
		return parser.parse_args(argv[1:])[0]

class Distro(Install):

	def check_command(self, cmd):
		return bool(self.execute_command(['which', cmd],
					check_exit=False).strip())

	def install_venv(self):
		if self.check_command('easy_install'):
			print('Installing virtual env using easy_install.', end=" ")
		if self.execute_command(['easy_install', 'virtualenv']):
			print('Success')
			return
		else:
			print('Failed')

		self.terminate('Error: virtualenv not found.\n\n%s'
			' requires virtualenv, please install it.' % self.name)

class Fedora(Distro):

	def check_package(self, pkg):
		return self.execute_command_abs(['rpm', '-q', pkg],
									check_exit=False)[1] == 0

	def install_venv(self):
		if self.check_command('virtualenv'):
			return
		if not self.check_package('python-virtualenv'):
			self.terminate("Please install 'python-virtualenv'.")

		super(Fedora, self).install_venv()
