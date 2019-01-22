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

"""Module to implement graphic styles.

"""

# Fixme: get_geometry / as argument

####################################################################################################

__all__= ['GraphicPathStyle', 'GraphicBezierStyle', 'Font']

####################################################################################################

import logging

from Patro.GraphicStyle import Colors, StrokeStyle

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GraphicPathStyle:

    ##############################################

    def __init__(self,
                 stroke_style=StrokeStyle.SolidLine,
                 line_width=1.0,
                 stroke_color=Colors.black,
                 fill_color=None, # only for closed path
    ):

        """*color* can be a defined color name, a '#rrggbb' string or a :class:`Color` instance.

        """

        self.stroke_style = stroke_style
        self.line_width = line_width
        self.stroke_color = stroke_color
        self.fill_color = fill_color

    ##############################################

    def clone(self):
        return self.__class__(
            self._stroke_style,
            self._line_width,
            self._stroke_color,
            self._fill_color,
        )

    ##############################################

    def __repr__(self):
        return 'GraphicPathStyle({0._stroke_style}, {0._line_width}, {0._stroke_color}, {0._fill_color})'.format(self)

    ##############################################

    @property
    def stroke_style(self):
        return self._stroke_style

    @stroke_style.setter
    def stroke_style(self, value):
        self._stroke_style = StrokeStyle(value)

    ##############################################

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        self._line_width = value # Fixme: float ???

    @property
    def line_width_as_float(self):
        line_width = self._line_width
        # Fixme: use scale ?
        if isinstance(line_width, float):
            return line_width
        else:
            line_width = line_width.replace('pt', '')
            line_width = line_width.replace('px', '')
            return float(line_width)

    ##############################################

    @property
    def stroke_color(self):
        return self._stroke_color

    @stroke_color.setter
    def stroke_color(self, value):
        self._stroke_color = Colors.ensure_color(value)

    ##############################################

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value):
        self._fill_color = Colors.ensure_color(value)

####################################################################################################

class GraphicBezierStyle(GraphicPathStyle):

    ##############################################

    def __init__(self,
                 # Fixme: duplicate
                 stroke_style=StrokeStyle.SolidLine,
                 line_width=1.0,
                 stroke_color=Colors.black,
                 fill_color=None, # only for closed path
                 #
                 show_control=False,
                 control_color=None,
    ):

        super().__init__(stroke_style, line_width, stroke_color, fill_color)
        self._show_control = show_control
        self._control_color = Colors.ensure_color(control_color)

    ##############################################

    def clone(self):
        return self.__class__(
            self.stroke_style,
            self.line_width,
            self.stroke_color,
            self.fill_color,
            self._show_control,
            self._control_color,
        )

    ##############################################

    @property
    def show_control(self):
        return self._show_control

    @show_control.setter
    def show_control(self, value):
        self._show_control = value

    ##############################################

    @property
    def control_color(self):
        return self._control_color

    @control_color.setter
    def control_color(self, value):
        self._control_color = value

####################################################################################################

class Font:

    ##############################################

    def __init__(self, family, point_size):

        self.family = family
        self.point_size = point_size
