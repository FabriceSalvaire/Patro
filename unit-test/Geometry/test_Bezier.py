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

from Valentina.Geometry.Bezier import *
from Valentina.Geometry.Vector import Vector2D

####################################################################################################

class TestQuadraticBezier(unittest.TestCase):

    ##############################################

    def test(self):

        p0 = Vector2D(0, 0)
        p1 = Vector2D(5, 5)
        p2 = Vector2D(10, 0)

        curve = QuadraticBezier2D(p0, p1, p2)
        self.assertAlmostEqual(curve.length, curve.interpolated_length(), 4)

        split = curve.split_at_t(.5)
        self.assertAlmostEqual(sum([curve.length for curve in split]), curve.length, 4)

####################################################################################################

class TestCubicBezier(unittest.TestCase):

    ##############################################

    def test(self):

        p0 = Vector2D(0, 0)
        p1 = Vector2D(3, 5)
        p2 = Vector2D(6, 5)
        p3 = Vector2D(10, 0)

        curve = CubicBezier2D(p0, p1, p2, p3)
        self.assertAlmostEqual(curve.q_length(), curve.interpolated_length(), 0)
        self.assertAlmostEqual(curve.length, curve.interpolated_length(), 3)

        split = curve.split_at_t(.5)
        self.assertAlmostEqual(sum([curve.length for curve in split]), curve.length, 4)

        # Self intersecting curve
        curve = CubicBezier2D(p0, p2, p1, p3)
        self.assertAlmostEqual(curve.q_length(), curve.interpolated_length(), 0)
        self.assertAlmostEqual(curve.length, curve.interpolated_length(), 3)

        split = curve.split_at_t(.5)
        self.assertAlmostEqual(sum([curve.length for curve in split]), curve.length, 4)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
