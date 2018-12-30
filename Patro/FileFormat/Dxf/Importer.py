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

import ezdxf

from Patro.GeometryEngine.Bezier import CubicSpline2D
from Patro.GeometryEngine.Conic import Circle2D, Conic2D, Interval
from Patro.GeometryEngine.Segment import Segment2D
from Patro.GeometryEngine.Vector import Vector2D

from .Polyline import Polyline

####################################################################################################

class DxfImporter:

    ##############################################

    def __init__(self, path):

        path = str(path)
        self._drawing = ezdxf.readfile(path)
        self._model_space = self._drawing.modelspace()
        self._items = []
        self._read()

    ##############################################

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, slice_):
        return self._items[slice_]

    ##############################################

    @staticmethod
    def _to_vector(point):
        return Vector2D(point[:2])

    @classmethod
    def _to_vectors(cls, points):
        return [cls._to_vector(x) for x in points]

    ##############################################

    def _add(self, item):
        self._items.append(item)

    ##############################################

    def _read(self):

        for item in self._model_space:
            dxf_type = item.dxftype()
            if dxf_type == 'LINE':
                self._on_line(item)
            elif dxf_type in ('CIRCLE', 'ARC'):
                self._on_circle(item, dxf_type == 'ARC')
            elif dxf_type == 'ELLIPSE':
                self._on_ellipse(item)
            elif dxf_type == 'LWPOLYLINE':
                self._on_polyline(item)
            elif dxf_type == 'SPLINE':
                self._on_spline(item)

    ##############################################

    def _on_line(self, item):
        segment = Segment2D(*self._to_vectors((item.dxf.start, item.dxf.end)))
        self._add(segment)

    ##############################################

    def _on_circle(self, item, is_arc):

        if is_arc:
            # Fixme:  start > stop, don't fit in Interval
            # domain = Interval(item.dxf.start_angle, item.dxf.end_angle)
            domain = None
        else:
            domain = None
        circle = Circle2D(self._to_vector(item.dxf.center), item.dxf.radius, domain=domain)
        self._add(circle)

    ##############################################

    def _on_ellipse(self, item):

        # domain = (item.dxf.start_param, item.dxf.end_param)
        domain = None
        major_axis = self._to_vector(item.dxf.major_axis)
        minor_axis = major_axis * item.dxf.ratio
        # Fixme:
        # ellipse = Conic2D(self._to_vector(item.dxf.center), major_axis, minor_axis, domain=domain)
        # self._add(ellipse)

    ##############################################

    def _on_polyline(self, item):

        polyline = Polyline(item.closed)
        for x, y, s, e, b in item.get_points():
            polyline.add(x, y, b)
        geometry = polyline.geometry()
        self._add(geometry)

    ##############################################

    def _on_spline(self, item):

        with item.edit_data() as data:
            points = self._to_vectors(data.control_points)
        # Fixme: item.closed
        spline = CubicSpline2D(points) # Fixme: cubic ???
        self._add(spline)
