####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
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

from .Environment import Environment

####################################################################################################

class TikzFigure(Environment):

    ##############################################

    __STROKE_STYLE__ = {
        None: None,
        'dashDotLine': 'dash pattern=on 5mm off 4mm on 2mm off 4mm', # 'loosely dashdotted',
        'dotLine': 'dash pattern=on 2mm off 2mm', # 'dotted',
        'hair': 'solid',
        'none': None,

        'solid': 'solid',
        }

    __COLOR__ = {
        None : None,
        'black': 'black',
        }

    @staticmethod
    def format_path_style(path_syle):

        stroke_style = TikzFigure.__STROKE_STYLE__[path_syle.stroke_style]
        stroke_color = TikzFigure.__COLOR__[path_syle.stroke_color]

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
