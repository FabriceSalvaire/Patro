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

import logging

# from Valentina.Geometry import Segment2D, CubicBezier2D

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Vertex:

    ##############################################

    def __init__(self, point):

        self._point = point

    ##############################################

    @property
    def point(self):
        return self._point

    # def geometry

####################################################################################################

class Edge:

    ##############################################

    def __init__(self, contour, location):

        self._contour = contour
        self._location = location

    ##############################################

    @property
    def start_point(self):
        return self._contour._vertexes[self._location]

    @property
    def end_point(self):
        return self._contour._vertexes[self._location +1]

    @property
    def previous(self):
        # (location = 0) - 1 = -1
        return self._contour._edges[self._location -1]

    @property
    def next(self):
        location = self._location +1
        if location == self._contour.number_of_edges:
            location = 0
        return self._contour._edges[location]

    ##############################################

    # def __eq__
    # def geometry

####################################################################################################

class SegmentEdge(Edge):
    pass

####################################################################################################

class CurvedEdge(Edge):

    ##############################################

    def __init__(self, contour, location, curve, reverse=False):

        Edge.__init__(self, contour, location)
        self._curve = curve
        self._reverse = reverse

####################################################################################################

#     def __init__(self, first_point, second_point):

#         # Fixme: mixin
#         self._first_point = first_point
#         self._second_point = second_point

#     ##############################################

#     @property
#     def first_point(self):
#         return self._first_point

#     @property
#     def second_point(self):
#         return self._second_point

####################################################################################################

class Contour:

    _logger = _module_logger.getChild('Contour')

    ##############################################

    def __init__(self):

        self._vertexes = []
        self._edges = []

    ##############################################

    @property
    def start_point(self):
        return self._vertexes[0]

    @property
    def end_point(self):
        return self._vertexes[-1]

    @property
    def number_of_edges(self):
        return len(self._edges)

    ##############################################

    def iter_on_vertexes(self):
        return iter(self._vertexes)

    def iter_on_edges(self):
        return iter(self._edges)

    ##############################################

    def add_segment_edge(self, point):

        vertex = Vertex(point)
        self._vertexes.append(vertex)
        self._edges.append(SegmentEdge(self, self.number_of_edges))

    ##############################################

    def add_curved_edge(self, curve, reverse=False):

        start_point = curve.start_point
        if start_point != self.end_point: # Fixme: implement
            raise ValueError()
        vertex = Vertex(curve.end_point)
        self._vertexes.append(vertex)
        self._edges.append(CurvedEdge(self, self.number_of_edges, curve, reverse))

    ##############################################

    # def add_edge(self, edge, reverse=False):

    #     if not isinstance(edge, (Segment2D, CubicBezier2D)):
    #         raise ValueError()

    #     if reverse:
    #         edge = edge.reverse()

    #     self._edges.append(edge)

    #     for point in edge.iter_on_points():
    #         self._vertexes.append(point)
