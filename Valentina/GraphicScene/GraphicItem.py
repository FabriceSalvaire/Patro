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

# from Valentina.Geometry.Vector import Vector2D

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PathStyle:

    ##############################################

    def __init__(self, stroke_style=None, line_width=None, stroke_color=None, fill_color=None):

        self._stroke_style = stroke_style
        self._line_width = line_width
        self._stroke_color = stroke_color
        self._fill_color = fill_color

    ##############################################

    @property
    def stroke_style(self):
        return self._stroke_style

    @stroke_style.setter
    def stroke_style(self, value):
        self._stroke_style = value

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        self._line_width = value

    @property
    def stroke_color(self):
        return self._stroke_color

    @stroke_color.setter
    def stroke_color(self, value):
        self._stroke_color = value

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value):
        self._fill_color = value

####################################################################################################

class GraphicItem:
    pass

    ##############################################

    # def __init__(self):
    #     pass

####################################################################################################

class PositionMixin:

    ##############################################

    def __init__(self, position):

        # Fixme: could be Vector2D or name
        self._position = position # Vector2D(position)

    ##############################################

    @property
    def position(self):
        return self._position

    # @position.setter
    # def position(self, value):
    #     self._position = value

    @property
    def positions(self):
        return (self._position)

####################################################################################################

class TwoPositionMixin:

    ##############################################

    def __init__(self, position1, position2):

        # Fixme: could be Vector2D or name
        self._position1 = position1
        self._position2 = position2

    ##############################################

    @property
    def position1(self):
        return self._position1

    @property
    def position2(self):
        return self._position2

    @property
    def positions(self):
        return (self._position1, self._position2)

####################################################################################################

class FourPositionMixin(TwoPositionMixin):

    ##############################################

    def __init__(self, position1, position2, position3, position4):

        TwoPositionMixin.__init__(self, position1, position2)
        self._position3 = position3
        self._position4 = position4

    ##############################################

    @property
    def position3(self):
        return self._position3

    @property
    def position4(self):
        return self._position4

    @property
    def positions(self):
        return (self._position1, self._position2, self._position3, self._position4)

####################################################################################################

class CoordinateItem(GraphicItem, PositionMixin):

    ##############################################

    def __init__(self, name, position):

        GraphicItem.__init__(self)
        PositionMixin.__init__(self, position)
        self._name = str(name)

    ##############################################

    @property
    def name(self):
        return self._name

####################################################################################################

class TextItem(GraphicItem, PositionMixin):

    ##############################################

    def __init__(self, position, text):

        GraphicItem.__init__(self)
        PositionMixin.__init__(self, position)
        self._text = str(text)

    ##############################################

    @property
    def text(self):
        return self._text

    # @text.setter
    # def text(self, value):
    #     self._text = value

####################################################################################################

class PathItem:

    ##############################################

    def __init__(self, path_style):

        self._path_style = path_style

    ##############################################

    @property
    def path_style(self):
        return self._path_style

    # @path_style.setter
    # def path_style(self, value):
    #     self._path_style = value

####################################################################################################

class CircleItem(PathItem, PositionMixin):

    ##############################################

    def __init__(self, position, radius, path_style):

        PathItem.__init__(self, path_style)
        PositionMixin.__init__(self, position)
        self._radius = radius

    ##############################################

    @property
    def radius(self):
        return self._radius

    # @radius.setter
    # def radius(self, value):
    #     self._radius = value

####################################################################################################

class SegmentItem(PathItem, TwoPositionMixin):

    ##############################################

    def __init__(self, position1, position2, path_style): # segment

        PathItem.__init__(self, path_style)
        TwoPositionMixin.__init__(self, position1, position2)
        # super(SegmentItem, self).__init__(path_style)
        # self._segment = segment

    ##############################################

    # @property
    # def segment(self):
    #     return self._segment

    # @segment.setter
    # def segment(self, value):
    #     self._segment = value

####################################################################################################

class CubicBezierItem(PathItem, FourPositionMixin):

    ##############################################

    def __init__(self, position1, position2, position3, position4, path_style): # , curve

        # Fixme: curve vs path

        PathItem.__init__(self, path_style)
        FourPositionMixin.__init__(self, position1, position2, position3, position4)

        # super(CubicBezierItem, self).__init__(path_style)
        # self._curve = curve

    ##############################################

    # @property
    # def curve(self):
    #     return self._curve

    # @curve.setter
    # def curve(self, value):
    #     self._curve = value
