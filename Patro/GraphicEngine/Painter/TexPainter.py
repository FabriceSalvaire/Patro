####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2017 Fabrice Salvaire
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

import logging

from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.TeX.Document import Document
from Patro.GraphicEngine.TeX.Environment import Center
from Patro.GraphicEngine.TeX.Tikz import TikzFigure
from .Painter import Painter, Tiler

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

_preambule = r'''
%** Package ****************************************************************************************

%**** Page settings ******************************

\usepackage[%
paper=«0.paper_name»,%
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

'''

####################################################################################################

class TexPainter(Painter):

    ##############################################

    def __init__(self, path, scene, paper):

        super().__init__(scene)

        self._document = Document(path, 'article', '12pt')
        self._paper = paper

        self._preambule.append(Document._format(_preambule, self))

    ##############################################

    @property
    def paper_name(self):
        return self._paper.name.lower() + 'paper'

    @property
    def margin(self):
        return self._paper.margin

    @property
    def _preambule(self):
        return self._document.preambule

    @property
    def _content(self):
        return self._document.content

    ##############################################

    def _format_position(self, position):

        if isinstance(position, str):
            return '(' + position + ')'
        elif isinstance(position, Vector2D):
            return '({0.x:.2f},{0.y:.2f})'.format(position)

    ##############################################

    def paint(self):

        for item in self._scene.coordinates:
            self.paint_CoordinateItem(item)
        super().paint()

    ##############################################

    def paint_CoordinateItem(self, item):

        # Fixme: implement detail in TikzFigure ?

        coordinate = self._format_position(item.position)
        self._figure.append(r'\coordinate ({0}) at {1};'.format(item.name, coordinate) + '\n')

    ##############################################

    def paint_TextItem(self, item):

        coordinate = self._format_position(item.position)
        self._figure.append(Document._format(r'\draw[] «0» node[anchor=north west] {«1»};', coordinate, item.text) + '\n')

    ##############################################

    def paint_CircleItem(self, item):

        coordinate = self._format_position(item.position)
        self._figure.append(r'\fill [black] {0} circle (1pt);'.format(coordinate) + '\n')

    ##############################################

    def paint_SegmentItem(self, item):

        style = TikzFigure.format_path_style(item.path_style)
        coordinates = [self._format_position(position) for position in item.positions]
        self._figure.append(r'\draw[{0}] {1} -- {2};'.format(style, *coordinates) + '\n')

    ##############################################

    def paint_CubicBezierItem(self, item):

        style = TikzFigure.format_path_style(item.path_style)
        coordinates = [self._format_position(position) for position in item.positions]
        self._figure.append(r'\draw[{0}] {1} .. controls {2} and {3} .. {4};'.format(style, *coordinates) + '\n')

    ##############################################

    def _add_pagestyle_empty(self):

        # Fixme: implement in Document ?
        self._content.append(r'\pagestyle{empty}' + '\n')

    ##############################################

    def add_detail_figure(self):

        # Fixme: split document / scene painter
        #  don't make sense to generate a0 and a4 content on the same file !

        self._add_pagestyle_empty()
        self._content.append(r'\fontsize{64}{72}\selectfont % \fontsize{size}{baselineskip}' + '\n')
        options = 'x=8mm,y=8mm'
        self._figure = TikzFigure(options)
        self._content.append(Center().append(self._figure))
        self.paint()

    ##############################################

    def add_tiled_detail_figure(self):

        self._add_pagestyle_empty()
        tiler = Tiler(self._scene.bounding_box, self._paper)
        for interval, r, c in tiler:
            options = 'x=10mm,y=10mm'
            self._figure = TikzFigure(options)
            offset = 1
            self._figure.append(r'\fontsize{128}{128}\selectfont % \fontsize{size}{baselineskip}' + '\n')
            self._figure.append(r'\color{gray!50}' + '\n')
            self._figure.append(
                Document._format(r'\draw[] («0»,«1») node[anchor=south west] {«2», «3»};',
                                 interval.x.inf + offset,
                                 interval.y.inf + offset,
                                 r+1,
                                 c+1,
                ) + '\n')
            self._figure.append(r'\fontsize{14}{16}\selectfont % \fontsize{size}{baselineskip}' + '\n')
            self._figure.append(r'\color{black}' + '\n')
            self._figure.append(r'\draw[clip] '
                                r'({0.x.inf:.2f},{0.y.inf:.2f}) -- '
                                r'({0.x.sup:.2f},{0.y.inf:.2f}) -- '
                                r'({0.x.sup:.2f},{0.y.sup:.2f}) -- '
                                r'({0.x.inf:.2f},{0.y.sup:.2f}) -- cycle;'.format(interval) + '\n')
            self._content.append(Center().append(self._figure))
            self.paint()
