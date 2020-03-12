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

from Patro.GraphicStyle import StrokeStyle
from .Environment import Environment

####################################################################################################

class TikzFigure(Environment):

    ##############################################

    __STROKE_STYLE__ = {
        StrokeStyle.DashLine: 'dash pattern=on 5mm off 5mm',
        StrokeStyle.DashDotLine: 'dash pattern=on 5mm off 4mm on 2mm off 4mm', # 'loosely dashdotted',
        StrokeStyle.DotLine: 'dash pattern=on 2mm off 2mm', # 'dotted',
        StrokeStyle.NoPen: None,
        StrokeStyle.SolidLine: 'solid',
    }

    @staticmethod
    def format_path_style(path_syle):

        stroke_style = TikzFigure.__STROKE_STYLE__[path_syle.stroke_style]
        stroke_color = path_syle.stroke_color.name

        styles = []
        styles.append('line width={}'.format(path_syle.line_width))
        if stroke_style is not None:
            styles.append(stroke_style)
        if stroke_color is not None:
            styles.append(stroke_color)
        return ', '.join(styles)

    ##############################################

    def __init__(self, options=''):
        super(TikzFigure, self).__init__('tikzpicture', options)
