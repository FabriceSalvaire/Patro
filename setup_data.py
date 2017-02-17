####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Making Software
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

import os

####################################################################################################

long_description = open('README.rst').read()

####################################################################################################

setup_dict = dict(
    name='PyValentina',
    version='0.1.0',
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    description='A Python implementation of Valentina Pattern Making Software.',
    license="GPLv3",
    keywords="pattern making, valentina",
    url='https://github.com/FabriceSalvaire/PyValentina',
    scripts=[],
    packages=['Valentina', # Fixme:
              'Valentina.Math',
              'Valentina.Tools',
          ],
    # package_dir = {'PyValentina': 'PyValentina'},
    data_files=[],
    long_description=long_description,
    # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Education",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        ],
    requires=[
        'numpy',
    ],
)

####################################################################################################
#
# End
#
####################################################################################################
