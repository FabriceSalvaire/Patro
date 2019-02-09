####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2017 Fabrice Salvaire
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

"""Module to compute bounding box for a set of points.

"""

####################################################################################################

__all__ = [
    'bounding_box_from_points',
]

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
