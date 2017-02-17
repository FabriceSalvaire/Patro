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

####################################################################################################

from Valentina.Geometry.Line2D import *
from Valentina.Geometry.Vector2D import *

####################################################################################################

class TestLine2D(unittest.TestCase):

    ##############################################

    def test(self):

        p0 = Vector2D(10, 10)
        v0 = Vector2D.from_angle(10)
        l0 = Line2D(p0, v0)

        for x in -5, 0, 5:
            self.assertAlmostEqual(l0.get_x_from_y(l0.get_y_from_x(x)), x)
            self.assertAlmostEqual(l0.get_y_from_x(l0.get_x_from_y(x)), x)

        for offset in -20, 0, 20:
            l1 = l0.shifted_parallel_line(offset)
            self.assertAlmostEqual(l0.distance_to_line(l1.p), offset)

            l2 = l0.orthogonal_line_at_abscissa(0)
            p2 = l0.point_at_s(0)
            self.assertAlmostEqual(l1.projected_abscissa(p2), 0)
            self.assertAlmostEqual(l1.distance_to_line(p2), -offset)

            for s in -50, 50:
                l3 = l0.orthogonal_line_at_abscissa(s)
                p3 = l0.point_at_s(s)
                self.assertAlmostEqual(l1.projected_abscissa(p3), s)
                self.assertAlmostEqual(l1.distance_to_line(p3), -offset)

        # Orthocenter Triangle test

        p0 = Vector2D(10, 10)
        d0 = Vector2D.from_angle(10)
        l0 = Line2D(p0, d0)

        p1 = Vector2D(50, 50)
        d1 = Vector2D.from_angle(-40)
        l1 = Line2D(p1, d1)

        p2 = Vector2D(20, 60)
        d2 = Vector2D.from_angle(-20)
        l2 = Line2D(p2, d2)

        v0 = l0.intersection(l1)
        v1 = l1.intersection(l2)
        v2 = l2.intersection(l0)

        lp0 = Line2D(v2, d0.rotate_counter_clockwise_90())
        lp1 = Line2D(v0, d1.rotate_counter_clockwise_90())
        lp2 = Line2D(v1, d2.rotate_counter_clockwise_90())

        i0 = lp0.intersection(lp1)
        i1 = lp1.intersection(lp2)
        i2 = lp2.intersection(lp0)

        self.assertTrue(i0.almost_equal(i1))
        self.assertTrue(i1.almost_equal(i2))
        self.assertTrue(i2.almost_equal(i0))

        # Centroid Triangle test

        lm0 = Line2D.from_two_points(v0, Vector2D.middle(v1, v2))
        lm1 = Line2D.from_two_points(v1, Vector2D.middle(v0, v2))
        lm2 = Line2D.from_two_points(v2, Vector2D.middle(v0, v1))

        i0 = lm0.intersection(lm1)
        i1 = lm1.intersection(lm2)
        i2 = lm2.intersection(lm0)

        self.assertTrue(i0.almost_equal(i1))
        self.assertTrue(i1.almost_equal(i2))
        self.assertTrue(i2.almost_equal(i0))

        # l0.get_x_y_from_bounding_box()

####################################################################################################

if __name__ == '__main__':

    unittest.main()
