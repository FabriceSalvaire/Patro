####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Salvaire Fabrice
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
import unittest
from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from IntervalArithmetic import Interval2D

from Patro.FileFormat.Svg import SvgFormat
from Patro.FileFormat.Svg.SvgFile import SvgFile, SvgFileInternal
from Patro.GeometryEngine.Transformation import AffineTransformation2D
from Patro.GeometryEngine.Vector import Vector2D
# from PatroExample import find_data_path

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

svg_data = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   version="1.1"
   viewBox="0 0 140 140"
   height="140mm"
   width="140mm"
   >
  <title id="title1">SVG Basic Demo</title>
  <g id="layer1" transform="translate(0,0)" style="stroke:#000000">
    <path id="path-x"  d="M 20,20 h 100" />
    <path id="path-y"  d="M 20,20 v 100" />
    <path id="path-45" d="M 20,20 l 100,100" />

    <rect id="rect-0"  x="20" y="20" height="10" width="10" />
    <rect id="rect-x1" x="40" y="20" height="10" width="10" />
    <rect id="rect-x2" x="80" y="20" height="10" width="10" />
    <rect id="rect-y1" x="20" y="40" height="10" width="10" />
    <rect id="rect-y2" x="20" y="80" height="10" width="10" />
    <rect id="rect-bisect" x="50" y="50" height="10" width="10" />

    <rect id="rect-45-2" transform="rotate(45)" x="50" y="50" height="10" width="10" />
    <rect id="rect-45" transform="rotate(45,75,75)" x="70" y="70" height="10" width="10" />
    <rect id="rect-30" transform="rotate(30,85,85)" x="80" y="80" height="10" width="10" />
    <rect id="rect-60" transform="rotate(60,95,95)" x="90" y="90" height="10" width="10" />
  </g>
</svg>
"""

####################################################################################################

class SceneImporter(SvgFileInternal):

    # Fixme: duplicated code

    _logger = _module_logger.getChild('SceneImporter')

    ##############################################

    def __init__(self, svg_path, data=None):

        self._scene = {}
        self._bounding_box = None

        super().__init__(svg_path, data)

    ##############################################

    def __len__(self):
        return len(self._scene)

    def __getitem__(self, name):
        return self._scene[name]

    @property
    def scene(self):
        return self._scene

    @property
    def bounding_box(self):
        return self._bounding_box

    ##############################################

    def _add_to_scene(self, name, geometry):
        self._scene[name] = geometry

    ##############################################

    def _update_bounding_box(self, item):

        interval = item.bounding_box
        if self._bounding_box is None:
            self._bounding_box = interval
        else:
            self._bounding_box |= interval

    ##############################################

    def on_svg_root(self, svg_root):
        super().on_svg_root(svg_root)
        self._screen_transformation = AffineTransformation2D.Screen(self._view_box.y.sup)

    ##############################################

    def on_group(self, group):
        # self._logger.info('Group: {}\n{}'.format(group.id, group))
        pass

    ##############################################

    def on_graphic_item(self, item):

        state = self._dispatcher.state.clone().merge(item)
        self._logger.info('Item: {}\n{}'.format(item.id, item))
        # self._logger.info('Item State:\n' + str(state))

        transformation = state.transform
        # transformation = self._screen_transformation * state.transform
        self._logger.info('Sate Transform\n' + str(transformation))
        if isinstance(item, SvgFormat.Path):
            path = item.path_data
            if path is not None: # Fixme:
                path = path.transform(transformation)
                self._update_bounding_box(path)
                self._add_to_scene(item.id, path)
        elif isinstance(item, SvgFormat.Rect):
            path = item.geometry
            self._add_to_scene(item.id, path)

####################################################################################################

def count_svg_tags(svg_data):

    tag_counter = {}
    for line in svg_data.splitlines():
        line = line.strip()
        if line.startswith('<'):
            position = line.find(' ')
            tag = line[1:position]
            if tag[0].isalpha():
                tag_counter.setdefault(tag, 0)
                tag_counter[tag] += 1

    return tag_counter

####################################################################################################

class TestLine2D(unittest.TestCase):

    ##############################################

    def test(self):

        svg_path = 'basic-demo-2.by-hand.svg'
        # svg_path = find_data_path('svg', svg_path)
        #data = None
        data = svg_data

        scene_importer = SceneImporter(svg_path, data=data)
        scene = scene_importer.scene

        interval = Interval2D((20, 120), (20, 120))
        self.assertEqual(scene_importer.bounding_box, interval)

        tag_counter = count_svg_tags(data)
        number_of_items = sum([tag_counter[x] for x in ('path', 'rect')])
        self.assertEqual(len(scene_importer), number_of_items)

        # for name, item in scene.items():
        #     print(name, item)

        origin = Vector2D(20, 20)
        for name in ('path-x', 'path-y', 'path-45'):
            self.assertEqual(scene[name].p0, origin)

        for name, p0 in (
                ('rect-0', (20, 20)),
                ('rect-x1', (40, 20)),
                ('rect-x2', (80, 20)),
                ('rect-y1', (20, 40)),
                ('rect-y2', (20, 80)),
                ('rect-bisect', (50, 50)),
                #
                # ('rect-45-2', (50, 50)),
                # ('rect-45', (70, 70)),
                # ('rect-30', (80, 80)),
                # ('rect-60', (90, 90)),
        ):
            self.assertEqual(scene[name].p0, Vector2D(p0))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
