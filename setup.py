# --*- encoding: utf-8 -*--
## This file is adapted from projects
## jupyter-widgets/widget-ts-cookiecutter
## and sagemath/sage_sample

# Copyright (c) Jupyter Development Team.
# Copyright (c) Sagemath Development Team.
# Distributed under the terms of the Modified BSD License.

from os.path import join as pjoin
from codecs import open # To open the README file with proper encoding
from setuptools.command.test import test as TestCommand # for tests

from setupbase import (
    create_cmdclass, install_npm, ensure_targets,
    find_packages, combine_commands,
    HERE
)

from setuptools import setup

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

# The name of the project
name = 'sage-combinat-widgets'
pyname = 'sage_combinat_widgets' # basis for JS extension

js_path = pjoin(HERE, 'js')
nb_path = pjoin(HERE, pyname, 'nbextension', 'static')
lab_path = pjoin(HERE, pyname, 'labextension')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
    pjoin(HERE, 'js', 'lib', 'extension.js'),
]

package_data_spec = {
    name: [
        'nbextension/static/*.*js*',
        'nbextension/static/*.*css',
        'labextension/*.tgz'
    ]
}

data_files_spec = [
    ('share/jupyter/nbextensions/sage-combinat-widgets',
        nb_path, '*.js*'),
    ('share/jupyter/nbextensions/sage-combinat-widgets',
        nb_path, '*.css'),
    ('share/jupyter/lab/extensions', lab_path, '*.tgz'),
    ('etc/jupyter/nbconfig/notebook.d', HERE, 'sage-combinat-widgets.json')
]


cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
                           data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(pjoin(HERE, 'js'), build_cmd='build:all'),
    ensure_targets(jstargets),
)
cmdclass['test'] = SageTest

setup_args = dict(
    name            = name,
    version         = readfile("VERSION"),
    description     = 'Jupyter widgets for SAGE Combinat',
    long_description = readfile("README.rst"),
    cmdclass        = cmdclass,
    packages        = find_packages(),
    url             = 'https://github.com/sagemath/sage-combinat-widgets',
    author          = 'Odile Bénassy, Henri Derycke, Nicolas M. Thiéry',
    author_email    = 'odile.benassy@u-psud.fr',
    license         = 'GPLv3+',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'Widgets', 'SageMath', 'combinatorics'],
    classifiers     = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Jupyter',
    ],
    include_package_data = True,
    install_requires = [
        'ipywidgets>=7.5.0',
    ],
    extras_require = {
        'docs': [
            'sage-package',
            'sphinx>=1.5',
        ],
    },
)

if __name__ == "__main__":
    setup(**setup_args)
