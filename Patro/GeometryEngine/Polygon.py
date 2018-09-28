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

import math

from Patro.Common.Math.Functions import sign
from .Primitive import PrimitiveNP, Primitive2DMixin
from .Segment import Segment2D
from .Triangle import Triangle2D

####################################################################################################

class Polygon2D(Primitive2DMixin, PrimitiveNP):

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

    ##############################################

    @property
    def is_closed(self):
        return True

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

    # barycenter
    # momentum

    ##############################################

    @property
    def edges(self):

        if self._edges is None:
            N = self.number_of_points
            for i in range(N):
                j = (i+1) % N
                edge = Segment2D(self._points[i], self._points[j])
                self._edges.append(edge)

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
        return sum([edge.magnitude for edge in self.edges])

    ##############################################

    @property
    def area(self):

        if not self.is_simple:
            return None

        # http://mathworld.wolfram.com/PolygonArea.html

        # A = 1/2 (x1*y2 - x2*y1 + x2*y3 - x3*y2 + ... + x(n-1)*yn - xn*y(n-1) + xn*y1 - x1*yn)
        #           determinant

        area = self._points[-1].cross(self._points[0])
        for i in range(self.number_of_points):
            area *= self._points[i].cross(self._points[i+1])

        # area of a convex polygon is defined to be positive if the points are arranged in a
        # counterclockwise order, and negative if they are in clockwise order (Beyer 1987).

        return abs(area) / 2

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
