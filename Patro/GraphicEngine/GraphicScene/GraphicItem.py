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

"""Module to implement graphic scene items like text, image, line, circle and Bézier curve.

"""

# Fixme: get_geometry / as argument

####################################################################################################

import logging

from Patro.GeometryEngine.Bezier import CubicBezier2D
from Patro.GeometryEngine.Conic import Circle2D, Ellipse2D, AngularDomain
from Patro.GeometryEngine.Polyline import Polyline2D
from Patro.GeometryEngine.Rectangle import Rectangle2D
from Patro.GeometryEngine.Segment import Segment2D
from Patro.GraphicStyle import Colors, StrokeStyle

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GraphicPathStyle:

    ##############################################

    def __init__(self,
                 stroke_style=StrokeStyle.SolidLine,
                 line_width=1.0,
                 stroke_color=Colors.black,
                 fill_color=None, # only for closed path
    ):

        """*color* can be a defined color name, a '#rrggbb' string or a :class:`Color` instance.

        """

        self.stroke_style = stroke_style
        self.line_width = line_width
        self.stroke_color = stroke_color
        self.fill_color = fill_color

    ##############################################

    def clone(self):
        return self.__class__(
            self._stroke_style,
            self._line_width,
            self._stroke_color,
            self._fill_color,
        )

    ##############################################

    def __repr__(self):
        return 'GraphicPathStyle({0._stroke_style}, {0._line_width}, {0._stroke_color}, {0._fill_color})'.format(self)

    ##############################################

    @property
    def stroke_style(self):
        return self._stroke_style

    @stroke_style.setter
    def stroke_style(self, value):
        self._stroke_style = StrokeStyle(value)

    ##############################################

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        self._line_width = value # Fixme: float ???

    @property
    def line_width_as_float(self):
        line_width = self._line_width
        # Fixme: use scale ?
        if isinstance(line_width, float):
            return line_width
        else:
            line_width = line_width.replace('pt', '')
            line_width = line_width.replace('px', '')
            return float(line_width)

    ##############################################

    @property
    def stroke_color(self):
        return self._stroke_color

    @stroke_color.setter
    def stroke_color(self, value):
        self._stroke_color = Colors.ensure_color(value)

    ##############################################

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value):
        self._fill_color = Colors.ensure_color(value)

####################################################################################################

class GraphicBezierStyle(GraphicPathStyle):

    ##############################################

    def __init__(self,
                 # Fixme: duplicate
                 stroke_style=StrokeStyle.SolidLine,
                 line_width=1.0,
                 stroke_color=Colors.black,
                 fill_color=None, # only for closed path
                 #
                 show_control=False,
                 control_color=None,
    ):

        super().__init__(stroke_style, line_width, stroke_color, fill_color)
        self._show_control = show_control
        self._control_color = Colors.ensure_color(control_color)

    ##############################################

    def clone(self):
        return self.__class__(
            self.stroke_style,
            self.line_width,
            self.stroke_color,
            self.fill_color,
            self._show_control,
            self._control_color,
        )

    ##############################################

    @property
    def show_control(self):
        return self._show_control

    @show_control.setter
    def show_control(self, value):
        self._show_control = value

    ##############################################

    @property
    def control_color(self):
        return self._control_color

    @control_color.setter
    def control_color(self, value):
        self._control_color = value

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

class NPositionMixin:

    ##############################################

    def __init__(self, positions):
        self._positions = list(positions)

    ##############################################

    @property
    def positions(self): # Fixme: versus points
        return self._positions # Fixme: iter list ???

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

    ##############################################

    @property
    def is_closed(self):
        return abs(self._stop_angle - self.start_angle) >= 360

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

class Font:

    ##############################################

    def __init__(self, family, point_size):

        self.family = family
        self.point_size = point_size

####################################################################################################

class TextItem(PositionMixin, GraphicItem):

    ##############################################

    def __init__(self, scene, position, text, font, user_data):

        GraphicItem.__init__(self, scene, user_data)
        PositionMixin.__init__(self, position)

        self._text = str(text)
        self._font = font

    ##############################################

    @property
    def text(self):
        return self._text

    # @text.setter
    # def text(self, value):
    #     self._text = value

    @property
    def font(self):
        return self._font

    # @font.setter
    # def font(self, value):
    #     self._font = value

    ##############################################

    def get_geometry(self):
        position = self.casted_position
        # Fixme: require metric !
        # QFontMetrics(font).width(self._text)
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
        # Fixme: radius
        domain = AngularDomain(self._start_angle, self._stop_angle)
        return Circle2D(position, self._radius, domain=domain)

####################################################################################################

class EllipseItem(PositionMixin, StartStopAngleMixin, PathStyleItemMixin):

    ##############################################

    def __init__(self, scene, position,
                 x_radius, y_radius,
                 angle,
                 path_style, user_data,
                 start_angle=0,
                 stop_angle=360,
    ):

        PathStyleItemMixin.__init__(self, scene, path_style, user_data)
        PositionMixin.__init__(self, position)
        StartStopAngleMixin.__init__(self, start_angle, stop_angle)

        self._x_radius = x_radius
        self._y_radius = y_radius
        self._angle = angle

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

    @property
    def angle(self):
        return self._angle

    ##############################################

    def get_geometry(self):
        position = self.casted_position
        return Ellipse2D(position, self._x_radius, self._y_radius, self._angle)

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

class PolylineItem(NPositionMixin, PathStyleItemMixin):

    ##############################################

    def __init__(self, scene, positions, path_style, user_data):

        PathStyleItemMixin.__init__(self, scene, path_style, user_data)
        NPositionMixin.__init__(self, positions)

    ##############################################

    def get_geometry(self):
        positions = self.casted_positions
        return Polyline2D(*positions)

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

    def __init__(self,
                 scene,
                 position1, position2, position3, position4,
                 path_style,
                 user_data,
    ):

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
