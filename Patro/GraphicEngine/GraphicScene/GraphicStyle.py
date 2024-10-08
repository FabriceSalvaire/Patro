####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Fabrice Salvaire
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

"""Module to implement graphic styles.

"""

# Fixme: get_geometry / as argument

####################################################################################################

__all__ = [
    'GraphicPathStyle',
    'GraphicBezierStyle',
    'Font',
]

####################################################################################################

import logging

from Patro.GraphicStyle import Color, Colors, StrokeStyle, CapStyle, JoinStyle

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GraphicPathStyle:

    """Class to define path style"""

    ##############################################

    def __init__(self, **kwargs: dict) -> None:
        """Constructor method

        *color* can be a defined color name, a '#rrggbb' string or a :class:`Color` instance.

        :param line_width: defaults to 1.0

        :param stroke_alpha: defaults to 1.0
        :param stroke_color: defaults to :const:`Colors.black`
        :param stroke_style: defaults to :const:`StrokeStyle.SolidLine`

        :param fill_color: defaults to `None`
        :param fill_alpha: defaults to 1.0

        :param cap_style: defaults to :const:`CapStyle.SquareCap`
        :param join_style: defaults to :const:`JoinStyle.BevelJoin`
        """
        self.stroke_style = kwargs.get('stroke_style', StrokeStyle.SolidLine)
        self.line_width = kwargs.get('line_width', 1.0)
        self.stroke_color = kwargs.get('stroke_color', Colors.black)
        self.stroke_alpha = kwargs.get('stroke_alpha', 1.0)

        self.fill_color = kwargs.get('fill_color', None)   # only for closed path
        self.fill_alpha = kwargs.get('fill_alpha', 1.0)

        # This is default Qt
        self.cap_style = kwargs.get('cap_style', CapStyle.SquareCap)
        self.join_style = kwargs.get('join_style', JoinStyle.BevelJoin)

    ##############################################

    def _dict_keys(self) -> list:
        return (
            'stroke_style',
            'line_width',
            'stroke_color',
            'fill_color',
        )

    ##############################################

    def _to_dict(self) -> dict:
        return {name: getattr(self, '_' + name) for name in self._dict_keys()}

    ##############################################

    def clone(self) -> 'GraphicPathStyle':
        return self.__class__(**self._to_dict())

    ##############################################

    def __repr__(self) -> str:
        return '{0}({1})'.format(self.__class__.__name__, self._to_dict())

    ##############################################

    @property
    def stroke_style(self) -> StrokeStyle:
        return self._stroke_style

    @stroke_style.setter
    def stroke_style(self, value: str) -> None:
        self._stroke_style = StrokeStyle(value)

    ##############################################

    @property
    def line_width(self) -> int | float | str:
        return self._line_width

    @line_width.setter
    def line_width(self, value: int | float | str) -> None:
        # Fixme: float or TypographyUnit
        self._line_width = value

    @property
    def line_width_as_float(self) -> float:
        return float(self._line_width)

    ##############################################

    @property
    def stroke_color(self) -> Color:
        return self._stroke_color

    @stroke_color.setter
    def stroke_color(self, value: Color | str) -> None:
        self._stroke_color = Colors.ensure_color(value)

    @property
    def stroke_alpha(self) -> float:
        return self._stroke_alpha

    @stroke_alpha.setter
    def stroke_alpha(self, value: float | str) -> None:
        self._stroke_alpha = float(value)   # Fixme: check < 1

    ##############################################

    @property
    def fill_color(self) -> Color:
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value: Color | str) -> None:
        self._fill_color = Colors.ensure_color(value)

    @property
    def fill_alpha(self) -> float:
        return self._fill_alpha

    @fill_alpha.setter
    def fill_alpha(self, value: int | float) -> None:
        self._fill_alpha = float(value)

    ##############################################

    @property
    def cap_style(self) -> CapStyle:
        return self._cap_style

    @cap_style.setter
    def cap_style(self, value: str) -> None:
        self._cap_style = CapStyle(value)

    @property
    def join_style(self) -> JoinStyle:
        return self._join_style

    @join_style.setter
    def join_style(self, value: str) -> None:
        self._join_style = JoinStyle(value)

####################################################################################################

class GraphicBezierStyle(GraphicPathStyle):

    """Class to define Bézier curve style"""

    ##############################################

    def __init__(self, **kwargs: dict) -> None:
        """
        :param show_control: defaults to `False`
        :param control_color: defaults to `None`
        """
        super().__init__(**kwargs)
        self.show_control = kwargs.get('show_control', False)
        self.control_color = kwargs.get('control_color', None)

    ##############################################

    def _dict_keys(self) -> list:
        return (
            'show_control',
            'control_color',
        )

    ##############################################

    @property
    def show_control(self) -> bool:
        return self._show_control

    @show_control.setter
    def show_control(self, value: bool) -> None:
        self._show_control = bool(value)

    ##############################################

    @property
    def control_color(self) -> Color:
        return self._control_color

    @control_color.setter
    def control_color(self, value: Color | str) -> None:
        self._control_color = Colors.ensure_color(value)

####################################################################################################

class Font:

    """Class to define font style"""

    ##############################################

    def __init__(self, family: str, point_size: int | float) -> None:
        self.family = family
        self.point_size = point_size
