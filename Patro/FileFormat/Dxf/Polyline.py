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

from Patro.Common.Math.Functions import sign
from Patro.GeometryEngine.Conic import Circle2D, AngularDomain
from Patro.GeometryEngine.Segment import Segment2D
from Patro.GeometryEngine.Vector import Vector2D

####################################################################################################

import math

####################################################################################################

class PolylineVertex:

    # sagitta of a circular arc is the distance from the center of the arc to the center of its base.
    #
    # bulge = sagitta / half the length of the chord
    #   a bulge value of 1 defines a semicircle
    #
    # The sign of the bulge value defines the side of the bulge:
    #     positive value (> 0): bulge is right of line (count clockwise)
    #     negative value (< 0): bulge is left of line (clockwise)
    #     0 = no bulge
    # points = item.get_points(format='xyseb') # ???

    # r = (s**2 + l**2) / (2*s)
    # b = s / l
    #
    # s = b*l
    # r = ((b*l)**2 + l**2) / (2*b*l)
    #   = l/2 * (b + 1/b)
    #
    # r - s = l/2 * (b + 1/b) - b*l
    #       = l/2 * (1/b - b)

    ##############################################

    def __init__(self, polyline, index, point, bulge=0):

        self._polyline = polyline
        self._index = index
        self._point = point
        self._bulge = bulge

    ##############################################

    @property
    def point(self):
        return self._point

    @property
    def x(self):
        return self._point.x

    @property
    def y(self):
        return self._point.y

    @property
    def bulge(self):
        return self._bulge

    ##############################################

    @property
    def prev(self):
        if self._index == 0 and not self._polyline.closed:
                return None
        return self._polyline[self._index -1]

    ##############################################

    @property
    def next(self):
        if self._polyline.is_last_index(self._index):
            if self._polyline.closed:
                return self._polyline[0]
            else:
                return None
        return self._polyline[self._index +1]

    ##############################################

    def __str__(self):
        return '({0.x:5.2f} {0.y:5.2f} {0._bulge:5.2f})'.format(self)

    ##############################################

    @property
    def segment_vector(self):
        return self.next.point - self._point

    ##############################################

    @property
    def demi_chord(self):
        return self.segment_vector.magnitude / 2

    ##############################################

    @property
    def sagitta(self):
        return self.bulge * self.demi_chord

    ##############################################

    @property
    def bulge_radius(self):
        if self._bulge == 0:
            return 0
        else:
            return self.demi_chord/2 * (self._bulge + 1/self._bulge)

    ##############################################

    @property
    def sagitta_dual(self):
        if self._bulge == 0:
            return 0
        else:
            return self.demi_chord/2 * (1/self._bulge - self._bulge)

    ##############################################

    @property
    def angle(self):
        if self._bulge == 0:
            return 0
        else:
            return math.degrees(2 * math.atan(self.bulge_radius/self.demi_chord - self._bulge))

####################################################################################################

class Polyline:

    ##############################################

    def __init__(self, closed=False):
        self._vertices = []
        self._closed = closed

    ##############################################

    @property
    def closed(self):
        return self._closed

    ##############################################

    def __len__(self):
        return len(self._vertices)

    def __iter__(self):
        return iter(self._vertices)

    def __getitem__(self, index):
        return self._vertices[index]

    def is_last_index(self, index):
        return index == len(self) - 1

    ##############################################

    def add(self, *args, **kwargs):
        vertex = PolylineVertex(self, len(self), *args, **kwargs)
        self._vertices.append(vertex)

    ##############################################

    def __str__(self):
        return ' '.join(['{:5.2f}'.format(vertex) for vertex in self])

    ##############################################

    def iter_on_segment(self):
        for i in range(len(self._vertices) -1):
            yield self._vertices[i], self._vertices[i+1]
        if self._closed:
            yield self._vertices[-1], self._vertices[0]

    ##############################################

    def geometry(self):

        items = []
        for vertex1, vertex2 in self.iter_on_segment():
            segment = Segment2D(vertex1.point, vertex2.point)
            if vertex1.bulge:
                segment_center = segment.center
                direction = vertex1.segment_vector.normalise()
                normal = direction.normal
                # offset = vertex1.bulge_radius - vertex1.sagitta
                offset = vertex1.sagitta_dual
                center = segment_center + normal * sign(vertex1.bulge) * offset
                arc = Circle2D(center, vertex1.bulge_radius)
                start_angle, stop_angle = [arc.angle_for_point(vertex.point) for vertex in (vertex1, vertex2)]
                if start_angle < 0:
                    start_angle += 360
                if stop_angle < 0:
                    stop_angle += 360
                if vertex1.bulge < 0:
                    start_angle, stop_angle = stop_angle, start_angle
                # print('bulb', vertex1, vertex2, vertex1.bulge, start_angle, stop_angle)
                arc.domain = AngularDomain(start_angle, stop_angle)
                # arc = Circle2D(center, vertex1.bulge_radius, domain=AngularDomain(start_angle, stop_angle))
                items.append(arc)
            else:
                items.append(segment)
        return items
