## -*- encoding: utf-8 -*-
import os
import sys
from setuptools import setup
from codecs import open # To open the README file with proper encoding
from setuptools.command.test import test as TestCommand # for tests


# Get information from separate files (README, VERSION)
def readfile(filename):
    with open(filename,  encoding='utf-8') as f:
        return f.read()

# For the tests
class SageTest(TestCommand):
    def run_tests(self):
        errno = os.system("sage -t --force-lib sage_widget_adapters")
        if errno != 0:
            sys.exit(1)
        errno = os.system("sage -t --force-lib sage_combinat_widgets")
        if errno != 0:
            sys.exit(1)

setup(
    name = "sage-combinat-widgets",
    version = readfile("VERSION"),
    description='Jupyter widgets for SAGE Combinat',
    long_description = readfile("README.rst"),
    url='https://github.com/sagemath/sage-combinat-widgets',
    author='Odile Bénassy, Nicolas M. Thiéry',
    author_email='odile.benassy@u-psud.fr',
    license='GPLv3+',
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering :: Mathematics',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Programming Language :: Python :: 2.7',
    ], # classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords = "SageMath widget combinatorics",
    packages = ['sage_combinat_widgets', 'sage_widget_adapters', 'sage_widget_adapters.combinat', 'sage_widget_adapters.graphs', 'sage_widget_adapters.matrix'],
    cmdclass = {'test': SageTest}, # adding a special setup command for tests
    install_requires = ['ipywidgets']
)
