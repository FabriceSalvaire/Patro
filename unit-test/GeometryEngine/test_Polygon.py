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
from Patro.GeometryEngine.Vector import Vector2D

####################################################################################################

class TestPolygon(unittest.TestCase):

    ##############################################

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

        # Perimeter Area
        self.assertEqual(polygon.perimeter, 4*(x+y))
        self.assertEqual(polygon.area, 4*x*y)

        # Barycenter
        origin = Vector2D(0, 0)
        self.assertEqual(polygon.point_barycenter, origin)
        self.assertEqual(polygon.barycenter, origin)

    ##############################################

    def test_convex_hull(self):

        # 6           *
        # 5     *
        # 4       +
        # 3   +     +   +   *
        # 2 *       +       *
        # 1       *       *
        # 0   *
        #   - 0 1 2 3 4 5 6 7

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

        self.assertTrue(polygon.is_simple)
        self.assertFalse(polygon.is_convex)
        self.assertTrue(polygon.is_concave)

        convex_hull = polygon.convex_hull()
        self.assertListEqual(list(convex_hull.points), convex_hull_points)

        reversed_polygon = Polygon2D(*reversed(points))
        print(reversed_polygon)
        convex_hull2 = reversed_polygon.convex_hull()
        print(convex_hull2)
        self.assertEqual(convex_hull, convex_hull2)

####################################################################################################

if __name__ == '__main__':
    unittest.main()
