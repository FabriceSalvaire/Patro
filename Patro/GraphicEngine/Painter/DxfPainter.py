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

__all__ = [
    'DxfPainter',
]

####################################################################################################

import logging

from Patro.GeometryEngine.Vector import Vector2D
from .Painter import Painter

try:
    import ezdxf
except ImportError:
    ezdxf = None

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class DxfPainterBase(Painter):

    ##############################################

    def __init__(self, path, scene, paper):

        super().__init__(scene)

        self._path = path
        self._paper = paper

        self._coordinates = {}

    ##############################################

    def _cast_position(self, position):

        # Fixme: to base class

        if isinstance(position, str):
            return self._coordinates[position]
        elif isinstance(position, Vector2D):
            return position

    ##############################################

    def paint_CoordinateItem(self, item):
        # Fixme: to base class
        self._coordinates[item.name] = item.position

####################################################################################################

class EzdxfPainter(DxfPainterBase):

    # AC1009 AutoCAD R12
    # AC1012 AutoCAD R13 -> R2000
    # AC1014 AutoCAD R14 -> R2000
    # AC1015 AutoCAD R2000
    # AC1018 AutoCAD R2004
    # AC1021 AutoCAD R2007
    # AC1024 AutoCAD R2010
    # AC1027 AutoCAD R2013
    # AC1032 AutoCAD R2018

    __STROKE_STYLE__ = {
        None: None,
        'dashDotLine': 'DASHDOT',
        'dotLine': 'DOTTED',
        'hair': 'CONTINUOUS',
        'none': 'PHANTOM', # Fixme: ???

        'solid': 'CONTINUOUS',
    }

    __COLOR__ = {
        None : None,
        'black': 0,
    }

    ##############################################

    def __init__(self, path, scene, paper, dxf_version='R2010'):

        super().__init__(path, scene, paper)

        self._dxf_version = dxf_version
        self._drawing = ezdxf.new(dxf_version)
        self._model_space= self._drawing.modelspace() # add new entities to the model space
        # self._model_space.page_setup(
        #     size=(self._paper.width, self._paper.height),
        #     # margins=(top, right, bottom, left)
        #     units='mm',
        # )

        # print('Available line types:')
        # for line_type in self._drawing.linetypes:
        #     print('{}: {}'.format(line_type.dxf.name, line_type.dxf.description))

        self.paint()
        self._drawing.saveas(path)

    ##############################################

    def _cast_position(self, position):

        position = super()._cast_position(position)
        position = position.clone() * 10 # Fixme: cm -> mm
        return position

    ##############################################

    def _cast_positions(self, positions):

        return [list(self._cast_position(position)) for position in positions]

    ##############################################

    def _graphic_style(self, item):

        # cf. https://ezdxf.readthedocs.io/en/latest/graphic_base_class.html#common-dxf-attributes-for-dxf-r13-or-later

        path_style = item.path_style
        if path_style.stroke_color is None:
            return {'linetype': 'PHANTOM', 'color': 2} # Fixme:
        color = self.__COLOR__[path_style.stroke_color] # see also true_color color_name (AutoCAD R2004)
        line_type = self.__STROKE_STYLE__[path_style.stroke_style]
        # https://ezdxf.readthedocs.io/en/latest/graphic_base_class.html#GraphicEntity.dxf.lineweight
        # line_weight = float(path_syle.line_width.replace('pt', '')) / 3 # Fixme: pt ???

        return {'linetype': line_type, 'color': color} # 'lineweight':line_weight

    ##############################################

    def paint_TextItem(self, item):

        position = self._cast_position(item.position)
        # Fixme: anchor position
        # https://ezdxf.readthedocs.io/en/latest/tutorials/text.html
        self._model_space.add_text(item.text).set_pos(list(position), align='CENTER')

    ##############################################

    def paint_CircleItem(self, item):
        # in fact a graphic dot
        pass # skipped for DXF

    ##############################################

    def paint_SegmentItem(self, item):

        positions = self._cast_positions(item.positions)
        self._model_space.add_line(
            *positions,
            dxfattribs=self._graphic_style(item),
        )

    ##############################################

    def paint_CubicBezierItem(self, item):

        positions = self._cast_positions(item.positions)
        for position in positions:
            position.append(0)
        # https://ezdxf.readthedocs.io/en/latest/layouts.html#Layout.add_open_spline
        self._model_space.add_open_spline(
            positions,
            degree=3,
            dxfattribs=self._graphic_style(item),
        )

####################################################################################################

_driver_to_cls = {
    'ezdxf': EzdxfPainter,
}

def DxfPainter(*args, **kwargs):
    """Wrapper to driver classes"""
    driver = kwargs.get('driver', 'ezdxf')
    if 'driver' in kwargs:
        del kwargs['driver']
    return _driver_to_cls[driver](*args, **kwargs)
