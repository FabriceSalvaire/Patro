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

"""Module to implement a colour database.
"""

####################################################################################################

__all__ = ['Colors']

####################################################################################################

from . import color_data as _color_data
from .ColorDataBase import Color, ColorDataBase

####################################################################################################

#: Colour Database Singleton as an instance of :class:`ColorDataBase`
Colors = ColorDataBase()

def __init__():
    # First name set color
    for color_set in (
            _color_data.BASE_COLORS,
            _color_data.TABLEAU_COLORS,
            _color_data.XKCD_COLORS,
            _color_data.CSS4_COLORS,
            _color_data.QML_COLORS,
            _color_data.VALENTINA_COLORS ,
    ):
        for name, value in color_set.items():
            name = name.replace(' ', '_')
            color = Color(value, name=name)
            if name in Colors and color != Colors[name]:
                pass
                # print('# {:15} {} vs {}'.format(name, color, Colors[name]))
                # print('Warning: color name clash: {} {} vs {}'.format(name, color, Colors[name]))
            else:
                Colors.add(name, color)

__init__()
