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

####################################################################################################

import unittest

from Patro.GeometryEngine.Polygon import *
from Patro.GeometryEngine.Segment import Segment2D
from Patro.GeometryEngine.Vector import Vector2D

####################################################################################################

class TestPolygon(unittest.TestCase):

    ##############################################

    # @unittest.skip
    def test_basic(self):

        x, y = 10, 20
        # points = Vector2D.from_coordinates()
        p0 = Vector2D( x,  y)
        p1 = Vector2D( x, -y)
        p2 = Vector2D(-x, -y)
        p3 = Vector2D(-x,  y)
        points = [p0, p1, p2, p3]

        # Ctor
        polygon = Polygon2D(*points)
        self.assertEqual(polygon.number_of_points, len(points))
        self.assertListEqual(list(polygon.points), points)

        # Clone
        clone = polygon.clone()
        self.assertEqual(polygon, clone)
        for i in range(polygon.number_of_points):
            self.assertEqual(polygon[i], clone[i]) # same value
            self.assertIsNot(polygon[i], clone[i]) # but cloned !

        self.assertTrue(polygon.is_closed)
        self.assertTrue(polygon.is_simple)
        self.assertTrue(polygon.is_convex)

        # Edges
        self.assertEqual(polygon.number_of_edges, len(points))
        for i in range(i):
            self.assertEqual(polygon.edges[i], Segment2D(points[i], points[(i+1)%len(points)]))
        self.assertEqual(polygon.edges[1], Segment2D(p1, p2))
        self.assertEqual(polygon.edges[2], Segment2D(p2, p3))
        self.assertEqual(polygon.edges[3], Segment2D(p3, p0))

        # Perimeter Area
        self.assertEqual(polygon.perimeter, 4*(x+y))
        self.assertEqual(polygon.area, 4*x*y)

        # Barycenter
        origin = Vector2D(0, 0)
        self.assertEqual(polygon.point_barycenter, origin)
        self.assertEqual(polygon.barycenter, origin)

        # Simplify
        self.assertIs(polygon.simplify(threshold=1.), polygon)

    ##############################################

    # @unittest.skip
    def test_convex_hull(self):

        # 6           *
        # 5     *
        # 4       +
        # 3   +     +   +   *
        # 2 *       +       *
        # 1       *       *
        # 0   *
        #   - 0 1 2 3 4 5 6 7

        # Points are clockwise oriented
        points = Vector2D.from_coordinates(
            (0, 0),  #  0 p0
            (-1, 2), #  1 *
            (0, 3),  #  2
            (2, 4),  #  3
            (1, 5),  #  4 *
            (4, 6),  #  5 *
            (3, 3),  #  6
            (5, 3),  #  7
            (7, 3),  #  8 *
            (7, 2),  #  9 *
            (6, 1),  # 10 *
            (3, 2),  # 11
            (2, 1),  # 12
        )

        convex_hull_points = [points[i] for i in (0, 10, 9, 8, 5, 4, 1)] # ccw

        polygon = Polygon2D(*points)
        convex_hull_truth = Polygon2D(*convex_hull_points)

        self.assertTrue(polygon.is_simple)
        self.assertFalse(polygon.is_convex)
        self.assertTrue(polygon.is_concave)
        self.assertTrue(polygon.is_clockwise)
        self.assertFalse(polygon.is_counterclockwise)

        convex_hull = polygon.convex_hull()
        self.assertListEqual(list(convex_hull.points), convex_hull_points)
        self.assertEqual(convex_hull, convex_hull_truth)
        self.assertFalse(convex_hull.is_clockwise)
        self.assertTrue(convex_hull.is_counterclockwise)

        reversed_polygon = Polygon2D(*reversed(points))
        self.assertFalse(reversed_polygon.is_clockwise)
        self.assertTrue(reversed_polygon.is_counterclockwise)
        convex_hull2 = reversed_polygon.convex_hull()
        self.assertEqual(convex_hull, convex_hull2)
        self.assertFalse(convex_hull2.is_clockwise)
        self.assertTrue(convex_hull2.is_counterclockwise)

        # Simplify
        simplified_polygon = convex_hull.simplify(threshold=.1)
        self.assertEqual(simplified_polygon, convex_hull_truth)

    ##############################################

    # @unittest.skip
    def test_simplification(self):

        # Points are clockwise oriented
        points = Vector2D.from_coordinates(
            (  0.1, 10.1), # 0
            ( -0.1, 10.9), # 1
            (  0.1, 20.1), # 2
            (  0  , 30  ), # 3 *
            ( 15.1, 30.1), # 4
            ( 30  , 30  ), # 5 *
            ( 29.9, 10.0), # 6
            ( 30  ,  0  ), # 7 *
            ( 15.1,  0.1), # 8
            (  0  ,  0  ), # 9 *
        )
        polygon = Polygon2D(*points)
        simplified_polygon = polygon.simplify(threshold=1.)
        simplified_polygon_truth = Polygon2D(*[points[i] for i in (3, 5, 7, 9)])
        self.assertEqual(simplified_polygon, simplified_polygon_truth)

        points = Vector2D.from_coordinates(
            (  0  ,  0  ),
            (  0.1, 10.1),
            (  0.2, 20.1),
        )
        polygon = Polygon2D(*points)
        simplified_polygon = polygon.simplify(threshold=1.)
        self.assertIsNone(simplified_polygon)

####################################################################################################

if __name__ == '__main__':
    unittest.main()
