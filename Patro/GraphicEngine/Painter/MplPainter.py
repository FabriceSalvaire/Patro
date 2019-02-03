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

from matplotlib import pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

from Patro.GeometryEngine.Vector import Vector2D
from .Painter import Painter, Tiler

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class MplPainter(Painter):

    __STROKE_STYLE__ = {
        None: None,
        'dashDotLine': 'dashdot', # '--'
        'dotLine': 'dotted', # ':'
        'hair': 'solid', # '-'
        'none': None,

        'solid': 'solid',
    }

    __COLOR__ = {
        None : None,
        'black': 'black',
    }

    ##############################################

    def __init__(self, scene, paper):

        super().__init__(scene)

        self._paper = paper

        self._figure = plt.figure(
            # figsize=(self._paper.width_in, self._paper.height_in),
            # dpi=200,
        )
        self._axes = self._figure.add_subplot(111)

        bounding_box = scene.bounding_box
        factor = 10 / 100
        x_margin = bounding_box.x.length * factor
        y_margin = bounding_box.y.length * factor
        margin = max(x_margin, y_margin)
        bounding_box = bounding_box.clone().enlarge(margin)
        self._axes.set_xlim(bounding_box.x.inf, bounding_box.x.sup)
        self._axes.set_ylim(bounding_box.y.inf, bounding_box.y.sup)
        self._axes.set_aspect('equal')

        self._coordinates = {}
        self.paint()

    ##############################################

    def show(self):
        plt.show()

    ##############################################

    def _add_path(self, item, vertices, codes):

        path = Path(vertices, codes)

        path_syle = item.path_style
        color = self.__COLOR__[path_syle.stroke_color]
        line_style = self.__STROKE_STYLE__[path_syle.stroke_style]
        line_width = float(path_syle.line_width.replace('pt', '')) / 3
        patch = patches.PathPatch(path, edgecolor=color, facecolor='none', linewidth=line_width, linestyle=line_style)
        self._axes.add_patch(patch)

    ##############################################

    def paint_CoordinateItem(self, item):

        self._coordinates[item.name] = item.position

    ##############################################

    def _cast_position(self, position):

        if isinstance(position, str):
            return self._coordinates[position]
        elif isinstance(position, Vector2D):
            return position

    ##############################################

    def paint_TextItem(self, item):

        position = self._cast_position(item.position)
        # Fixme: anchor position
        self._axes.text(position.x, position.y, item.text)

    ##############################################

    def paint_CircleItem(self, item):

        center = list(self._cast_position(item.position))
        circle = plt.Circle(center, .5, color='black')
        self._axes.add_artist(circle)

    ##############################################

    def paint_SegmentItem(self, item):

        vertices = [list(self._cast_position(position)) for position in item.positions]
        codes = [Path.MOVETO, Path.LINETO]
        self._add_path(item, vertices, codes)

    ##############################################

    def paint_CubicBezierItem(self, item):

        vertices = [list(self._cast_position(position)) for position in item.positions]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        self._add_path(item, vertices, codes)
