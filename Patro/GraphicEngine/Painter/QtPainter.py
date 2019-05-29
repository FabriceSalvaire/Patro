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

"""Module to implement a Qt Painter.

"""

####################################################################################################

import logging
import math

import numpy as np

from IntervalArithmetic import Interval2D

from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    QRectF, QSize, QSizeF, QPointF, Qt,
)
from QtShim.QtGui import QColor, QFont, QFontMetrics, QImage, QPainter, QPainterPath, QBrush, QPen
# from QtShim.QtQml import qmlRegisterType
from QtShim.QtQuick import QQuickPaintedItem

from .Painter import Painter
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.GraphicScene.GraphicItem import LinearSegment, QuadraticSegment, CubicSegment
from Patro.GraphicEngine.GraphicScene.Scene import GraphicScene
from Patro.GraphicStyle import StrokeStyle, CapStyle, JoinStyle

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QtScene(QObject, GraphicScene):

    """Class to add Qt Object features to GraphicScene ."""

    _logger = _module_logger.getChild('QtScene')

    ##############################################

    def __init__(self):
        QObject.__init__(self)
        GraphicScene.__init__(self)

####################################################################################################

class QtPainter(Painter):

    """Class to implement a Qt painter."""

    __STROKE_STYLE__ = {
        StrokeStyle.NoPen: Qt.NoPen,
        StrokeStyle.SolidLine: Qt.SolidLine,
        StrokeStyle.DashLine: Qt.DashLine,
        StrokeStyle.DotLine: Qt.DotLine,
        StrokeStyle.DashDotLine: Qt.DashDotLine,
        StrokeStyle.DashDotDotLine: Qt.DashDotDotLine,
    }

    __CAP_STYLE__ = {
        CapStyle.FlatCap: Qt.FlatCap,
        CapStyle.SquareCap: Qt.SquareCap,
        CapStyle.RoundCap: Qt.RoundCap,
    }

    __JOIN_STYLE__ = {
        JoinStyle.MiterJoin: Qt.MiterJoin,
        JoinStyle.BevelJoin: Qt.BevelJoin,
        JoinStyle.RoundJoin: Qt.RoundJoin,
        JoinStyle.SvgMiterJoin: Qt.SvgMiterJoin,
    }

    _logger = _module_logger.getChild('QtPainter')

    ##############################################

    def __init__(self, scene=None):

        super().__init__(scene)

        self._show_grid = True

        # self._paper = paper
        # self._translation = QPointF(0, 0)
        # self._scale = 1

    ##############################################

    # @property
    # def translation(self):
    #     return self._translation

    # @translation.setter
    # def translation(self, value):
    #     self._translation = value

    # @property
    # def scale(self):
    #     return self._scale

    # @scale.setter
    # def scale(self, value):
    #     print('set scale', value)
    #     self._scale = value

    ##############################################

    def to_svg(self, path, scale=10, dpi=100, title='', description=''):

        """Render the scene to SVG"""

        from QtShim.QtSvg import QSvgGenerator

        generator = QSvgGenerator()
        generator.setFileName(str(path))

        generator.setTitle(str(title))
        generator.setDescription(str(description))
        generator.setResolution(dpi)

        # Fixme: scale
        # Scale applied to (x,y) and radius but not line with
        self._scale = scale

        bounding_box = self._scene.bounding_box
        size = QSize(*[x*self._scale for x in bounding_box.size])
        view_box = QRectF(*[x*self._scale for x in bounding_box.rect])
        generator.setSize(size)
        generator.setViewBox(view_box)

        painter = QPainter()
        painter.begin(generator)
        self.paint(painter)
        painter.end()

        self._scale = None

    ##############################################

    def paint(self, painter):

        if bool(self):
            self._logger.info('Start painting')
            self._painter = painter
            if self._show_grid:
                self._paint_grid()
            super().paint()
            self._logger.info('Paint done')
        else:
            # Fixme: also protected in _paint_grid
            self._logger.warning('Scene is undefined')

    ##############################################

    def length_scene_to_viewport(self, length):
        return length * self._scale

    @property
    def scene_area(self):
        return None

    def scene_to_viewport(self, position):
        return QPointF(position.x * self._scale, position.y * self._scale)

        # Note: painter.scale apply to text as well

        # point = QPointF(position.x, position.y)
        # point += self._translation
        # point *= self._scale
        # point = QPointF(point.x(), -point.y())
        # return point

    ##############################################

    def cast_position(self, position):
        """Cast coordinate, apply scope transformation and convert scene to viewport, *position* can be a
        coordinate name string of a:class:`Vector2D`.

        """
        position = super().cast_position(position)
        return self.scene_to_viewport(position)

    ##############################################

    def _set_pen(self, item):

        path_syle = item.path_style
        # print('_set_pen', item, path_syle)
        if item.selected:
            color = QColor('red') # Fixme: style
        else:
            color = path_syle.stroke_color
            if color is not None:
                color = QColor(str(color))
                color.setAlphaF(path_syle.stroke_alpha)
            else:
                color = None
        line_style = self.__STROKE_STYLE__[path_syle.stroke_style]
        line_width = path_syle.line_width_as_float

        # Fixme: selection style
        if item.selected:
            line_width *= 4

        fill_color = path_syle.fill_color
        if fill_color is not None:
            color = QColor(str(fill_color))
            color.setAlphaF(path_syle.fill_alpha)
            self._painter.setBrush(color)
            # return None
        else:
            self._painter.setBrush(Qt.NoBrush)

        # print(item, color, line_style)
        if color is None or line_style is StrokeStyle.NoPen:
            # invisible item
            pen = QPen(Qt.NoPen)
            # print('Warning Pen:', item, item.user_data, color, line_style)
            return None
        else:
            pen = QPen(
                QBrush(color),
                line_width,
                line_style,
                self.__CAP_STYLE__[path_syle.cap_style],
                self.__JOIN_STYLE__[path_syle.join_style],
            )
            self._painter.setPen(pen)
            return pen

    ##############################################

    def _paint_grid(self):

        area = self.scene_area
        # Fixme:
        if area is None:
            return

        xinf, xsup = area.x.inf, area.x.sup
        yinf, ysup = area.y.inf, area.y.sup
        length = min(area.x.length, area.y.length)

        color = QColor('black')
        brush = QBrush(color)
        pen = QPen(brush, .75)
        self._painter.setPen(pen)
        self._painter.setBrush(Qt.NoBrush)

        step = max(10**int(math.log10(length)), 10)
        small_step = step // 10
        self._logger.info('Grid of {}/{} for {:.1f} mm'.format(step, small_step, length))
        self._paint_axis_grid(xinf, xsup, yinf, ysup, True, step)
        self._paint_axis_grid(yinf, ysup, xinf, xsup, False, step)

        color = QColor('black')
        brush = QBrush(color)
        pen = QPen(brush, .25)
        self._painter.setPen(pen)
        self._painter.setBrush(Qt.NoBrush)

        self._paint_axis_grid(xinf, xsup, yinf, ysup, True, small_step)
        self._paint_axis_grid(yinf, ysup, xinf, xsup, False, small_step)

    ##############################################

    def _paint_axis_grid(self, xinf, xsup, yinf, ysup, is_x, step):

        for i in range(int(xinf // step), int(xsup // step) +1):
            x = i*step
            if xinf <= x <= xsup:
                if is_x:
                    p0 = Vector2D(x, yinf)
                    p1 = Vector2D(x, ysup)
                else:
                    p0 = Vector2D(yinf, x)
                    p1 = Vector2D(ysup, x)
                p0 = self.cast_position(p0)
                p1 = self.cast_position(p1)
                self._painter.drawLine(p0, p1)

    ##############################################

    def paint_CoordinateItem(self, item):
        self._coordinates[item.name] = self.scene_to_viewport(item.position)

    ##############################################

    def _paint_arc(self, item, center, radius_x, radius_y):

        if item.is_closed:
            self._painter.drawEllipse(center, radius_x, radius_y)
        else:
            # drawArc cannot be filled !
            rectangle = QRectF(
                center + QPointF(-radius_x, radius_y),
                center + QPointF(radius_x, -radius_y),
            )
            start_angle, stop_angle = [int(angle*16) for angle in (item.start_angle, item.stop_angle)]
            span_angle = stop_angle - start_angle
            if span_angle < 0:
                span_angle = 5760 + span_angle
            self._painter.drawArc(rectangle, start_angle, span_angle)
            # self._painter.drawArc(center.x, center.y, radius, radius, start_angle, stop_angle)

    ##############################################

    def paint_CircleItem(self, item):

        center = self.cast_position(item.position)
        radius = self.length_scene_to_viewport(item.radius)

        pen = self._set_pen(item)

        self._paint_arc(item, center, radius, radius)

    ##############################################

    def paint_EllipseItem(self, item):

        center = self.cast_position(item.position)
        radius_x = self.length_scene_to_viewport(item.radius_x)
        radius_y = self.length_scene_to_viewport(item.radius_y)

        pen = self._set_pen(item)

        # Fixme: angle !!!
        self._paint_arc(item, center, radius_x, radius_y)

    ##############################################

    def _paint_cubic(self, item, vertices):

        pen = self._set_pen(item)
        path = QPainterPath()
        path.moveTo(vertices[0])
        path.cubicTo(*vertices[1:])
        self._painter.drawPath(path)

        path_style = item.path_style
        # if path_style.show_control:
        if getattr(path_style, 'show_control', False):
            color = QColor(str(path_style.control_color))
            brush = QBrush(color)
            pen = QPen(brush, 1) # Fixme
            self._painter.setPen(pen)
            self._painter.setBrush(Qt.NoBrush)
            path = QPainterPath()
            path.moveTo(vertices[0])
            for vertex in vertices[1:]:
                path.lineTo(vertex)
            self._painter.drawPath(path)

            # Fixme:
            radius = 3
            self._painter.setBrush(brush)
            for vertex in vertices:
                self._painter.drawEllipse(vertex, radius, radius)
            self._painter.setBrush(Qt.NoBrush) # Fixme:

    ##############################################

    def paint_QuadraticBezierItem(self, item):

        vertices = [self.cast_position(position) for position in item.cubic_positions]
        self._paint_cubic(item, vertices)

    ##############################################

    def paint_CubicBezierItem(self, item):

        vertices = self.cast_item_positions(item)
        self._paint_cubic(item, vertices)

    ##############################################

    def paint_ImageItem(self, item):

        vertices = self.cast_item_positions(item)
        rec = QRectF(vertices[0], vertices[1])

        image = item.image
        height, width, bytes_per_line = image.shape
        bytes_per_line *= width
        qimage = QImage(image, width, height, bytes_per_line, QImage.Format_RGB888)

        self._painter.drawImage(rec, qimage)

    ##############################################

    def paint_SegmentItem(self, item):

        self._set_pen(item)
        vertices = self.cast_item_positions(item)
        self._painter.drawLine(*vertices)

    ##############################################

    def paint_PolylineItem(self, item):

        self._set_pen(item)
        vertices = self.cast_item_positions(item)
        path = QPainterPath()
        path.moveTo(vertices[0])
        for vertex in vertices[1:]:
            path.lineTo(vertex)
        self._painter.drawPath(path)

    ##############################################

    def paint_PolygonItem(self, item):

        self._set_pen(item)
        vertices = self.cast_item_positions(item)
        # Fixme: fill ???
        self._painter.drawPolygon(*vertices) # API is like this

    ##############################################

    def paint_PathItem(self, item):

        self._set_pen(item)
        position = self.cast_position(item.position)
        path = QPainterPath()
        path.moveTo(position)
        for segment in item:
            if isinstance(segment, LinearSegment):
                # Fixme: can merge
                position = self.cast_position(segment.position)
                path.lineTo(position)
            else:
                if isinstance(segment, QuadraticSegment):
                    method = path.quadraticTo
                elif isinstance(segment, CubicSegment):
                    method = path.cubicTo
                else:
                    raise NotImplementedError
                positions = self.cast_position(segment.positions)
                method(*positions)

        # if item.it_closed:
        #     path.closeSubpath()

        self._painter.drawPath(path)

    ##############################################

    def paint_TextItem(self, item):

        position = self.cast_position(item.position)

        font = item.font
        qfont = QFont(font.family, font.point_size) # weight, italic = False

        # Fixme: anchor position
        # font_metrics = QFontMetrics(qfont)
        # height = font_metrics.height()
        # width = font_metrics.width(item.text)

        self._painter.setFont(qfont)
        self._painter.drawText(position, item.text)

####################################################################################################

class ViewportArea:

    """Class to implement a viewport."""

    _logger = _module_logger.getChild('ViewportArea')

    ##############################################

    def __init__(self):

        self._scene = None

        # self._width = None
        # self._height = None
        self._viewport_size = None

        self._scale = 1
        self._center = None
        self._area = None

    ##############################################

    def __bool__(self):
        return self._scene is not None

    ##############################################

    @classmethod
    def _to_np_array(cls, *args):
        if len(args) == 1:
            args = args[0]
        return np.array(args, dtype=np.float)

    ##############################################

    @classmethod
    def _point_to_np(cls, point):
        return cls._to_np_array(point.x(), point.y())

    ##############################################

    @property
    def viewport_size(self):
        return self._viewport_size
        # return (self._width, self._height)

    @viewport_size.setter
    def viewport_size(self, geometry):
        # self._width = geometry.width()
        # self._height = geometry.height()
        self._viewport_size = self._to_np_array(geometry.width(), geometry.height())
        if self:
            self._update_viewport_area()

    ##############################################

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, value):
        if not isinstance(value, GraphicScene):
            raise ValueError
        self._scene = value

    @property
    def scene_area(self):
        if self:
            return self._scene.bounding_box
        else:
            return None

    ##############################################

    # @property
    # def scale(self):
    #     return self._scale # px / mm

    @property
    def scale_px_by_mm(self):
        # Fixme: assume unit is mm
        return self._scale

    @property
    def scale_mm_by_px(self):
        return 1 / self._scale

    @property
    def center(self):
        return self._center

    # @property
    # def center_as_point(self):
    #     return QPointF(self._center[0], self._center[1])

    @property
    def area(self):
        return self._area

    ##############################################

    def _update_viewport_area(self):

        offset = self._viewport_size / 2 * self.scale_mm_by_px
        x, y = self._center
        dx, dy = offset

        self._area = Interval2D(
            (x - dx, x + dx),
            (y - dy, y + dy),
        )
        # Fixme: QPointF ???
        self._translation = - QPointF(self._area.x.inf, self._area.y.sup)

        # self._logger.debug('_update_viewport_area', self._center, self.scale_mm_by_px, self._area)

    ##############################################

    def _compute_scale_to_fit_scene(self, margin=None):

        # width_scale = self._width / scene_area.x.length
        # height_scale = self._height / scene_area.y.length
        # scale = min(width_scale, height_scale)

        # scale [px/mm]
        # Add 2% to scene for margin
        margin_scale = 1 + 2 / 100
        axis_scale = self._viewport_size / (self._to_np_array(self.scene_area.size) * margin_scale)
        axis = axis_scale.argmin()
        scale = axis_scale[axis]

        return scale, axis

    ##############################################

    def zoom_at(self, center, scale):
        self._center = center
        self._scale = scale
        self._update_viewport_area()

    ##############################################

    def fit_scene(self):

        # Fixme: AttributeError: 'NoneType' object has no attribute 'center'
        if self:
            center = self._to_np_array(self.scene_area.center)
            scale, axis = self._compute_scale_to_fit_scene()
            self.zoom_at(center, scale)

    ##############################################

    def scene_to_viewport(self, position):

        point = QPointF(position.x, position.y)
        point += self._translation
        point *= self._scale
        point = QPointF(point.x(), -point.y())
        return point

    ##############################################

    def viewport_to_scene(self, position):

        point = QPointF(position.x(), -position.y())
        point /= self._scale
        point -= self._translation
        return self._point_to_np(point)

    ##############################################

    def length_scene_to_viewport(self, length):
        return length * self._scale

    ##############################################

    def length_viewport_to_scene(self, length):
        return length / self._scale

    ##############################################

    def pan_delta_to_scene(self, position):
        point = self._point_to_np(position)
        point *= self.scale_mm_by_px
        return point

####################################################################################################

class QtQuickPaintedSceneItem(QQuickPaintedItem, QtPainter):

    """Class to implement a painter as Qt Quick item"""

    _logger = _module_logger.getChild('QtQuickPaintedSceneItem')

    ##############################################

    def __init__(self, parent=None):

        QQuickPaintedItem.__init__(self, parent)
        QtPainter.__init__(self)

        # Setup backend rendering
        self.setAntialiasing(True)
        # self.setRenderTarget(QQuickPaintedItem.Image) # high quality antialiasing
        self.setRenderTarget(QQuickPaintedItem.FramebufferObject) # use OpenGL

        self._viewport_area = ViewportArea()

    ##############################################

    def geometryChanged(self, new_geometry, old_geometry):

        # self._logger.info('geometryChanged', new_geometry, old_geometry)
        self._viewport_area.viewport_size = new_geometry
        # if self._scene:
        #     self._update_transformation()
        QQuickPaintedItem.geometryChanged(self, new_geometry, old_geometry)

    ##############################################

    # def _update_transformation(self):
    #     area = self._viewport_area.area
    #     self.translation = - QPointF(area.x.inf, area.y.sup)
    #     self.scale = self._viewport_area.scale_px_by_mm # QtPainter

    ##############################################

    @property
    def scene_area(self):
        return self._viewport_area.area

    ##############################################

    def scene_to_viewport(self, position):
        return self._viewport_area.scene_to_viewport(position)

    ##############################################

    def length_scene_to_viewport(self, length):
        return self._viewport_area.length_scene_to_viewport(length)

    ##############################################

    def length_viewport_to_scene(self, length):
        return self._viewport_area.length_viewport_to_scene(length)

    ##############################################

    sceneChanged = Signal()

    @Property(QtScene, notify=sceneChanged)
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        if self._scene is not scene:
            # self._logger.info('QtQuickPaintedSceneItem set scene', scene)
            self._logger.info('set scene') # Fixme: don't print ???
            self._scene = scene
            self._viewport_area.scene = scene
            self._viewport_area.fit_scene()
            # self._update_transformation()
            self.update()
            self.sceneChanged.emit()

    ##############################################

    # zoomChanged = Signal()

    # @Property(float, notify=zoomChanged)
    # def zoom(self):
    #     return self._zoom

    # @zoom.setter
    # def zoom(self, zoom):
    #     if self._zoom != zoom:
    #         print('QtQuickPaintedSceneItem zoom', zoom, self.width(), self.height())
    #         self._zoom = zoom
    #         self.set_transformation(zoom)
    #         self.update()
    #         self.zoomChanged.emit()

    ##############################################

    @Property(float)
    def zoom(self):
        return self._viewport_area.scale_px_by_mm

    ##############################################

    @Slot(QPointF, result=str)
    def format_coordinate(self, position):
        if bool(self._scene):
            scene_position = self._viewport_area.viewport_to_scene(position)
            return '{:.3f}, {:.3f}'.format(scene_position[0], scene_position[1])
        else:
            return ''

    ##############################################

    @Slot(float)
    def zoom_at_center(self, zoom):
        if bool(self._scene):
            self._viewport_area.zoom_at(self._viewport_area.center, zoom)
            self.update()

    ##############################################

    @Slot(QPointF, float)
    def zoom_at(self, position, zoom):
        # print('zoom_at', position, zoom)
        if bool(self._scene):
            scene_position = self._viewport_area.viewport_to_scene(position)
            self._viewport_area.zoom_at(scene_position, zoom)
            self.update()

    ##############################################

    @Slot()
    def fit_scene(self):
        if bool(self._scene):
            self._viewport_area.fit_scene()
            self.update()

    ##############################################

    @Slot(QPointF)
    def pan(self, dxy):
        if bool(self._scene):
            position = self._viewport_area.center + self._viewport_area.pan_delta_to_scene(dxy)
            self._viewport_area.zoom_at(position, self._viewport_area.scale_px_by_mm)
            self.update()

    ##############################################

    @Slot(QPointF)
    def item_at(self, position, radius_px=10):

        if not bool(self._scene):
            return

        self._scene.update_rtree()
        self._scene.unselect_items()
        scene_position = Vector2D(self._viewport_area.viewport_to_scene(position))
        radius = self.length_viewport_to_scene(radius_px)
        self._logger.info('Item selection at {} with radius {:1f} mm'.format(scene_position, radius))
        items = self._scene.item_at(scene_position, radius)
        if items:
            distance, nearest_item = items[0]
            # print('nearest item at {} #{:6.2f} {} {}'.format(scene_position, len(items), distance, nearest_item.user_data))
            nearest_item.selected = True
            # Fixme: z_value ???
            for pair in items[1:]:
                distance, item = pair
                # print('  {:6.2f} {}'.format(distance, item.user_data))
        self.update()

####################################################################################################

# qmlRegisterType(QtQuickPaintedSceneItem, 'Patro', 1, 0, 'PaintedSceneItem')
