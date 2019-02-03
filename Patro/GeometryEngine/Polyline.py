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

"""Module to implement polyline.

"""

####################################################################################################

__all__ = ['Polyline2D']

####################################################################################################

from .Path import Path2D
from .Primitive import PrimitiveNP, Primitive2DMixin
from .Segment import Segment2D

####################################################################################################

class Polyline2D(Primitive2DMixin, PrimitiveNP):

    """Class to implements 2D Polyline."""

    ##############################################

    def __init__(self, *points):

        if len(points) < 2:
            raise ValueError('Polyline require at least 2 vertexes')

        PrimitiveNP.__init__(self, points)
        self._edges = None

    ##############################################

    @property
    def edges(self):

        if self._edges is None:
            self._edges = [Segment2D(self._points[i], self._points[i+1])
                           for i in range(self.number_of_points -1)]

        return iter(self._edges)

    ##############################################

    @property
    def length(self):
        return sum([edge.magnitude for edge in self.edges])

    ##############################################

    def distance_to_point(self, point):

        distance = None
        for edge in self.edges:
            edge_distance = edge.distance_to_point(point)
            if distance is None or edge_distance < distance:
                distance = edge_distance
        return distance

    ##############################################

    def to_path(self):

        path = Path2D(self.start_point)
        for point in self.iter_from_second_point():
            path.line_to(point)

        return path
