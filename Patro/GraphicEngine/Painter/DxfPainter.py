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
from Patro.GraphicStyle import StrokeStyle, Colors
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
        StrokeStyle.NoPen: 'PHANTOM', # Fixme: ???
        StrokeStyle.SolidLine: 'CONTINUOUS',
        StrokeStyle.DashLine: 'DASH', # Fixme:
        StrokeStyle.DotLine: 'DOTTED',
        StrokeStyle.DashDotLine: 'DASHDOT',
        StrokeStyle.DashDotDotLine: 'DASHDOTDOT', # Fixme:
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

    def cast_position(self, position):
        return super().cast_position(position) * 10 # Fixme: cm -> mm

    ##############################################

    def _graphic_style(self, item):

        # cf. https://ezdxf.readthedocs.io/en/latest/graphic_base_class.html#common-dxf-attributes-for-dxf-r13-or-later

        path_style = item.path_style
        if path_style.stroke_color is None:
            return {'linetype': 'PHANTOM', 'color': 2} # Fixme:
        color = self.__COLOR__[path_style.stroke_color.name] # see also true_color color_name (AutoCAD R2004)
        line_type = self.__STROKE_STYLE__[path_style.stroke_style]
        # https://ezdxf.readthedocs.io/en/latest/graphic_base_class.html#GraphicEntity.dxf.lineweight
        # line_weight = float(path_syle.line_width.replace('pt', '')) / 3 # Fixme: pt ???

        return {'linetype': line_type, 'color': color} # 'lineweight':line_weight

    ##############################################

    def paint_TextItem(self, item):

        position = self.cast_position(item.position)
        # Fixme: anchor position
        # https://ezdxf.readthedocs.io/en/latest/tutorials/text.html
        self._model_space.add_text(item.text).set_pos(list(position), align='CENTER')

    ##############################################

    def paint_CircleItem(self, item):
        # in fact a graphic dot
        pass # skipped for DXF

    ##############################################

    def paint_SegmentItem(self, item):

        positions = self.cast_item_coordinates(item)
        self._model_space.add_line(
            *positions,
            dxfattribs=self._graphic_style(item),
        )

    ##############################################

    def paint_CubicBezierItem(self, item):

        positions = self.cast_item_coordinates(item)
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
