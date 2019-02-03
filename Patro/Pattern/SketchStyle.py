####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Fabrice Salvaire
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

"""Module to implement sketch style.

"""

####################################################################################################

from Patro.GraphicEngine.GraphicScene.GraphicStyle import GraphicPathStyle, Font
from Patro.GraphicEngine.GraphicScene.TypographyUnit import PointUnit
from Patro.GraphicStyle import Colors

####################################################################################################

class DetailSketchStyle:

    """Class to implement detail sketch style"""

    ##############################################

    def __init__(self, **kargs):

        self.point_size = kargs.get('point_size', .2)
        self.point_color = kargs.get('point_color', Colors.black)

        font_size = kargs.get('font_size', 16)
        self.font = Font('', font_size)
        self.label_line_width = kargs.get('label_line_width', 2)

        self.line_width = kargs.get('line_width', 3)
        self.construction_line_width = kargs.get('construction_line_width', 1.5)

    ##############################################

    @property
    def point_size(self):
        return self._point_size

    @point_size.setter
    def point_size(self, value):
        self._point_size = value

    @property
    def point_color(self):
        return self._point_color

    @point_color.setter
    def point_color(self, value):
        self._point_color = Colors.ensure_color(value)

    @property
    def point_style(self):
        return GraphicPathStyle(fill_color=self._point_color)

    ##############################################

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

    @property
    def label_line_width(self):
        return self._label_line_width

    @label_line_width.setter
    def label_line_width(self, value):
        self._label_line_width = value

    @property
    def label_line_style(self):
        return GraphicPathStyle(line_width=self._label_line_width)

    ##############################################

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        self._line_width = value

    @property
    def construction_line_width(self):
        return self._construction_line_width

    @construction_line_width.setter
    def construction_line_width(self, value):
        self._construction_line_width = value

