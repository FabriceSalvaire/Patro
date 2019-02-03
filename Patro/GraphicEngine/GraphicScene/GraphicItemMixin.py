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

"""Module to implement graphic scene items mixins.

"""

####################################################################################################

__all__ = [
    'GraphicItem',
    'PathStyleItemMixin',
    'PositionMixin',
    'TwoPositionMixin',
    'FourPositionMixin',
    'NPositionMixin',
    'StartStopAngleMixin',
]

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

class ThreePositionMixin(TwoPositionMixin):

    ##############################################

    def __init__(self, position1, position2, position3):
        TwoPositionMixin.__init__(self, position1, position2)
        self._position3 = position3

    ##############################################

    @property
    def position3(self):
        return self._position3

    @property
    def positions(self):
        return (self._position1, self._position2, self._position3)

####################################################################################################

class FourPositionMixin(ThreePositionMixin):

    ##############################################

    def __init__(self, position1, position2, position3, position4):
        ThreePositionMixin.__init__(self, position1, position2, position3)
        self._position4 = position4

    ##############################################

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
