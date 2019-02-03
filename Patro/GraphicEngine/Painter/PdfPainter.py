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
    'PdfPainter',
]

####################################################################################################

import logging

from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicStyle import StrokeStyle
from .Painter import Painter, Tiler

try:
    import reportlab
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm, cm
except ImportError:
    reportlab = None

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PdfPainterBase(Painter):

    ##############################################

    def __init__(self, path, scene, paper):

        super().__init__(scene)

        self._path = path
        self._paper = paper

    ##############################################

    @staticmethod
    def mm_to_pt(x):
        return x * 72 / 25.4

    ##############################################

    @property
    def page_size(self):
        return [self.mm_to_pt(x) for x in (self._paper.width, self._paper.height)]

####################################################################################################

class ReportlabPainter(PdfPainterBase):

    __STROKE_STYLE__ = {
        StrokeStyle.NoPen: None,
        StrokeStyle.SolidLine: (),
        StrokeStyle.DashLine: (), # Fixme: ???
        StrokeStyle.DotLine: (1, 2),
        StrokeStyle.DashDotLine: (6, 3),
        StrokeStyle.DashDotDotLine: (), # Fixme: ???
    }

    ##############################################

    def __init__(self, path, scene, paper):

        super().__init__(path, scene, paper)

        self._canvas = canvas.Canvas(
            str(self._path),
            pagesize=self.page_size,
            # bottomup=1,
            # pageCompression=0,
            # encoding=rl_config.defaultEncoding,
            # verbosity=0,
            # encrypt=None,
        )

        # self._canvas.setAuthor()
        # self._canvas.addOutlineEntry(title, key, level=0, closed=None)
        # self._canvas.setTitle(title)
        # self._canvas.setSubject(subject)

        bounding_box = scene.bounding_box
        # print(bounding_box, bounding_box.x.length, bounding_box.y.length)
        self._canvas.translate(-bounding_box.x.inf*cm, -bounding_box.y.inf*cm)
        self._canvas.translate(1*cm, 1*cm) # Fixme: margin

        self._canvas.setFont('Times-Roman', 20)

        self.paint()
        self._canvas.showPage()
        self._canvas.save()

    ##############################################

    def cast_position(self, position):
        return super().cast_position(position) * cm * .7 # Fixme:

    ##############################################

    def _set_graphic_style(self, item):

        path_syle = item.path_style
        color = path_syle.stroke_color.name
        self._canvas.setStrokeColor(color)
        line_style = self.__STROKE_STYLE__[path_syle.stroke_style]
        self._canvas.setDash(*line_style)
        line_width = float(path_syle.line_width.replace('pt', '')) / 3 # Fixme: pt ???
        self._canvas.setLineWidth(line_width)

    ##############################################

    def paint_TextItem(self, item):

        position = self.cast_position(item.position)
        # Fixme: anchor position
        self._canvas.drawString(position.x, position.y, item.text)

    ##############################################

    def paint_CircleItem(self, item):

        position = self.cast_position(item.position)
        self._canvas.saveState()
        self._canvas.setFillColor('black')
        self._canvas.circle(position.x, position.y, 2*mm, fill=1)
        self._canvas.restoreState()

    ##############################################

    def paint_SegmentItem(self, item):

        # self._set_graphic_style(item)
        self._canvas.line(*self.cast_item_coordinates(item, flat=True))

    ##############################################

    def paint_CubicBezierItem(self, item):

        # self._set_graphic_style(item)
        self._canvas.bezier(*self.cast_item_coordinates(item, flat=True))

####################################################################################################

_driver_to_cls = {
    'reportlab': ReportlabPainter,
}

def PdfPainter(*args, **kwargs):
    """Wrapper to driver classes"""
    driver = kwargs.get('driver', 'reportlab')
    del kwargs['driver']
    return _driver_to_cls[driver](*args, **kwargs)
