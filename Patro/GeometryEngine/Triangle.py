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

####################################################################################################

def triangle_orientation(p0, p1, p2):

    """Return the triangle orientation defined by the three points."""

    dx1 = p1.x - p0.x
    dy1 = p1.y - p0.y
    dx2 = p2.x - p0.x
    dy2 = p2.y - p0.y

    # second slope is greater than the first one --> counter-clockwise
    if dx1 * dy2 > dx2 * dy1:
        return 1
    # first slope is greater than the second one --> clockwise
    elif dx1 * dy2 < dx2 * dy1:
        return -1
    # both slopes are equal --> collinear line segments
    else:
        # p0 is between p1 and p2
        if dx1 * dx2 < 0 or dy1 * dy2 < 0:
            return -1
        # p2 is between p0 and p1, as the length is compared
        # square roots are avoided to increase performance
        elif dx1 * dx1 + dy1 * dy1 >= dx2 * dx2 + dy2 * dy2:
            return 0
        # p1 is between p0 and p2
        else:
            return 1
