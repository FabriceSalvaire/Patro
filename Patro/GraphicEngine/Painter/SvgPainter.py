####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
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

__all__ = [
    'SvgPainter',
]

####################################################################################################

import logging

from Patro.FileFormat.Svg.SvgFile import SvgFile
from Patro.FileFormat.Svg import SvgFormat
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GeometryEngine.Transformation import AffineTransformation2D
from .Painter import Painter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SvgPainter(Painter):

    __STROKE_STYLE__ = {
        None: None,
        'dashDotLine': [6, 3],
        'dotLine': [1, 2],
        'hair': None,
        'none': None, # Fixme: ???

        'solid': None,
    }

    __COLOR__ = {
        None : None,
        'black': 'black',
    }

    ##############################################

    def __init__(self, path, scene, paper):

        super().__init__(scene)

        self._path = path
        self._paper = paper

        self._coordinates = {}

        bounding_box = scene.bounding_box
        self._transformation = AffineTransformation2D.Scale(10, -10)
        self._transformation *= AffineTransformation2D.Translation(-Vector2D(bounding_box.x.inf, bounding_box.y.sup))

        self._tree = []

        self._append(SvgFormat.Style(text='''
        .normal { font: 12px sans-serif; }
        '''))

        self.paint()

        self._svg_file = SvgFile()
        self._svg_file.write(paper, self._tree, transformation=None, path=path)

    ##############################################

    def _append(self, element):
        self._tree.append(element)

    ##############################################

    def _cast_position(self, position):

        # Fixme: to base class

        if isinstance(position, str):
            position = self._coordinates[position]
        return self._transformation * position

    ##############################################

    def paint_CoordinateItem(self, item):

        # Fixme: to base class
        self._coordinates[item.name] = item.position

    ##############################################

    def _cast_positions(self, positions):

        vertices = []
        for position in positions:
            vertices += list(self._cast_position(position))
        return vertices

    ##############################################

    def _graphic_style(self, item):

        path_syle = item.path_style
        color = self.__COLOR__[path_syle.stroke_color]
        line_style = self.__STROKE_STYLE__[path_syle.stroke_style]
        line_width = str(float(path_syle.line_width.replace('pt', '')) / 3) # Fixme: pt ???

        kwargs = dict(stroke=color, stroke_width=line_width)
        if line_style:
            kwargs['stroke_dasharray'] = line_style

        return kwargs

    ##############################################

    def paint_TextItem(self, item):

        x, y = list(self._cast_position(item.position))
        # Fixme: anchor position
        text = SvgFormat.Text(x=x, y=y, text=item.text, fill='black')
        self._append(text)

    ##############################################

    def paint_CircleItem(self, item):

        x, y = list(self._cast_position(item.position))
        circle = SvgFormat.Text(cx=x, cy=y, r=2, fill='black', _class='normal')
        self._append(circle)

    ##############################################

    def paint_SegmentItem(self, item):

        x1, y1, x2, y2 = self._cast_positions(item.positions)
        line = SvgFormat.Line(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            **self._graphic_style(item),
        )
        self._append(line)

    ##############################################

    def paint_CubicBezierItem(self, item):

        path = SvgFormat.Path(
            path_data='M {} {} C {} {}, {} {}, {} {}'.format(*self._cast_positions(item.positions)),
            fill='none',
            **self._graphic_style(item),
        )
        self._append(path)

