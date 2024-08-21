#! /usr/bin/env python3

####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import sys

from setuptools import setup

####################################################################################################

# Check for python3 setup.py install
required_python_version = (3, 10)
if sys.version_info < required_python_version:
    sys.stderr.write('ERROR: PySpice requires Python {}.{}\n'.format(*required_python_version))
    sys.exit(1)
####################################################################################################

from setup_data import setup_dict
setup(**setup_dict)
