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

"""Module to implement a graphic scene.

"""

####################################################################################################

__all__ = [
    'GraphicScene',
    # sphinx
    'GraphicSceneScope',
]

####################################################################################################

import logging

import rtree

from Patro.GeometryEngine import (
    Bezier,
    Conic,
    Line,
    Path,
    Polygon,
    Polyline,
    Rectangle,
    Segment,
    Spline,
    Triangle,
)
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
        # 'path': GraphicItem.PathItem, # see add_path...
        'polygon': GraphicItem.PolygonItem,
        'polyline': GraphicItem.PolylineItem,
        'quadratic_bezier': GraphicItem.QuadraticBezierItem,
        'rectangle': GraphicItem.RectangleItem,
        'segment': GraphicItem.SegmentItem,
        'text': GraphicItem.TextItem,
    }

    _logger = _module_logger.getChild('GraphicSceneScope')

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

    def __len__(self):
        return self.number_of_items

    @property
    def number_of_items(self):
        return len(self._items)

    def __iter__(self):
        # must be an ordered item list
        return iter(self._items.values())

    ##############################################

    @property
    def coordinates(self):
        return self._coordinates.values()

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
                # Fixme: distance is None
                if distance is not None and distance <= radius:
                    items.append((distance, item))
            except NotImplementedError:
                pass
        return sorted(items, key=lambda pair: pair[0])

    ##############################################

    # Fixme: !!!
    # def add_scope(self, *args, **kwargs):
    #     return self.add_item(GraphicSceneScope, self, *args, **kwargs)

    ##############################################

    def add_geometry(self, item, path_style):

        """Add a geometry primitive"""

        ctor = None
        points = None
        args = []
        args_tail = [path_style]
        kwargs = dict(user_data=item)

        unpack_points = True

        # Bezier
        if isinstance(item, Bezier.QuadraticBezier2D):
            ctor = self.quadratic_bezier

        elif isinstance(item, Bezier.CubicBezier2D):
            ctor = self.cubic_bezier

        # Conic
        elif isinstance(item, Conic.Circle2D):
            ctor = self.circle
            args = [item.radius]
            if item.domain:
                kwargs['start_angle'] = item.domain.start
                kwargs['stop_angle'] = item.domain.stop

        elif isinstance(item, Conic.Ellipse2D):
            ctor = self.ellipse
            args = [item.radius_x, item.radius_y, item.angle]

        # Line
        elif isinstance(item, Line.Line2D):
            # Fixme: extent ???
            raise NotImplementedError

        # Path
        elif isinstance(item, Path.Path2D):
            self.add_path(item, path_style, as_segments=True)

        # Polygon
        elif isinstance(item, Polygon.Polygon2D):
            ctor = self.polygon # or linear closed path
            unpack_points = False

        # Polyline
        elif isinstance(item, Polyline.Polyline2D):
            ctor = self.polyline # or linear path
            unpack_points = False

        # Rectangle
        elif isinstance(item, Rectangle.Rectangle2D):
            ctor = self.rectangle # or linear closed path

        # Segment
        elif isinstance(item, Segment.Segment2D):
            ctor = self.segment

        # Spline
        elif isinstance(item, Spline.BSpline2D):
            return self.add_spline(item, path_style)

        # Triangle
        elif isinstance(item, Triangle.Triangle2D):
            ctor = self.polygon # or linear path
            unpack_points = False

        # Not implemented
        else:
            self._logger.warning('Not implemented item {}'.format(item))
            raise NotImplementedError

        if ctor is not None:
            if points is None:
                points = list(item.points)
            if unpack_points:
                return ctor(*points, *args, *args_tail, **kwargs)
            else:
                return ctor(points, *args, *args_tail, **kwargs)

    ##############################################

    # def add_quadratic_bezier(self, curve, *args, **kwargs):
    #     # Fixme:
    #     cubic = curve.to_cubic()
    #     return self.cubic_bezier(*cubic.points, *args, **kwargs)

    ##############################################

    def add_spline(self, spline, path_style):
        return [
            self.cubic_bezier(*bezier.points, path_style, user_data=spline)
            for bezier in spline.to_bezier()
        ]

    ##############################################

    def add_path(self, path, path_style, user_data=None, as_segments=True):

        if as_segments:
            method = self.add_as_path_segments
        else:
            method = self.add_as_path

        return method(path, path_style, user_data)

    ##############################################

    def add_as_path(self, path, path_style, user_data=None):

        """Add a path as only one path item.

        .. warning: path can be filled.

        """

        item = self.add_item(GraphicItem.PathItem, path.p0, path_style, user_data)

        # cf. add_as_path_segments
        for segment in path:
            if isinstance(segment, Path.LinearSegment):
                # if segment.radius is not None:
                #     add_bulge(segment)
                item.line_to(segment.stop_point)
            elif isinstance(segment, Path.QuadraticBezierSegment):
                item.quadratic_to(segment.point1, segment.point2)
            elif isinstance(segment, Path.CubicBezierSegment):
                item.cubic_to(segment.point1, segment.point2, segment.point3)
            elif isinstance(segment, Path.ArcSegment):
                pass
            elif isinstance(segment, Path.StringedQuadtraticBezierSegment):
                pass
            elif isinstance(segment, Path.StringedCubicBezierSegment):
                pass

        if path.is_closed:
            item.close()

        return item

    ##############################################

    def add_as_path_segments(self, path, path_style, user_data=None):

        """Add a path as one item for each segments.

        .. warning: path cannot be filled.

        """

        if user_data is None:
            user_data = path

        items = []

        def add_bulge(segment):
            arc = segment.bulge_geometry
            arc_item = self.circle(
                arc.center, arc.radius,
                path_style,
                start_angle=arc.domain.start,
                stop_angle=arc.domain.stop,
                user_data=user_data, # segment
            )
            items.append(arc_item)

        def add_by_method(method, segment):
            item = method(
                *segment.points,
                path_style,
                user_data=user_data, # segment
            )
            items.append(item)

        def add_segment(segment):
            add_by_method(self.segment, segment)

        def add_ellipse(segment):
            # add_segment(Segment.Segment2D(*segment.points))
            ellipse = segment.geometry
            # print(ellipse, ellipse.domain)
            arc_item = self.ellipse(
                ellipse.center,
                ellipse.radius_x,
                ellipse.radius_y,
                ellipse.angle,
                path_style,
                start_angle=ellipse.domain.start,
                stop_angle=ellipse.domain.stop,
                user_data=user_data, # segment
            )
            items.append(arc_item)

        def add_quadratic(segment):
            add_by_method(self.quadratic_bezier, segment)

        def add_cubic(segment):
            add_by_method(self.cubic_bezier, segment)

        for segment in path:
            item = None
            if isinstance(segment, Path.LinearSegment):
                # if segment._start_radius is True:
                #     continue
                if segment.radius is not None:
                    add_bulge(segment)
                # if segment._closing is True:
                #     start_segment = path.start_segment
                #     add_bulge(start_segment)
                #     add_segment(start_segment)
                add_segment(segment)
            elif isinstance(segment, Path.QuadraticBezierSegment):
                add_quadratic(segment)
            elif isinstance(segment, Path.CubicBezierSegment):
                add_cubic(segment)
            elif isinstance(segment, Path.ArcSegment):
                add_ellipse(segment)
            elif isinstance(segment, Path.StringedQuadtraticBezierSegment):
                pass
            elif isinstance(segment, Path.StringedCubicBezierSegment):
                pass

    ##############################################

    # def quadratic_bezier(self, p0, p1, p2, *args, **kwargs):
    #     # Fixme:
    #     cubic = Bezier.QuadraticBezier2D(p0, p1, p2).to_cubic()
    #     return self.add_cubic(cubic, *args, **kwargs)

    ##############################################

    def bezier_path(self, points, degree, *args, **kwargs):

        """Add a Bézier curve with the given control points and degree"""

        if degree == 1:
            method = self.segment
        elif degree == 2:
            # Fixme:
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
