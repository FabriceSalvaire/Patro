####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
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

from Valentina.Tools.IterTools import pairwise
from .Primitive import Primitive2D
from .Vector import Vector2D

####################################################################################################

class Line2D(Primitive2D):

    """ 2D Line """

    ##############################################

    @staticmethod
    def from_two_points(p0, p1):

        """ Construct a :class:`Line2D` from two points. """

        return Line2D(p0, p1 - p0)

    ##############################################

    def __init__(self, point, vector):

        """ Construct a :class:`Line2D` from a point and a vector. """

        self.p = point
        self.v = vector

    ##############################################

    def clone(self):

        return self.__class__(self.p, self.v)

    ##############################################

    def __str__(self):

        text = '''Line
  Point  %s
  Vector %s
    magnitude %g
'''

        return text % (str(self.p), str(self.v), self.v.magnitude())

    ##############################################

    def point_at_s(self, s):

        """ Return the Point corresponding to the curvilinear abscissa s """

        return self.p + (self.v * s)

    ##############################################

    def compute_distance_between_abscissae(self, s0, s1):

        """ Compute distance between two abscissae """

        return abs(s1 - s0) * self.v.magnitude()

    ##############################################

    def compute_distance(self, s_list):

        """ Compute distance between a set of abscissae """

        # Fixme: ?
        #   s_list_sorted = copy.deepcopy(s_list)
        #   s_list_sorted.sort()

        return [self.compute_distance_between_abscissae(s0, s1) for s0, s1 in pairwise(s_list)]

    ##############################################

    def get_y_from_x(self, x):

        """ Return y corresponding to x """

        return self.v.tan() * (x - self.p.x) + self.p.y

    ##############################################

    def get_x_from_y(self, y):

        """ Return x corresponding to y """

        return self.v.inverse_tan() * (y - self.p.y) + self.p.x

    ##############################################

    # Fixme: is_parallel_to

    def is_parallel(self, other):

        """ Self is parallel to other """

        return self.v.is_parallel(other.v)

    ##############################################

    def is_orthogonal(self, other):

        """ Self is orthogonal to other """

        return self.v.is_orthogonal(other.v)

    ##############################################

    def shifted_parallel_line(self, shift):

        """ Return the shifted parallel line """

        n = self.v.normal()
        n.normalise()
        point = self.p + n*shift

        return self.__class__(point, self.v)

    ##############################################

    def orthogonal_line_at_abscissa(self, s):

        """ Return the orthogonal line at abscissa s """

        point = self.point_at_s(s)
        vector = self.v.normal()

        return self.__class__(point, vector)

    ##############################################

    def intersection_abscissae(l1, l2):

        """ Return the intersection abscissae between l1 and l2 """

        # l1 = p1 + s1*v1
        # l2 = p2 + s2*v2
        # delta = p2 - p1 = s2*v2 - s1*v1
        # delta x v1 = s2*v2 x v1 = s2 *  - v1 x v2
        # delta x v2 = s1*v1 x v2 = s1 *  v1 x v2

        if l1.is_parallel(l2):
            return (None, None)
        else:
            denominator = 1. / l1.v.cross(l2.v)
            delta = l2.p - l1.p
            s1 = delta.cross(l2.v) * denominator
            s2 = delta.cross(l1.v) * -denominator
            return (s1, s2)

    ##############################################

    def intersection(self, other):

        """ Return the intersection Point between self and other """

        s0, s1 = self.intersection_abscissae(other)
        if s0 is None:
            return None
        else:
            return self.point_at_s(s0)

    ##############################################

    def projected_abscissa(self, point):

        """ Return the abscissa corresponding to the perpendicular projection of a point to the line
        """

        delta = point - self.p
        s = delta.projection_on(self.v)

        return s

    ##############################################

    def distance_to_line(self, point):

        """ Return the distance of a point to the line """

        delta = point - self.p
        d = delta.deviation_with(self.v)

        return d

    ##############################################

    def distance_and_abscissa_to_line(self, point):

        """ Return the distance of a point to the line """

        delta = point - self.p
        d = delta.deviation_with(self.v)
        s = delta.projection_on(self.v)

        return (d, s) # distance to line, abscissa

    ##############################################

    def get_x_y_from_bounding_box(self, interval):

        """ Return the bounding box build on the intersection of the input bounding box with the
        line
        """

        left, bottom, right, top = interval.bounding_box()
        vb = Vector2D(interval.size())
        if abs(self.v.tan()) > vb.tan():
            x_min, y_min = self.get_x_from_y(bottom), bottom
            x_max, y_max = self.get_x_from_y(top), top
        else:
            x_min, y_min = left, self.get_y_from_x(left)
            x_max, y_max = right, self.get_y_from_x(right)

        return Vector2D(x_min, y_min), Vector2D(x_max, y_max)
