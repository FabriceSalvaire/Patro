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

"""Module to implement a graphic scene.

"""

####################################################################################################


__class__ = ['GraphicScene']

####################################################################################################

import logging

import rtree

from Patro.GeometryEngine.Transformation import AffineTransformation2D
from Patro.GeometryEngine.Vector import Vector2D
from . import GraphicItem
from .GraphicItem import CoordinateItem

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GraphicSceneScope:

    """Class to implement a graphic scene."""

    __ITEM_CTOR__ = {
        'circle': GraphicItem.CircleItem,
        'cubic_bezier': GraphicItem.CubicBezierItem,
        'ellipse': GraphicItem.EllipseItem,
        'image': GraphicItem.ImageItem,
        # 'path': GraphicItem.PathItem,
        # 'polygon': GraphicItem.PolygonItem,
        'rectangle': GraphicItem.RectangleItem,
        'segment': GraphicItem.SegmentItem,
        'polyline': GraphicItem.PolylineItem,
        'text': GraphicItem.TextItem,
    }

    ##############################################

    def __init__(self, transformation=None):

        if transformation is None:
            transformation = AffineTransformation2D.Identity()
        self._transformation = transformation

        self._coordinates = {}
        self._items = {} # id(item) -> item, e.g. for rtree query

        self._user_data_map = {}

        self._rtree = rtree.index.Index()
        # item_id -> bounding_box, used to delete item in rtree (cf. rtree api)
        self._item_bounding_box_cache = {}

    ##############################################

    @property
    def transformation(self):
        return self._transformation

    ##############################################

    def __iter__(self):
        # must be an ordered item list
        return iter(self._items.values())

    ##############################################

    def z_value_iter(self):

        # Fixme: cache ???
        # Group by z_value and keep inserting order
        z_map = {}
        for item in self._items.values():
            if item.visible:
                items = z_map.setdefault(item.z_value, [])
                items.append(item)

        for z_value in sorted(z_map.keys()):
            for item in z_map[z_value]:
                yield item

    ##############################################

    @property
    def selected_items(self):
        # Fixme: cache ?
        return [item for item in self._items.values() if item.selected]

    ##############################################

    def unselect_items(self):
        for item in self.selected_items:
            item.selected = False

    ##############################################

    def add_coordinate(self, name, position):

        item = CoordinateItem(name, position)
        self._coordinates[name] = item
        return item

    ##############################################

    def remove_coordinate(self, name):
        del self._coordinates[name]

    ##############################################

    def coordinate(self, name):
        return self._coordinates[name]

    ##############################################

    def cast_position(self, position):

        """Cast coordinate and apply scope transformation, *position* can be a coordinate name string of a
        :class:`Patro.GeometryEngine.Vector.Vector2D`.

        """

        # Fixme: cache ?
        if isinstance(position, str):
            vector = self._coordinates[position].position
        elif isinstance(position, Vector2D):
            vector = position
        return self._transformation * vector

    ##############################################

    def add_item(self, cls, *args, **kwargs):

        item = cls(self, *args, **kwargs)
        # print(item, item.user_data, hash(item))
        # if item in self._items:
        #     print('Warning duplicate', item.user_data)

        item_id = id(item) # Fixme: hash ???
        self._items[item_id] = item

        user_data = item.user_data
        if user_data is not None:
            user_data_id = id(user_data) # Fixme: hash ???
            items = self._user_data_map.setdefault(user_data_id, [])
            items.append(item)

        return item

    ##############################################

    def remove_item(self, item):

        self.update_rtree(item, insert=False)

        items = self.item_for_user_data(item.user_data)
        if items:
            items.remove(item)

        del self._items[item]

    ##############################################

    def item_for_user_data(self, user_data):
        user_data_id = id(user_data)
        return self._user_data_map.get(user_data_id, None)

    ##############################################

    def update_rtree(self):
        for item in self._items.values():
            if item.dirty:
                self.update_rtree_item(item)

    ##############################################

    def update_rtree_item(self, item, insert=True):

        item_id = id(item)
        old_bounding_box = self._item_bounding_box_cache.pop(item_id, None)
        if old_bounding_box is not None:
            self._rtree.delete(item_id, old_bounding_box)
        if insert:
            # try:
            bounding_box = item.bounding_box.bounding_box # Fixme: name
            # print(item, bounding_box)
            self._rtree.insert(item_id, bounding_box)
            self._item_bounding_box_cache[item_id] = bounding_box
            # except AttributeError:
            #     print('bounding_box not implemented for', item)
            #     pass # Fixme:

    ##############################################

    def item_in_bounding_box(self, bounding_box):

        # Fixme: Interval2D ok ?
        # print('item_in_bounding_box', bounding_box)
        item_ids = self._rtree.intersection(bounding_box)
        if item_ids:
            return [self._items[item_id] for item_id in item_ids]
        else:
            return None

    ##############################################

    def item_at(self, position, radius):

        x, y = list(position)
        bounding_box = (
            x - radius, y - radius,
            x + radius, y + radius,
        )
        items = []
        for item in self.item_in_bounding_box(bounding_box):
            try: # Fixme
                distance = item.distance_to_point(position)
                # print('distance_to_point {:6.2f} {}'.format(distance, item))
                if distance <= radius:
                    items.append((distance, item))
            except NotImplementedError:
                pass
        return sorted(items, key=lambda pair: pair[0])

    ##############################################

    # Fixme: !!!
    # def add_scope(self, *args, **kwargs):
    #     return self.add_item(GraphicSceneScope, self, *args, **kwargs)

    ##############################################

    def bezier_path(self, points, degree, *args, **kwargs):

        if degree == 1:
            method = self.segment
        elif degree == 2:
            method = self.quadratic_bezier
        elif degree == 3:
            method = self.cubic_bezier
        else:
            raise ValueError('Unsupported degree for Bezier curve: {}'.format(degree))

        # Fixme: generic code

        number_of_points = len(points)
        n = number_of_points -1
        if n % degree:
            raise ValueError('Wrong number of points for Bezier {} curve: {}'.format(degree, number_of_points))

        items = []
        for i in range(number_of_points // degree):
            j = degree * i
            k = j + degree
            item = method(*points[j:k+1], *args, **kwargs)
            items.append(item)

        return items

    ##############################################

# Register a method in GraphicSceneScope class for each type of graphic item

def _make_add_item_wrapper(cls):
    def wrapper(self, *args, **kwargs):
        return self.add_item(cls, *args, **kwargs)
    return wrapper

for name, cls in GraphicSceneScope.__ITEM_CTOR__.items():
    setattr(GraphicSceneScope, name, _make_add_item_wrapper(cls))

####################################################################################################

class GraphicScene(GraphicSceneScope):
    """Class to implement a graphic scene."""
    pass
