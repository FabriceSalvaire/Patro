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

####################################################################################################

import logging

from IntervalArithmetic import Interval2D

from Patro.Common.Math.Functions import ceil_int
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.GraphicScene.GraphicItem import GraphicItem

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Tiler:

    _logger = _module_logger.getChild('Tiler')

    ##############################################

    def __init__(self, bounding_box, paper, margin=1):

        # print('Tiler', bounding_box)
        self._bounding_box = bounding_box.enlarge(margin)
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
                yield (interval, r, c)

####################################################################################################

class Painter:

    ##############################################

    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)

        # Register paint methods
        paint_method = {}
        for item_cls in GraphicItem.__subclasses__:
            name = 'paint_' + item_cls.__name__
            try:
                paint_method[item_cls] = getattr(cls, name)
            except AttributeError:
                pass
        cls.__paint_method__ = paint_method

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

        if self._scene is None:
            return

        # Fixme: GraphicItemScope
        for item in self._scene.z_value_iter():
            try:
                self.__paint_method__[item.__class__](self, item)
            except KeyError:
                raise NotImplementedError('{} is not implemented in painter'.format(item.__class__))

    ##############################################

    def cast_position(self, position):
        """Call :meth:`GraphicSceneScope.cast_position`, cast coordinate and apply scope transformation,
        *position* can be a coordinate name string of a:class:`Vector2D`.

        """
        return self._scene.cast_position(position)

    ##############################################

    def cast_item_positions(self, item):
        return [self.cast_position(position) for position in item.positions]

    ##############################################

    def cast_item_coordinates(self, item, flat=False):
        positions = self.cast_item_positions(item)
        if flat:
            coordinates = []
            for position in positions:
                coordinates += list(position)
            return coordinates
        else:
            return [list(position) for position in positions]

    ##############################################

    def paint_CircleItem(self, item):
        raise NotImplementedError

    # def paint_CoordinateItem(self, item):
    #     raise NotImplementedError

    def paint_CubicBezierItem(self, item):
        raise NotImplementedError

    def paint_EllipseItem(self, item):
        raise NotImplementedError

    def paint_ImageItem(self, item):
        raise NotImplementedError

    def paint_PathItem(self, item):
        raise NotImplementedError

    def paint_PolygonItem(self, item):
        raise NotImplementedError

    def paint_PolylineItem(self, item):
        raise NotImplementedError

    def paint_QuadraticBezierItem(self, item):
        raise NotImplementedError

    def paint_SegmentItem(self, item):
        raise NotImplementedError

    def paint_TextItem(self, item):
        raise NotImplementedError
