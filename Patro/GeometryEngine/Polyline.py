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
            for i in range(self.number_of_points -1):
                edge = Segment2D(self._points[i], self._points[i+1])
                self._edges.append(edge)

        return iter(self._edges)

    ##############################################

    @property
    def length(self):
        return sum([edge.magnitude for edge in self.edges])

    ##############################################

    def distance_to_point(self, point):

        distance = None
        for edge in edges:
            edge_distance = edge.distance_to_point(point)
            if distance is None or edge_distance < distance:
                distance = edge_distance
        return distance
