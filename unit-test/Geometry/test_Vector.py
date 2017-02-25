####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
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

####################################################################################################

from Valentina.Geometry.Vector import *

####################################################################################################

class TestVector2D(unittest.TestCase):

    ##############################################

    def test(self):

        v1 = Vector2D(10, 20)
        v1 = Vector2D((10, 20))
        v1 = Vector2D([10, 20])

        v1 = Vector2D(10, 20)
        self.assertEqual(v1.x, 10)
        self.assertEqual(v1.y, 20)

        self.assertEqual(v1, v1.copy())

        v1 = Vector2D(10, 20)
        v2 = Vector2D(20, 30)
        self.assertEqual(v1 + v2, Vector2D(30, 50))

        v1 = Vector2D(10, 20)
        v2 = Vector2D(20, 30)
        self.assertEqual(v1 - v2, Vector2D(-10, -10))

        v1 = Vector2D(10, 20)
        v1 += Vector2D(20, 30)
        self.assertEqual(v1, Vector2D(30, 50))

        v1 = Vector2D(10, 20)
        v1 -= Vector2D(20, 30)
        self.assertEqual(v1, Vector2D(-10, -10))

        v1 = Vector2D(10, 20)
        self.assertEqual(v1 * 10, Vector2D(100, 200))

        v1 = Vector2D(10, 20)
        v1 *= 10
        self.assertEqual(v1, Vector2D(100, 200))

        #?# v1 = Vector2D(10, 20)
        #?# v1 /= 10
        #?# self.assertEqual(v1, Vector2D(1, 2))

        v1 = Vector2D(10, 20)
        self.assertEqual(v1.magnitude_square(), 10**2 + 20**2)

        v1 = Vector2D(10, 20)
        self.assertEqual(v1.magnitude(), sqrt(10**2 + 20**2))

        v1 = Vector2D(10, 0)
        self.assertEqual(v1.orientation(), 0)
        v1 = Vector2D(-10, 0)
        v1.orientation()
        self.assertEqual(v1.orientation(), 180)
        v1 = Vector2D(0, 10)
        self.assertEqual(v1.orientation(), 90)
        v1 = Vector2D(0, -10)
        self.assertEqual(v1.orientation(), -90)

        v1 = Vector2D(10, 10)
        self.assertEqual(v1.orientation(), 45)
        v1 = Vector2D(10, -10)
        self.assertEqual(v1.orientation(), -45)
        v1 = Vector2D(-10, 10)
        self.assertEqual(v1.orientation(), 135)
        v1 = Vector2D(-10, -10)
        self.assertEqual(v1.orientation(), -135)

        v1 = Vector2D.from_angle(25)
        self.assertAlmostEqual(v1.orientation(), 25)
        v1 = Vector2D.from_angle(-25)
        self.assertAlmostEqual(v1.orientation(), -25)

        v1 = Vector2D.from_angle(60)
        self.assertAlmostEqual(v1.orientation(), 60)
        v1 = Vector2D.from_angle(-60)
        self.assertAlmostEqual(v1.orientation(), -60)

        v1 = Vector2D.from_angle(100)
        self.assertAlmostEqual(v1.orientation(), 100)
        v1 = Vector2D.from_angle(-100)
        self.assertAlmostEqual(v1.orientation(), -100)

        v1 = Vector2D.from_angle(160)
        self.assertAlmostEqual(v1.orientation(), 160)
        v1 = Vector2D.from_angle(-160)
        self.assertAlmostEqual(v1.orientation(), -160)

        v1 = Vector2D(10, 10)
        v2 = Vector2D(-10, 10)
        self.assertTrue(v1.is_orthogonal(v2))
        self.assertTrue(v1.is_orthogonal(v1.rotate_counter_clockwise_90()))

        v1 = Vector2D(10, 10)
        self.assertTrue(v1.is_parallel(v1 * -10))
        self.assertTrue(v1.is_parallel(v1.rotate_180()))

        angle1 = 10
        direction = Vector2D.from_angle(angle1)
        perpendicular_direction = direction.rotate_counter_clockwise_90()
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
