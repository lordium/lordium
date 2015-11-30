# from pip.req import parse_requirements
from distutils.core import setup

# install_reqs = parse_requirements('requirements.txt')
# reqs = [str(ir.req) for ir in install_reqs]
import os
from setuptools import setup
with open('requirements.txt') as f:
    required = f.read().splitlines()



setup(
    # Application name:
    name="lordium",

    # Version number (initial):
    version="0.0.1",

    # Application author details:
    author="Arslan Rafique",
    author_email="mailtoarslan@gmail.com",

    # Packages
    packages=["lordium"],

    # Include additional files into the package
    include_package_data=False,

    # Details
    url="http://pypi.python.org/pypi/arslanrafique_v010/",

    #
    # license="LICENSE.txt",
    description="Awesome",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=required
)
