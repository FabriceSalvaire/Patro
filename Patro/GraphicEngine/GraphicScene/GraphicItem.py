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

####################################################################################################

import logging

from Patro.GeometryEngine.Bezier import CubicBezier2D
from Patro.GeometryEngine.Conic import Circle2D, Conic2D
from Patro.GeometryEngine.Rectangle import Rectangle2D
from Patro.GeometryEngine.Segment import Segment2D

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GraphicStyle:

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

    @property
    def casted_position(self):
        return self._scene.cast_position(self._position)

####################################################################################################

class TwoPositionMixin:

    ##############################################

    def __init__(self, position1, position2):
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

class StartStopAngleMixin:

    ##############################################

    def __init__(self, start_angle=0, stop_angle=360):
        self._start_angle = start_angle
        self._stop_angle = stop_angle

    ##############################################

    @property
    def start_angle(self):
        return self._start_angle

    # @start_angle.setter
    # def start_angle(self, value):
    #     self._start_angle = value

    @property
    def stop_angle(self):
        return self._stop_angle

    # @stop_angle.setter
    # def stop_angle(self, value):
    #     self._stop_angle = value

####################################################################################################

class CoordinateItem(PositionMixin):

    ##############################################

    def __init__(self, name, position):

        PositionMixin.__init__(self, position)

        self._name = str(name)

    ##############################################

    @property
    def name(self):
        return self._name

####################################################################################################

class GraphicItem:

    # clipping
    # opacity

    __subclasses__ = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__subclasses__.append(cls)

    ##############################################

    def __init__(self, scene, user_data):

        self._scene = scene
        self._user_data = user_data

        self._z_value = 0

        self._visible = True
        self._selected = False

        self._dirty = True
        self._geometry = None
        self._bounding_box = None

    ##############################################

    @property
    def scene(self):
        return self._scene

    @property
    def user_data(self):
        return self._user_data

    ##############################################

    def __hash__(self):
        return hash(self._user_data)

    ##############################################

    @property
    def z_value(self):
        return self._z_value

    @z_value.setter
    def z_value(self, value):
        self._z_value = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = bool(value)

    ##############################################

    @property
    def positions(self):
        raise NotImplementedError

    ##############################################

    @property
    def casted_positions(self):
        cast = self._scene.cast_position
        return [cast(position) for position in self.positions]

    ##############################################

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):

        if bool(value):
            self._dirty = True
        else:
            self._dirty = True
            self._geometry = None
            self._bounding_box = None

    ##############################################

    @property
    def bounding_box(self):
        if self._bounding_box is None:
            self._bounding_box = self.get_bounding_box()
        return self._bounding_box

    @property
    def geometry(self):
        if self._geometry is None:
            self._geometry = self.get_geometry()
            self._dirty = False
        return self._geometry

    ##############################################

    def get_geometry(self):
        raise NotImplementedError

    ##############################################

    def get_bounding_box(self):
        return self.geometry.bounding_box

    ##############################################

    def distance_to_point(self, point):
        return self.geometry.distance_to_point(point)

####################################################################################################

class TextItem(PositionMixin, GraphicItem):

    # font

    ##############################################

    def __init__(self, scene, position, text, user_data):

        GraphicItem.__init__(self, scene, user_data)
        PositionMixin.__init__(self, position)

        self._text = str(text)

    ##############################################

    @property
    def text(self):
        return self._text

    # @text.setter
    # def text(self, value):
    #     self._text = value

    ##############################################

    def get_geometry(self):
        position = self.casted_position
        # Fixme:
        return Rectangle2D(position, position)

####################################################################################################

class PathStyleItemMixin(GraphicItem):

    ##############################################

    def __init__(self, scene, path_style, user_data):

        GraphicItem.__init__(self, scene, user_data)

        self._path_style = path_style

    ##############################################

    @property
    def path_style(self):
        return self._path_style

    # @path_style.setter
    # def path_style(self, value):
    #     self._path_style = value

####################################################################################################

class CircleItem(PositionMixin, StartStopAngleMixin, PathStyleItemMixin):

    ##############################################

    def __init__(self, scene, position, radius, path_style, user_data,
                 start_angle=0, # Fixme: kwargs ?
                 stop_angle=360,
    ):

        PathStyleItemMixin.__init__(self, scene, path_style, user_data)
        PositionMixin.__init__(self, position)
        StartStopAngleMixin.__init__(self, start_angle, stop_angle)

        # Fixme: radius = 1pt !!!
        if radius == '1pt':
            radius = 10

        self._radius = radius

    ##############################################

    @property
    def radius(self):
        return self._radius

    # @radius.setter
    # def radius(self, value):
    #     self._radius = value

    ##############################################

    def get_geometry(self):
        position = self.casted_position
        return Circle2D(position, self._radius) # Fixme: radius

####################################################################################################

class EllipseItem(PositionMixin, StartStopAngleMixin, PathStyleItemMixin):

    ##############################################

    def __init__(self, scene, position, x_radius, y_radius, path_style, user_data,
                 start_angle=0,
                 stop_angle=360,
    ):

        PathStyleItemMixin.__init__(self, scene, path_style, user_data)
        PositionMixin.__init__(self, position)
        StartStopAngleMixin.__init__(self, start_angle, stop_angle)

        self._x_radius = x_radius
        self._y_radius = y_radius

    ##############################################

    @property
    def x_radius(self):
        return self._x_radius

    # @x_radius.setter
    # def x_radius(self, value):
    #     self._x_radius = value

    @property
    def y_radius(self):
        return self._y_radius

    # @y_radius.setter
    # def y_radius(self, value):
    #     self._y_radius = value

    ##############################################

    def get_geometry(self):
        position = self.casted_position
        return Conic2D(position, self._x_radius, self._y_radius) # Fixme: radius, angle

####################################################################################################

class SegmentItem(TwoPositionMixin, PathStyleItemMixin):

    ##############################################

    def __init__(self, scene, position1, position2, path_style, user_data):

        PathStyleItemMixin.__init__(self, scene, path_style, user_data)
        TwoPositionMixin.__init__(self, position1, position2)

    ##############################################

    def get_geometry(self):
        positions = self.casted_positions
        return Segment2D(*positions)

####################################################################################################

class RectangleItem(TwoPositionMixin, PathStyleItemMixin):

    ##############################################

    def __init__(self, scene, position1, position2, path_style, user_data):

        # Fixme: position or W H
        PathStyleItemMixin.__init__(self, scene, path_style, user_data)
        TwoPositionMixin.__init__(self, position1, position2)

    ##############################################

    def get_geometry(self):
        positions = self.casted_positions
        return Rectangle2D(*positions)

####################################################################################################

class ImageItem(TwoPositionMixin, GraphicItem):

    ##############################################

    def __init__(self, scene, position1, position2, image, user_data):

        # Fixme: position or W H
        GraphicItem.__init__(self, scene, user_data)
        TwoPositionMixin.__init__(self, position1, position2)

        self._image = image

    ##############################################

    @property
    def image(self):
        return self._image

    # @image.setter
    # def image(self, value):
    #     self._image = value

    ##############################################

    def get_geometry(self):
        positions = self.casted_positions
        return Rectangle2D(*positions)

####################################################################################################

class CubicBezierItem(FourPositionMixin, PathStyleItemMixin):

    ##############################################

    def __init__(self, scene, position1, position2, position3, position4, path_style, user_data): # , curve

        # Fixme: curve vs path
        PathStyleItemMixin.__init__(self, scene, path_style, user_data)
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

    ##############################################

    def get_geometry(self):
        positions = self.casted_positions
        return CubicBezier2D(*positions)
