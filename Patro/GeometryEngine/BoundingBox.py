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

"""Module to compute bounding box and convex hull for a set of points.

"""

####################################################################################################

__all__ = [
    'bounding_box_from_points',
    'convex_hull',
]

####################################################################################################

import functools

####################################################################################################

def bounding_box_from_points(points):

    """Return the bounding box of the list of points."""

    bounding_box = None
    for point in points:
        if bounding_box is None:
            bounding_box = point.bounding_box
        else:
            bounding_box |= point.bounding_box
    return bounding_box

####################################################################################################

def _sort_point_for_graham_scan(points):

    def sort_by_y(p0, p1):
        return p0.x < p1.x if (p0.y == p1.y) else p0.y < p1.y

    # sort by ascending y
    sorted_points = sorted(points, key=functools.cmp_to_key(sort_by_y))

    # sort by ascending slope with p0
    p0 = sorted_points[0]
    x0 = p0.x
    y0 = p0.y
    def slope(p):
        # return (p - p0).tan
        return (p.y - y0) / (p.x - x0)
    def sort_by_slope(p0, p1):
        s0 = slope(p0)
        s1 = slope(p1)
        return p0.x < p1.x if (s0 == s1) else s0 < s1

    return sorted_points[0] + sorted(sorted_points[1:], key=cmp_to_key(sort_by_slope))

####################################################################################################

def _ccw(p1, p2, p3):
    """Three points are a counter-clockwise turn if ccw > 0, clockwise if ccw < 0, and collinear if ccw
     = 0 because ccw is a determinant that gives twice the signed area of the triangle formed by p1,
     p2 and p3.

    """
    return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)

####################################################################################################

def convex_hull(points):

    """Return the convex hull of the list of points using Graham Scan algorithm.

     References

     * https://en.wikipedia.org/wiki/Graham_scan

    """

   # convex_hull is a stack of points beginning with the leftmost point.
    convex_hull = []
    sorted_points = _sort_point_for_graham_scan(points)
    for p in sorted_points:
        # if we turn clockwise to reach this point,
        # pop the last point from the stack, else, append this point to it.
        while len(convex_hull) > 1 and _ccw(convex_hull[-1], convex_hull[-2], p) >= 0: # Fixme: check
            convex_hull.pop()
        convex_hull.append(p)

    # the stack is now a representation of the convex hull, return it.
    return convex_hull
