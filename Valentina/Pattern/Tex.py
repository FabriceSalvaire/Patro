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

from ArithmeticInterval import Interval2D

from Valentina.Geometry.Vector import Vector2D
from Valentina.Math.Functions import rint
from . import Calculation

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

_preambule = r'''
\documentclass[12pt]{article}

%** Package ****************************************************************************************

%**** Page settings ******************************

\usepackage[%
paper=«0.paper»,%
%landscape,
%includeheadfoot,%
margin=«0.margin»mm,%
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
'''

####################################################################################################

class Tex:

    ##############################################

    def __init__(self, path, paper='a0paper', margin=10):

        self._path = path
        self._file = None
        self._paper = paper
        self._margin = margin

    ##############################################

    @property
    def paper(self):
        return self._paper

    @property
    def margin(self):
        return self._margin

    ##############################################

    @staticmethod
    def _format(pattern, *args, **kwargs):

        pattern = pattern.replace('{', '{{')
        pattern = pattern.replace('}', '}}')
        pattern = pattern.replace('«', '{')
        pattern = pattern.replace('»', '}')
        return pattern.format(*args, **kwargs)

    ##############################################

    def open(self):

        self._file = open(str(self._path), 'w')
        self.write_preambule()

    ##############################################

    def close(self):

        self._file.write(r'''\end{document}''' + '\n')
        self._file.close()

    ##############################################

    def write_preambule(self):

        self._file.write(self._format(_preambule, self))

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

    def detail_figure(self, pattern):

        source = ''
        for calculation in pattern.calculations:
            if isinstance(calculation, Calculation.Point):
                # \node [label={[shift={(1.0,0.3)}]Label}] {Node};
                source += r'\coordinate ({0.name}) at ({0.vector.x:.2f},{0.vector.y:.2f});'.format(calculation) + '\n'
                source += r'\fill [black] ({0.name}) circle (1pt);'.format(calculation) + '\n'
                # source += r'\draw[] ({0.name}) node[anchor=center] {{{0.name}}};'.format(calculation) + '\n'
                label_offset = calculation.label_offset
                offset = Vector2D(label_offset.x, -label_offset.y) # Fixme: ???
                label_position = calculation.vector + offset
                print(calculation.name, calculation.vector, offset, label_position)
                if offset:
                    # arrow must point to the label center and be clipped
                    source += r'\draw[line width=.5pt] ({0.vector.x:.2f},{0.vector.y:.2f}) -- ({1.x:.2f},{1.y:.2f}) ;'.format(calculation, label_position) + '\n'
                source += self._format(r'\draw[] («0.x:.2f»,«0.y:.2f») node[anchor=north west] {«1.name»};', label_position, calculation) + '\n'
#                 source += r'''
# {{
# \pgftransformshift{{\pgfpointxy{{{0.x:.2f}}}{{{0.y:.2f}}}}}
# \pgfnode{{rectangle}}{{north west}}{{{1.name}}}{{label{1.name}}}{{\pgfusepath{{stroke}}}}
# \pgfpathcircle{{\pgfpointanchor{{label{1.name}}}{{north}}}}{{2pt}}
# }}
# '''.format(label_position, calculation)

                if isinstance(calculation, Calculation.LinePropertiesMixin):
                    style = self._format_line_style(calculation, '2pt')
                    if isinstance(calculation, Calculation.AlongLinePoint):
                        source += r'\draw[{0}] ({1.first_point.name}) -- ({1.name});'.format(style, calculation) + '\n'
                    elif isinstance(calculation, Calculation.EndLinePoint):
                        source += r'\draw[{0}] ({1.base_point.name}) -- ({1.name});'.format(style, calculation) + '\n'
                    # elif isinstance(calculation, LineIntersectPoint):
                    #     source += r'\draw[{0}] ({1.point1_line1.name}) -- ({1.name});'.format(style, calculation) + '\n'
                    elif isinstance(calculation, Calculation.NormalPoint):
                        source += r'\draw[{0}] ({1.first_point.name}) -- ({1.name});'.format(style, calculation) + '\n'
            elif isinstance(calculation, Calculation.Line):
                style = self._format_line_style(calculation, '4pt')
                source += r'\draw[{0}] ({1.first_point.name}) -- ({1.second_point.name});'.format(style, calculation) + '\n'
            elif isinstance(calculation, Calculation.SimpleInteractiveSpline):
                style = self._format_line_style(calculation, '4pt')
                source += r'\draw[{0}] ({1.first_point.name}) .. controls ({1.control_point1.x:.2f},{1.control_point1.y:.2f}) and ({1.control_point2.x:.2f},{1.control_point2.y:.2f}) .. ({1.second_point.name});'.format(style, calculation) + '\n'

        return source

    ##############################################

    def add_tiled_detail_figure(self, pattern):

        bounding_box = pattern.bounding_box()
        print(bounding_box)

        paper_size = Vector2D(210, 297) / 10 # Fixme:
        figure_margin = 2
        paper_margin = (self._margin + figure_margin) / 10
        area_vector = paper_size - Vector2D(paper_margin, paper_margin) * 2
        number_of_columns = rint(bounding_box.x.length / area_vector.x)
        number_of_rows = rint(bounding_box.y.length / area_vector.y)

        print('Area {}'.format(area_vector))
        print('Grid {}x{}'.format(number_of_rows, number_of_columns))

        min_point = Vector2D((bounding_box.x.inf, bounding_box.y.inf))

        detail_figure = self.detail_figure(pattern)

        for r in range(number_of_rows):
            for c in range(number_of_columns):
                local_min_point = min_point + area_vector * Vector2D(r, c)
                local_max_point = local_min_point + area_vector
                interval = Interval2D((local_min_point.x, local_max_point.x), (local_min_point.y, local_max_point.y))
                print(r, c, interval)
                self._file.write(r'''
\begin{center}
\begin{tikzpicture}[x=10mm,y=10mm]
''')
                self._file.write(r'\draw[clip] ({0.x.inf:.2f},{0.y.inf:.2f}) -- ({0.x.sup:.2f},{0.y.inf:.2f}) -- ({0.x.sup:.2f},{0.y.sup:.2f}) -- ({0.x.inf:.2f},{0.y.sup:.2f}) -- cycle;'.format(interval) + '\n')
                self._file.write(detail_figure)
                self._file.write(r'''
\end{tikzpicture}
\end{center}
\newpage
''')

    ##############################################

    def add_detail_figure(self, pattern, interval=None):

        # Fixme: scale!
        self._file.write(r'''
\fontsize{64}{72}\selectfont % \fontsize{size}{baselineskip}
\begin{center}
\begin{tikzpicture}[x=8mm,y=8mm]
''')
        self._file.write(self.detail_figure(pattern))
        self._file.write(r'''
\end{tikzpicture}
\end{center}
\normalsize
''')
