####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2017 Salvaire Fabrice
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

import unittest

from math import sqrt

from Patro.GeometryEngine.Vector import *

####################################################################################################

class TestVector2D(unittest.TestCase):

    ##############################################

    def _check_vector(self, vector, x ,y):
        self.assertEqual(vector.x, x)
        self.assertEqual(vector.y, y)

    ##############################################

    def test_ctor(self):

        x, y = 10, 20

        v1 = Vector2D(x, y)
        self._check_vector(v1, x, y)
        v1 = Vector2D((x, y))
        self._check_vector(v1, x, y)
        v1 = Vector2D([x, y])
        self._check_vector(v1, x, y)

        self.assertEqual(v1, v1.clone())

        for angle in (20, 60, 100, 180):
            v1 = Vector2D.from_angle(angle)
            self.assertAlmostEqual(v1.orientation, angle)
            v1 = Vector2D.from_angle(-angle)
            self.assertAlmostEqual(v1.orientation, -angle)

    ##############################################

    def test_properties(self):

        x, y = 10, 20

        v1 = Vector2D(x, y)
        magnitude_square = x**2 + y**2
        self.assertEqual(v1.magnitude_square, magnitude_square)
        self.assertEqual(v1.magnitude, sqrt(magnitude_square))

        v1 = Vector2D(x, 0)
        self.assertEqual(v1.orientation, 0)
        v1 = Vector2D(-x, 0)
        self.assertEqual(v1.orientation, 180)
        v1 = Vector2D(0, x)
        self.assertEqual(v1.orientation, 90)
        v1 = Vector2D(0, -x)
        self.assertEqual(v1.orientation, -90)

        v1 = Vector2D(x, x)
        self.assertEqual(v1.orientation, 45)
        v1 = Vector2D(x, -x)
        self.assertEqual(v1.orientation, -45)
        v1 = Vector2D(-x, x)
        self.assertEqual(v1.orientation, 135)
        v1 = Vector2D(-x, -x)
        self.assertEqual(v1.orientation, -135)

    ##############################################

    def test_math_operations(self):

        a, b, c = 10, 20, 30

        # unary -
        v1 = Vector2D(a, b)
        self.assertEqual(-v1, Vector2D(-a, -b))

        # binary + +=
        v1 = Vector2D(a, b)
        v2 = Vector2D(b, c)
        self.assertEqual(v1 + v2, Vector2D(a+b, b+c))
        self.assertEqual(v1 - v2, Vector2D(a-b, b-c))

        v1 = Vector2D(a, b)
        v1 += Vector2D(b, c)
        self.assertEqual(v1, Vector2D(a+b, b+c))

        v1 = Vector2D(a, b)
        v1 -= Vector2D(b, c)
        self.assertEqual(v1, Vector2D(a-b, b-c))

        # scale *
        v1 = Vector2D(a, b)
        v2 = Vector2D(a*a, b*a)
        self.assertEqual(v1 * a, v2)
        self.assertEqual(a * v1, v2)

        v1 = Vector2D(a, b)
        v1 *= a
        self.assertEqual(v1, v2)

        v1 = Vector2D(a, b)
        v1 /= a
        self.assertEqual(v1, Vector2D(1, b/a))

    ##############################################

    def test_two_vector_operations(self):

        x = 10

        v1 = Vector2D(x, x)
        v2 = Vector2D(-x, x)
        self.assertTrue(v1.is_orthogonal(v2))
        self.assertTrue(v1.is_orthogonal(v1.rotate(90)))

        v1 = Vector2D(x, x)
        self.assertTrue(v1.is_parallel(v1 * -x))
        self.assertTrue(v1.is_parallel(v1.rotate(180)))

        angle1 = 10
        direction = Vector2D.from_angle(angle1)
        perpendicular_direction = direction.rotate(90)
        for angle2 in range(-160, 180, 10):
            v2 = Vector2D.from_angle(angle2)

            self.assertAlmostEqual(v2.orientation_with(direction), angle2-angle1)

            v2x = direction * v2.projection_on(direction)
            v2y = perpendicular_direction * v2.deviation_with(direction)
            v3 = v2x + v2y
            self.assertTrue(v2.almost_equal(v3))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
