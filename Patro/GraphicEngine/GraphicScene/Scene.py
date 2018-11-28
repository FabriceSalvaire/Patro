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

# Item
# bounding box, rtree
# distance to point

# nearest item to point
# item in point, radius

# line path
# polygon rect

# item -> user data
# user data -> item

# remove item

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

    __ITEM_CTOR__ = {
        'circle': GraphicItem.CircleItem,
        'cubic_bezier': GraphicItem.CubicBezierItem,
        'ellipse': GraphicItem.EllipseItem,
        'image': GraphicItem.ImageItem,
        # 'path': GraphicItem.PathItem,
        # 'polygon': GraphicItem.PolygonItem,
        'rectangle': GraphicItem.RectangleItem,
        'segment': GraphicItem.SegmentItem,
        'text': GraphicItem.TextItem,
    }

    ##############################################

    def __init__(self, transformation=None):

        if transformation is None:
            transformation = AffineTransformation2D.Identity()
        self._transformation = transformation

        self._coordinates = {}
        self._items = {} # used to retrieve item from item_id, e.g. for rtree query
        self._rtree = rtree.index.Index()
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
        return item

    ##############################################

    def remove_item(self, item):
        self.update_rtree(item, insert=False)
        del self._items[item]

    ##############################################

    # Fixme: ???
    # def item(self, item):
    #     return self._items[item]

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

def make_add_item_wrapper(cls):
    def wrapper(self, *args, **kwargs):
        return self.add_item(cls, *args, **kwargs)
    return wrapper

for name, cls in GraphicSceneScope.__ITEM_CTOR__.items():
    setattr(GraphicSceneScope, name, make_add_item_wrapper(cls))

####################################################################################################

class GraphicScene(GraphicSceneScope):
    pass
