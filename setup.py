#! /usr/bin/env python3

####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import glob
import sys

from setuptools import setup, find_packages
setuptools_available = True

####################################################################################################

if sys.version_info < (3,):
    print('Patro requires Python 3', file=sys.stderr)
    sys.exit(1)

exec(compile(open('setup_data.py').read(), 'setup_data.py', 'exec'))

####################################################################################################

def read_requirement():
    return [requirement.strip() for requirement in open('requirements.txt').readlines()]

####################################################################################################

setup_dict.update(dict(
    # include_package_data=True, # Look in MANIFEST.in
    packages=find_packages(exclude=['unit-test']),
    # scripts=glob.glob('bin/*'),
    # [
    #     'bin/...',
    # ],
    # package_data={
    #     'Patro.Config': ['logging.yml'],
    # },

    platforms='any',
    zip_safe=False, # due to data files

    # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Topic :: Scientific/Engineering',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        ],

    install_requires=read_requirement(),
))

####################################################################################################

setup(**setup_dict)
