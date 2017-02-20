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

from Valentina.Geometry.Vector2D import Vector2D
from . import Calculation

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Tex:

    ##############################################

    def __init__(self, path):

        self._path = path
        self._file = None

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

    __LINE_STYLE__ = {
        None: None,
        'dashDotLine': 'dash pattern=on 5mm off 4mm on 2mm off 4mm', # 'loosely dashdotted',
        'dotLine': 'dash pattern=on 2mm off 2mm', # 'dotted',
        'hair': 'solid',
        'none': None,

        'solid': 'solid',
        }

    __LINE_COLOR__ = {
        None : None,
        'black': 'black',
        }

    @staticmethod
    def _line_style(line):

        return Tex.__LINE_STYLE__[line.line_style], Tex.__LINE_COLOR__[line.line_color]

    @staticmethod
    def _format_line_style(line, line_width):

        line_style, line_color = Tex._line_style(line)
        style = 'line width={}'.format(line_width)
        if line_style is not None:
            style += ', {}'.format(line_style)
        if line_color is not None:
            style += ', {}'.format(line_color)
        return style

    ##############################################

    def add_detail_figure(self, pattern):

        self._file.write(r'''
\fontsize{64}{72}\selectfont % \fontsize{size}{baselineskip}
\begin{center}
\begin{tikzpicture}[x=8mm,y=8mm]
''')

        # \draw[clip] (0,0) -- (30,0) -- (30,-30) -- (0,-30) -- cycle;

        for calculation in pattern.calculations:
            if isinstance(calculation, Calculation.Point):
                # \node [label={[shift={(1.0,0.3)}]Label}] {Node};
                self._file.write(r'\coordinate ({0.name}) at ({0.vector.x:.2f},{0.vector.y:.2f});'.format(calculation) + '\n')
                self._file.write(r'\fill [black] ({0.name}) circle (1pt);'.format(calculation) + '\n')
                # self._file.write(r'\draw[] ({0.name}) node[anchor=center] {{{0.name}}};'.format(calculation) + '\n')
                label_offset = calculation.label_offset
                offset = Vector2D(label_offset.x, -label_offset.y) # Fixme: ???
                label_position = calculation.vector + offset
                print(calculation.name, calculation.vector, offset, label_position)
                if offset:
                    # arrow must point to the label center and be clipped
                    self._file.write(r'\draw[line width=.5pt] ({0.vector.x:.2f},{0.vector.y:.2f}) -- ({1.x:.2f},{1.y:.2f}) ;'.format(calculation, label_position) + '\n')
                self._file.write(r'\draw[] ({0.x:.2f},{0.y:.2f}) node[anchor=north west] {{{1.name}}};'.format(label_position, calculation) + '\n')
#                 self._file.write(r'''
# {{
# \pgftransformshift{{\pgfpointxy{{{0.x:.2f}}}{{{0.y:.2f}}}}}
# \pgfnode{{rectangle}}{{north west}}{{{1.name}}}{{label{1.name}}}{{\pgfusepath{{stroke}}}}
# \pgfpathcircle{{\pgfpointanchor{{label{1.name}}}{{north}}}}{{2pt}}
# }}
# '''.format(label_position, calculation))

                if isinstance(calculation, Calculation.LinePropertiesMixin):
                    style = self._format_line_style(calculation, '2pt')
                    if isinstance(calculation, Calculation.AlongLinePoint):
                        self._file.write(r'\draw[{0}] ({1.first_point.name}) -- ({1.name});'.format(style, calculation) + '\n')
                    elif isinstance(calculation, Calculation.EndLinePoint):
                        self._file.write(r'\draw[{0}] ({1.base_point.name}) -- ({1.name});'.format(style, calculation) + '\n')
                    # elif isinstance(calculation, LineIntersectPoint):
                    #     self._file.write(r'\draw[{0}] ({1.point1_line1.name}) -- ({1.name});'.format(style, calculation) + '\n')
                    elif isinstance(calculation, Calculation.NormalPoint):
                        self._file.write(r'\draw[{0}] ({1.first_point.name}) -- ({1.name});'.format(style, calculation) + '\n')
            elif isinstance(calculation, Calculation.Line):
                style = self._format_line_style(calculation, '4pt')
                self._file.write(r'\draw[{0}] ({1.first_point.name}) -- ({1.second_point.name});'.format(style, calculation) + '\n')
            elif isinstance(calculation, Calculation.SimpleInteractiveSpline):
                style = self._format_line_style(calculation, '4pt')
                self._file.write(r'\draw[{0}] ({1.first_point.name}) .. controls ({1.control_point1.x:.2f},{1.control_point1.y:.2f}) and ({1.control_point2.x:.2f},{1.control_point2.y:.2f}) .. ({1.second_point.name});'.format(style, calculation) + '\n')

        self._file.write(r'''
\end{tikzpicture}
\end{center}
\normalsize
''')
