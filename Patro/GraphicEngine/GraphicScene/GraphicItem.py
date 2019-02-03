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

"""Module to implement graphic scene items like text, image, line, circle and Bézier curve.

"""

# Fixme: get_geometry / as argument
#        position versus point

####################################################################################################

import logging

from Patro.GeometryEngine.Bezier import CubicBezier2D, QuadraticBezier2D
from Patro.GeometryEngine.Conic import Circle2D, Ellipse2D, AngularDomain
from Patro.GeometryEngine.Path import Path2D
from Patro.GeometryEngine.Polygon import Polygon2D
from Patro.GeometryEngine.Polyline import Polyline2D
from Patro.GeometryEngine.Rectangle import Rectangle2D
from Patro.GeometryEngine.Segment import Segment2D

from .GraphicItemMixin import (
    GraphicItem,
    PathStyleItemMixin,
    PositionMixin,
    TwoPositionMixin,
    ThreePositionMixin,
    FourPositionMixin,
    NPositionMixin,
    StartStopAngleMixin,
)

####################################################################################################

_module_logger = logging.getLogger(__name__)

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
                 radius_x, radius_y,
                 angle,
                 path_style, user_data,
                 start_angle=0,
                 stop_angle=360,
    ):

        PathStyleItemMixin.__init__(self, scene, path_style, user_data)
        PositionMixin.__init__(self, position)
        StartStopAngleMixin.__init__(self, start_angle, stop_angle)

        self._radius_x = radius_x
        self._radius_y = radius_y
        self._angle = angle

    ##############################################

    @property
    def radius_x(self):
        return self._radius_x

    # @radius_x.setter
    # def radius_x(self, value):
    #     self._radius_x = value

    @property
    def radius_y(self):
        return self._radius_y

    # @radius_y.setter
    # def radius_y(self, value):
    #     self._radius_y = value

    @property
    def angle(self):
        return self._angle

    ##############################################

    def get_geometry(self):
        position = self.casted_position
        return Ellipse2D(position, self._radius_x, self._radius_y, self._angle)

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

class PolygonItem(PolylineItem):

    ##############################################

    def get_geometry(self):
        positions = self.casted_positions
        return Polygon2D(*positions)

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

####################################################################################################

class QuadraticBezierItem(ThreePositionMixin, PathStyleItemMixin):

    ##############################################

    def __init__(self,
                 scene,
                 position1, position2, position3,
                 path_style,
                 user_data,
    ):

        # Fixme: curve vs path
        PathStyleItemMixin.__init__(self, scene, path_style, user_data)
        ThreePositionMixin.__init__(self, position1, position2, position3)

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
        return QuadraticBezier2D(*positions)

    ##############################################

    @property
    def cubic_positions(self):
        if not(hasattr(self, '_cubic_points')):
            cubic = self.geometry.to_cubic()
            self._cubic_points = list(cubic.points)
        return self._cubic_points

####################################################################################################

class PathItem(PositionMixin, PathStyleItemMixin):

    ##############################################

    def __init__(self, scene, position, path_style, user_data):

        PathStyleItemMixin.__init__(self, scene, path_style, user_data)
        PositionMixin.__init__(self, position)

        self._segments = []
        self._closed = False

    ##############################################

    def __len__(self):
        return len(self._segments)

    def __iter__(self):
        return iter(self._segments)

    def __getitem__(self, slice_):
        return self._segments[slice_]

    ##############################################

    @property
    def is_closed(self):
        return self._closed

    ##############################################

    def get_geometry(self):
        position = self.casted_position
        return Path2D(position) # Fixme: !!!

    ##############################################

    def _add_segment(self, segment):
        self._segments.append(segment)

    ##############################################

    def line_to(self, position):
        self._add_segment(LinearSegment(position))

    def quadratic_to(self, position1, position2):
        self._add_segment(QuadraticSegment(position1, position2))

    def cubic_to(self, position1, position2, position3):
        self._add_segment(CubicSegment(position1, position2, position3))

    # Fixme: which API ???
    #   QtPainterPath only support cubic
    def arc_to(self, position): # , ...
        # self._add_segment(ArcSegment(position))
        raise NotImplementedError

    def close(self):
        self._closed = True

####################################################################################################

class LinearSegment(PositionMixin):
    pass

class QuadraticSegment(TwoPositionMixin):
    pass

class CubicSegment(ThreePositionMixin):
    pass

class ArcSegment(PositionMixin):
    pass
