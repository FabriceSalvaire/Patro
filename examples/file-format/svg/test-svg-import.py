####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Fabrice Salvaire
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

from pathlib import Path

# Disable if executed by patro
# from Patro.Common.Logging import Logging
# Logging.setup_logging()

from Patro.FileFormat.Svg import SvgFormat
from Patro.FileFormat.Svg.SvgFile import SvgFile, SvgFileInternal
from Patro.GraphicEngine.GraphicScene.GraphicStyle import GraphicPathStyle, GraphicBezierStyle
from Patro.GraphicEngine.Painter.QtPainter import QtScene
from Patro.GraphicStyle import Colors, StrokeStyle, CapStyle
from Patro.GraphicStyle.Color.ColorDataBase import Color
from PatroExample import find_data_path

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SceneImporter(SvgFileInternal):

    _logger = _module_logger.getChild('SceneImporter')

    ##############################################

    def __init__(self, svg_path):

        self._bounding_box = None
        self._item_counter = 0
        self._scene = QtScene()

        super().__init__(svg_path)

        # Fixme:
        self._scene.bounding_box = self._bounding_box

        self._logger.info('Number of SVG item: {}'.format(self._item_counter))
        self._logger.info('Number of scene item: {}'.format(self._scene.number_of_items))

    ##############################################

    @property
    def scene(self):
        return self._scene

    ##############################################

    def _update_bounding_box(self, item):

        interval = item.bounding_box
        if self._bounding_box is None:
            self._bounding_box = interval
        else:
            self._bounding_box |= interval

    ##############################################

    def on_group(self, group):
        pass
        # self._logger.info('Group: {}\n{}'.format(group.id, group))

    ##############################################

    def on_graphic_item(self, item):

        # self._logger.info('Item: {}\n{}'.format(item.id, item))
        state = self._dispatcher.state.clone().merge(item)
        # self._logger.info('Item State:\n' + str(state))

        self._item_counter += 1

        stroke_style = StrokeStyle.SolidLine if state.stroke_dasharray is None else StrokeStyle.DashLine
        fill_color = None if state.fill is None else Color(state.fill)

        path_style = GraphicPathStyle(
            line_width=2,
            stroke_color=Colors.black,
            stroke_style=stroke_style,
            cap_style=CapStyle.RoundCap,
            # fill_color=fill_color,
        )

        transformation = state.transform
        if isinstance(item, SvgFormat.Path):
            # and state.stroke_dasharray is None
            path = item.path_data
            path = path.transform(transformation)
            # Fixme:
            for part in path:
                self._update_bounding_box(part)
            self._scene.add_path(path, path_style)

####################################################################################################

# svg_path = find_data_path('svg', 'demo.svg')
svg_path = find_data_path('patterns-svg', 'veravenus-little-bias-dress.pattern-a0.svg')
# svg_path = find_data_path('patterns-svg', 'test.svg')

# svg_file = SvgFile(svg_path)

scene_importer = SceneImporter(svg_path)
application.qml_application.scene = scene_importer.scene
