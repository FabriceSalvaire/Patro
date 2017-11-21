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

from IntervalArithmetic import Interval2D

from Valentina.Geometry.Vector import Vector2D
from Valentina.Math.Functions import ceil_int

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Tiler:

    _logger = _module_logger.getChild('Tiler')

    ##############################################

    def __init__(self, bounding_box, paper):

        self._bounding_box = bounding_box
        self._paper = paper

    ##############################################

    def __iter__(self):

        figure_margin = 2

        paper_size = Vector2D(self._paper.width, self._paper.height) / 10 # mm
        paper_margin = (self._paper.margin + figure_margin) / 10
        area_vector = paper_size - Vector2D(paper_margin, paper_margin) * 2

        number_of_columns = ceil_int(self._bounding_box.x.length / area_vector.x)
        number_of_rows = ceil_int(self._bounding_box.y.length / area_vector.y)

        self._logger.info('Bounding Box {}'.format(self._bounding_box))
        self._logger.info('Area {}'.format(area_vector))
        self._logger.info('Grid {}x{}'.format(number_of_rows, number_of_columns))

        min_point = Vector2D((self._bounding_box.x.inf, self._bounding_box.y.inf))

        for r in range(number_of_rows):
            for c in range(number_of_columns):
                local_min_point = min_point + area_vector * Vector2D(r, c)
                local_max_point = local_min_point + area_vector
                interval = Interval2D((local_min_point.x, local_max_point.x), (local_min_point.y, local_max_point.y))
                yield interval

####################################################################################################

class Painter:

    ##############################################

    def __init__(self, scene):

        self._scene = scene

    ##############################################

    @property
    def scene(self):
        return self._scene

    # @scene.setter
    # def scene(self, value):
    #     self._scene = value

    ##############################################

    def paint(self):

        for item in self._scene.root_scope:
            # Fixme: GraphicItemScope
            function = getattr(self, 'paint_' + item.__class__.__name__)
            function(item)

    ##############################################

    def paint_CoordinateItem(self, item):

        raise NotImplementedError

    ##############################################

    def paint_TextItem(self, item):

        raise NotImplementedError

    ##############################################

    def paint_CircleItem(self, item):

        raise NotImplementedError

    ##############################################

    def paint_SegmentItem(self, item):

        raise NotImplementedError

    ##############################################

    def paint_CubicBezierItem(self, item):

        raise NotImplementedError

