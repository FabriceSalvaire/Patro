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

    def test(self):

        x, y = 10, 20
        p0 = Vector2D( x,  y)
        p1 = Vector2D( x, -y)
        p2 = Vector2D(-x, -y)
        p3 = Vector2D(-x,  y)
        points = [p0, p1, p2, p3]

        polygon = Polygon2D(*points)
        self.assertEqual(polygon.number_of_points, len(points))
        self.assertListEqual(list(polygon.points), points)

        self.assertEqual(polygon.perimeter, 4*(x+y))
        self.assertEqual(polygon.area, 4*x*y)

        origin = Vector2D(0, 0)
        self.assertEqual(polygon.point_barycenter, origin)
        self.assertEqual(polygon.barycenter, origin)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
