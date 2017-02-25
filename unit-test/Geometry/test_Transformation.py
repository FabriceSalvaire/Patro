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

import numpy.testing as np_testing

####################################################################################################

from Valentina.Geometry.Transformation import *

####################################################################################################

class TestTransformation(unittest.TestCase):

    ##############################################

    def test(self):

        p0 = Vector2D(10, 0)
        rotation = Transformation2D.Rotation(90)
        p1 = rotation * p0
        p1_true = Vector2D(0, 10)
        self.assertTrue(p1.almost_equal(p1_true))

        rotation = AffineTransformation2D.Rotation(90)
        p1 = rotation * p0
        self.assertTrue(p1.almost_equal(p1_true))

        offset = Vector2D(10, 30)
        translation = AffineTransformation2D.Translation(offset)
        p1 = translation * p0
        p1_true = Vector2D(20, 30)
        self.assertTrue(p1.almost_equal(p1_true))

        p0 = Vector2D(20, 10)
        center = Vector2D(10, 10)
        rotation_at = AffineTransformation2D.RotationAt(center, 90)
        p1 = rotation_at * p0
        p1_true = Vector2D(10, 20)
        self.assertTrue(p1.almost_equal(p1_true))

        # np_testing.assert_almost_equal()

####################################################################################################

if __name__ == '__main__':

    unittest.main()
