####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
# Copyright (C) 2017 Fabrice Salvaire
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

import logging

from Valentina.Pattern import Point, Line

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Tex:

    ##############################################

    def __init__(self, path):

        self._path = path

    ##############################################

    def open(self):

        self._file = open(self._path, 'w')
        self.write_preambule()

    ##############################################

    def close(self):

        self._file.write(r'''
\end{document}
''')
        self._file.close()

    ##############################################

    def write_preambule(self):

        self._file.write(r'''
\documentclass[12pt]{article}

%** Package ****************************************************************************************

%**** Page settings ******************************

\usepackage[%
paper=a0paper,%
%landscape,
%includeheadfoot,%
margin=5cm,%
headsep=0cm, footskip=0cm,%
dvips,%
]{geometry}

%**** Encoding ***********************************

\usepackage[utf8]{inputenc}

%*************************************************

\usepackage{tikz}
\usetikzlibrary{calc}
\usepgflibrary{arrows}

\usepackage{calc}

%***************************************************************************************************

\begin{document}
%
\pagestyle{empty}
%
''')

    ##############################################

    def add_detail_figure(self, pattern):

        self._file.write(r'''
\begin{center}
\begin{tikzpicture}[x=5mm,y=5mm]
''')

        for operation in pattern.operations:
            if isinstance(operation, Point):
                self._file.write(r'\coordinate ({0.name}) at ({0.vector.x:.2f},{0.vector.y:.2f});'.format(operation) + '\n')
                self._file.write(r'\fill [black] ({0.name}) circle (1pt);'.format(operation) + '\n')
                self._file.write(r'\draw ({0.name}) node[anchor=south west] {{{0.name}}};'.format(operation) + '\n')
        for operation in pattern.operations:
            if isinstance(operation, Line):
                self._file.write(r'\draw ({0.first_point.name}) -- ({0.second_point.name});'.format(operation) + '\n')

        self._file.write(r'''
\end{tikzpicture}
\end{center}
''')
