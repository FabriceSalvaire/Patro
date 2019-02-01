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

"""Module to implement polygon.

For resources on polygon see :ref:`this section <polygon-geometry-ressources-page>`.

"""

####################################################################################################

__all__ = ['Polygon2D']

####################################################################################################

import math

import numpy as np

from .Primitive import PrimitiveNP, ClosedPrimitiveMixin, PathMixin, Primitive2DMixin
from .Segment import Segment2D
from .Triangle import Triangle2D
from Patro.Common.Math.Functions import sign

####################################################################################################

# Fixme: PrimitiveNP last ???

class Polygon2D(Primitive2DMixin, ClosedPrimitiveMixin, PathMixin, PrimitiveNP):

    """Class to implements 2D Polygon."""

    ##############################################

    # def __new__(cls, *points):

    #     # remove consecutive duplicates
    #     no_duplicate = []
    #     for point in points:
    #         if no_duplicate and point == no_duplicate[-1]:
    #             continue
    #         no_duplicate.append(point)
    #     if len(no_duplicate) > 1 and no_duplicate[-1] == no_duplicate[0]:
    #         no_duplicate.pop() # last point was same as first

    #     # remove collinear points
    #     i = -3
    #     while i < len(no_duplicate) - 3 and len(no_duplicate) > 2:
    #         a, b, c = no_duplicate[i], no_duplicate[i + 1], no_duplicate[i + 2]
    #         if Point.is_collinear(a, b, c):
    #             no_duplicate.pop(i + 1)
    #             if a == c:
    #                 no_duplicate.pop(i)
    #         else:
    #             i += 1

    #     if len(vertices) > 3:
    #         return GeometryEntity.__new__(cls, *vertices, **kwargs)
    #     elif len(vertices) == 3:
    #         return Triangle(*vertices, **kwargs)
    #     elif len(vertices) == 2:
    #         return Segment(*vertices, **kwargs)
    #     else:
    #         return Point(*vertices, **kwargs)

    ##############################################

    def __init__(self, *points):

        if len(points) < 3:
            raise ValueError('Polygon require at least 3 vertexes')

        PrimitiveNP.__init__(self, points)

        self._edges = None
        self._is_simple = None
        self._is_convex = None

        self._area = None
        # self._cross = None
        # self._barycenter = None

        # self._major_axis_angle = None
        self._major_axis = None
        # self._minor_axis = None
        # self._axis_ratio = None

    ##############################################

    @property
    def is_triangle(self):
        return self.number_of_points == 3

    def to_triangle(self):
        if self.is_triangle:
            return Triangle2D(*self.points)
        else:
            raise ValueError('Polygon is not a triangle')

    ##############################################

    @property
    def edges(self):

        if self._edges is None:
            edges = []
            N = self.number_of_points
            for i in range(N):
                j = (i+1) % N
                edge = Segment2D(self._points[i], self._points[j])
                edges.append(edge)
            self._edges = edges

        return iter(self._edges)

    ##############################################

    def _test_is_simple(self):

        edges = list(self.edges)
        # intersections = []
        # Test for edge intersection
        for edge1 in edges:
            for edge2 in edges:
                if edge1 != edge2:
                    # Fixme: recompute line for edge
                    intersection, intersect = edge1.intersection(edge2)
                    if intersect:
                        common_vertex = edge1.share_vertex_with(edge2)
                        if common_vertex is not None:
                            if common_vertex == intersection:
                                continue
                            else:
                                # degenerated case where a vertex lie on an edge
                                return False
                        else:
                            # two edge intersect
                            # intersections.append(intersection)
                            return False
        return True

    ##############################################

    def _test_is_convex(self):

        # https://en.wikipedia.org/wiki/Convex_polygon
        # http://mathworld.wolfram.com/ConvexPolygon.html

        if not self.is_simple:
            return False

        edges = list(self.edges)
        # a polygon is convex if all turns from one edge vector to the next have the same sense
        # sign = edges[-1].perp_dot(edges[0])
        sign0 = sign(edges[-1].cross(edges[0]))
        for i in range(len(edges)):
            if sign(edges[i].cross(edges[i+1])) != sign0:
                return False
        return True

    ##############################################

    @property
    def is_simple(self):
        """Test if the polygon is simple, i.e. if it doesn't self-intersect."""
        if self._is_simple is None:
            self._is_simple = self._test_is_simple()
        return self._is_simple

    ##############################################

    @property
    def is_convex(self):
        if self._is_convex is None:
            self._is_convex = self._test_is_convex()
        return self._is_convex

    @property
    def is_concave(self):
        return not self.is_convex

    ##############################################

    @property
    def perimeter(self):
        return sum([edge.length for edge in self.edges])

    ##############################################

    @property
    def point_barycenter(self):
        center = self.start_point
        for point in self.iter_from_second_point():
            center += point
        return center / self.number_of_points

    ##############################################

    def _compute_area_barycenter(self):

        """Compute polygon area and barycenter."""

        if not self.is_simple:
            return None

        # area = self._points[-1].cross(self._points[0])
        # for i in range(self.number_of_points):
        #     area *= self._points[i].cross(self._points[i+1])

        # P0, P1, Pn-1, P0
        points = self.closed_point_array

        # from 0 to n-1 : P0, ..., Pn-1
        xi  = points[0,:-1]
        yi  = points[1,:-1]
        # from 1 to n : P1, ..., Pn-1, P0
        xi1 = points[0,1:]
        yi1 = points[1,1:]

        # Fixme: np.cross ???
        cross = xi * yi1 - xi1 * yi
        self._cross = cross

        area = .5 * np.sum(cross)

        if area == 0:
            # print('Null area')
            self._area = 0
            self._barycenter = self.start_point
        else:
            factor = 1 / (6*area)
            x = factor * np.sum((xi + xi1) * cross)
            y = factor * np.sum((yi + yi1) * cross)

            # area of a convex polygon is defined to be positive if the points are arranged in a
            # counterclockwise order, and negative if they are in clockwise order (Beyer 1987).
            self._area = abs(area)
            self._barycenter = self.__vector_cls__(x, y)

    ##############################################

    def _compute_inertia_moment(self):

        """Compute inertia moment on vertices."""

        # self.recenter()

        # Fixme: duplicated code
        # P0, P1, Pn-1, P0
        points = self.closed_point_array

        # from 0 to n-1 : P0, ..., Pn-1
        xi  = points[0,:-1]
        yi  = points[1,:-1]
        # from 1 to n : P1, ..., Pn-1, P0
        xi1 = points[0,1:]
        yi1 = points[1,1:]

        # computation on vertices
        number_of_points = self.number_of_points
        Ix =    np.sum(yi**2) / number_of_points
        Iy =    np.sum(xi**2) / number_of_points
        Ixy = - np.sum(xi*yi) / number_of_points

        # cross = xi * yi1 - xi1 * yi
        # cross = self._cross
        # Ix  = 1/(12*self._area) * np.sum((yi**2 + yi*yi1 + yi1**2) * cross)
        # Iy  = 1/(12*self._area) * np.sum((xi**2 + xi*xi1 + xi1**2) * cross)
        # Ixy = 1/(24*self._area) * np.sum((xi*yi1 + 2*(xi*yi + xi1*yi1) + xi1*yi) * cross)
        # cx, cy = self._barycenter
        # Ix -= cy**2
        # Iy -= cx**2
        # Ixy -= cx*cy
        # Ix = -Ix
        # Iy = -Iy
        # print(Ix, Iy, Ixy)

        if Ixy == 0:
            if Iy >= Ix:
                self._major_axis_angle = 0

                lambda1 = Iy
                lambda2 = Ix

                vx  = 0
                v1y = 1
                v2y = 0
            else:
                self._major_axis_angle = 90

                lambda1 = Ix
                lambda2 = Iy

                vx  = 1
                v1y = 0
                v2y = 1
        else:
            Is = Iy + Ix
            Id = Ix - Iy

            sqrt0 = math.sqrt(Id*Id + 4*Ixy*Ixy)

            lambda1 = (Is + sqrt0) / 2
            lambda2 = (Is - sqrt0) / 2

            vx  = Ixy
            v1y = (Id + sqrt0) / 2
            v2y = (Id - sqrt0) / 2

            if lambda1 < lambda2:
                v1y, v2y = v2y, v1y
                lambda1, lambda2 = lambda2, lambda1

            self._major_axis_angle = - math.degrees(math.atan(v1y/vx))

        self._major_axis = 4 * math.sqrt(math.fabs(lambda1))
        self._minor_axis = 4 * math.sqrt(math.fabs(lambda2))

        if self._minor_axis != 0:
            self._axis_ratio = self._major_axis / self._minor_axis
        else:
            self._axis_ratio = 0

    ##############################################

    def _check_area(self):
        if self.is_simple and self._area is None:
            self._compute_area_barycenter()

    ##############################################

    @property
    def area(self):
        """Return polygon area."""
        self._check_area()
        return self._area

    ##############################################

    @property
    def barycenter(self):
        """Return polygon barycenter."""
        self._check_area()
        return self._barycenter

    ##############################################

    def recenter(self):
        """Recenter the polygon to the barycenter."""
        # if self._centred:
        #     return
        barycenter = self._barycenter
        for point in self._points:
            point -= barycenter
        # self._centred = True

    ##############################################

    def _check_moment(self):
        if self.is_simple and self._major_axis is None:
            self._compute_inertia_moment()

    ##############################################

    @property
    def major_axis_angle(self):
        self._check_moment()
        return self._major_axis_angle

    @property
    def major_axis(self):
        self._check_moment()
        return self._major_axis

    @property
    def minor_axis(self):
        self._check_moment()
        return self._minor_axis

    @property
    def axis_ratio(self):
        self._check_moment()
        return self._axis_ratio

    ##############################################

    def _crossing_number_test(self, point):

        """Crossing number test for a point in a polygon."""

        # Wm. Randolph Franklin, "PNPOLY  - Point Inclusion in Polygon Test" Web Page (2000)
        # https://www.ecse.rpi.edu/Homepages/wrf/research/geom/pnpoly.html

        crossing_number = 0
        x = point.x
        y = point.y

        for edge in self.edges:
            if ((edge.p0.y <= y < edge.p1.y) or # upward crossing
                (edge.p1.y <= y < edge.p0.y)):  # downward crossing
                xi = edge.p0.x + (y - edge.p0.y) / edge.vector.slope
                if x < xi:
                    crossing_number += 1

        # Fixme: even/odd func
        return (crossing_number & 1) == 1 # odd => in

    ##############################################

    def _winding_number_test(self, point):

        """Winding number test for a point in a polygon."""

        # more accurate than crossing number test
        # http://geomalgorithms.com/a03-_inclusion.html#wn_PnPoly()

        winding_number = 0
        y = point.y

        for edge in self.edges:
            if edge.p0.y <= y:
                if edge.p1.y > y: # upward crossing
                    if edge.is_left(point):
                        winding_number += 1
            else:
                if edge.p1.y <= y: #  downward crossing
                    if edge.is_right(point):
                        winding_number -= 1

        return winding_number > 0

    ##############################################

    def is_point_inside(self, point):

        # http://geomalgorithms.com/a03-_inclusion.html
        # http://paulbourke.net/geometry/polygonmesh/#insidepoly

        # Fixme: bounding box test

        return self._winding_number_test(point)
