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

__all__ = [
    'SvgPainter',
]

####################################################################################################

# See also
#   https://github.com/mozman/svgwrite
#   https://svgwrite.readthedocs.io/en/master/

####################################################################################################

import logging

from Patro.FileFormat.Svg import SvgFormat
from Patro.FileFormat.Svg.SvgFile import SvgFileWriter
from Patro.GeometryEngine.Transformation import AffineTransformation2D
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicStyle import StrokeStyle
from .Painter import Painter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SvgPainter(Painter):

    __STROKE_STYLE__ = {
        StrokeStyle.NoPen: None,
        StrokeStyle.SolidLine: None,
        StrokeStyle.DashLine: [6, 3], # Fixme:
        StrokeStyle.DotLine: [1, 2], # Fixme:
        StrokeStyle.DashDotLine: [6, 3], # Fixme:
        StrokeStyle.DashDotDotLine: [6, 3], # Fixme:
    }

    ##############################################

    def __init__(self, path, scene, paper):

        super().__init__(scene)

        self._path = path
        self._paper = paper

        bounding_box = scene.bounding_box
        self._transformation = AffineTransformation2D.Scale(10, -10)
        self._transformation *= AffineTransformation2D.Translation(-Vector2D(bounding_box.x.inf, bounding_box.y.sup))

        self._tree = []
        self._append(SvgFormat.Style(text='''
        .normal { font: 12px sans-serif; }
        '''))
        self.paint()

        self._svg_file = SvgFileWriter(path, paper, self._tree, transformation=None)

    ##############################################

    def cast_position(self, position):
        return self._transformation * super().cast_position(position)

    ##############################################

    def _append(self, element):
        self._tree.append(element)

    ##############################################

    def _graphic_style(self, item):

        path_syle = item.path_style
        color = path_syle.stroke_color.name
        line_style = self.__STROKE_STYLE__[path_syle.stroke_style]
        line_width = str(path_syle.line_width_as_float)

        kwargs = dict(stroke=color, stroke_width=line_width)
        if line_style:
            kwargs['stroke_dasharray'] = line_style

        return kwargs

    ##############################################

    def paint_TextItem(self, item):

        x, y = list(self.cast_position(item.position))
        # Fixme: anchor position
        text = SvgFormat.Text(x=x, y=y, text=item.text, fill='black')
        self._append(text)

    ##############################################

    def paint_CircleItem(self, item):

        x, y = self.cast_position(item.position)
        circle = SvgFormat.Text(cx=x, cy=y, r=2, fill='black', _class='normal')
        self._append(circle)

    ##############################################

    def paint_SegmentItem(self, item):

        p1, p2 = self.cast_item_positions(item)
        line = SvgFormat.Line(
            x1=p1.x,
            y1=p1.y,
            x2=p2.x,
            y2=p2.y,
            **self._graphic_style(item),
        )
        self._append(line)

    ##############################################

    def paint_CubicBezierItem(self, item):

        coordinates = self.cast_item_coordinates(item, flat=True)
        path = SvgFormat.Path(
            path_data='M {} {} C {} {}, {} {}, {} {}'.format(*coordinates),
            fill='none',
            **self._graphic_style(item),
        )
        #!# self._append(path)

