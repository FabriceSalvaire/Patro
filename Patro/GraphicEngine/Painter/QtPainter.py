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

import logging

from PyQt5.QtCore import (
    pyqtProperty, pyqtSignal, QObject,
    QRectF, QSizeF, QPointF, Qt,
)
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen
# from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtQuick import QQuickPaintedItem

from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.GraphicScene.Scene import GraphicScene
from .Painter import Painter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QtScene(QObject, GraphicScene):

    _logger = _module_logger.getChild('QtScene')

    ##############################################

    def __init__(self):

        QObject.__init__(self)
        GraphicScene.__init__(self)

####################################################################################################

class QtPainter(Painter):

    __STROKE_STYLE__ = {
        None: None,
        'dashDotLine': Qt.DashLine,
        'dotLine': Qt.DotLine,
        'hair': Qt.SolidLine,
        'none': None,

        'solid': Qt.SolidLine,
    }

    __COLOR__ = {
        None : None,
        'black': QColor('black'),
    }

    _logger = _module_logger.getChild('QtPainter')

    ##############################################

    def __init__(self, scene=None):

        super().__init__(scene)

        # self._paper = paper

        self._coordinates = {}

    ##############################################

    def paint(self, painter):

        self._logger.info('paint')

        self._painter = painter
        if self._scene is not None:
            bounding_box = self._scene.bounding_box
            self._scene_offset = QPointF(-bounding_box.x.inf, bounding_box.y.sup)
            self._view_offset = QPointF(30, 30)
            # painter.resetTransform()
            # painter.scale(1, -1) # filp font
            # painter.scale(10, 10) # scale font
            # bounding_box = self._scene.bounding_box
            # painter.translate(-bounding_box.x.inf, bounding_box.y.sup)
        super().paint()

    ##############################################

    def _cast_vector(self, position):

        point = QPointF(position.x, -position.y)
        point += self._scene_offset
        point *= 10
        point += self._view_offset
        return point

    ##############################################

    def _cast_position(self, position):

        if isinstance(position, str):
            return self._coordinates[position]
        elif isinstance(position, Vector2D):
            return self._cast_vector(position)

    ##############################################

    def paint_CoordinateItem(self, item):

        self._coordinates[item.name] = self._cast_vector(item.position)

    ##############################################

    def paint_TextItem(self, item):

        position = self._cast_position(item.position)
        # Fixme: anchor position
        self._painter.drawText(position, item.text)

    ##############################################

    def _set_pen(self, item):

        path_syle = item.path_style
        color = self.__COLOR__[path_syle.stroke_color]
        line_style = self.__STROKE_STYLE__[path_syle.stroke_style]
        line_width = float(path_syle.line_width.replace('pt', '')) / 3 # Fixme: pt ???
        # pen = QPen(
        #     color,
        #     line_width,
        #     line_style,
        # )
        # self._painter.setPen(pen)

    ##############################################

    def paint_CircleItem(self, item):

        center = self._cast_position(item.position)
        radius = 5

        # rectangle = QRectF(
        #     center - QPointF(1, 1)*radius,
        #     QSizeF(1, 1)*2*radius,
        # )
        # self._painter.setPen(QPen(
        #     QColor('black'),
        #     1,
        #     Qt::SolidLine,
        # )
        # self._painter.drawArc(rectangle, 0, 360)
        self._painter.drawEllipse(center, radius, radius)

    ##############################################

    def paint_SegmentItem(self, item):

        self._set_pen(item)
        vertices = [self._cast_position(position) for position in item.positions]
        self._painter.drawLine(*vertices)

    ##############################################

    def paint_CubicBezierItem(self, item):

        self._set_pen(item)
        vertices = [self._cast_position(position) for position in item.positions]
        path = QPainterPath()
        path.moveTo(vertices[0])
        path.cubicTo(*vertices[1:])
        self._painter.drawPath(path)

####################################################################################################

class QtQuickPaintedSceneItem(QQuickPaintedItem, QtPainter):

    _logger = _module_logger.getChild('QtQuickPaintedSceneItem')

    ##############################################

    def __init__(self, parent=None):

        QQuickPaintedItem.__init__(self, parent)
        QtPainter.__init__(self)

        self.setAntialiasing(True)
        # self.setRenderTarget(QQuickPaintedItem.Image) # high quality antialiasing
        self.setRenderTarget(QQuickPaintedItem.FramebufferObject) # use OpenGL

    ##############################################

    scene_changed = pyqtSignal()

    @pyqtProperty(QtScene, notify=scene_changed)
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        print('set scene', scene)
        self._scene = scene
        self.update()

####################################################################################################

# qmlRegisterType(QtQuickPaintedSceneItem, 'Patro', 1, 0, 'PaintedSceneItem')
