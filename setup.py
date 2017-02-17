#! /usr/bin/env python

####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
# Copyright (C) 2017 Salvaire Fabrice
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

import sys

from distutils.core import setup
# from setuptools import setup

####################################################################################################

if sys.version_info < (3,):
    print('PyValentina requires Python 3', file=sys.stderr)
    sys.exit(1)

exec(compile(open('setup_data.py').read(), 'setup_data.py', 'exec'))

setup(**setup_dict)

####################################################################################################
#
# End
#
####################################################################################################
