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

"""Module to implement a colour database.

"""

####################################################################################################

__all__ = ['Color', 'ColorDataBase']

####################################################################################################

class Color:

    """Class to define a colour

    Usage::

         color.red
         color.blue
         color.green

         color.name

         # to get a '#rrggbb' string
         str(color)

         color1 == color2

    """

    __STR_FORMAT__ = '#' + '{:02x}'*3

    ##############################################

    def __init__(self, *args, **kwargs):

        # self._rgb = str(rgb)

        number_of_args = len(args)
        if number_of_args == 1:
            color = args[0]
            if isinstance(str, Color):
                self._red = color.red
                self._green = color.green
                self._blue = color.blue
            else:
                rgb = str(color)
                if not rgb.startswith('#'):
                    raise ValueError('Invalid color {}'.format(rgb))
                rgb = rgb[1:]
                self._red = int(rgb[:2], 16)
                self._green = int(rgb[2:4], 16)
                self._blue = int(rgb[-2:], 16)
        elif number_of_args == 3:
            self._red, self._green, self._blue = [int(arg) for arg in args]

        # self._name = kwargs.get('name', None)
        if 'name' in kwargs:
            self._name = kwargs['name']
        else:
            self._name = None

    ##############################################

    def clone(self):
        return self.__class__(self._red, self._green, self._blue, name=self._name)

    ##############################################

    def __str__(self):
        return self.__STR_FORMAT__.format(self._red, self._green, self._blue)

    ##############################################

    def __repr__(self):
        return 'Color({})'.format(str(self))

    ##############################################

    def _check_value(self, value):
        if isinstance(value, int):
            if 0 <= value <= 255:
                return value
        if isinstance(value, float):
            if 0 <= value <= 1:
                return int(value * 255)
        raise ValueError('Invalid colour {}'.format(value))

    ##############################################

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        self._red = self._check_value(value)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        self._green = self._check_value(value)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        self._blue = self._check_value(value)

    ##############################################

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    ##############################################

    def __eq__(self, other):
        return str(self) == str(other)

####################################################################################################

class ColorDataBase:

    """Class to implement a colour database.

    The class implements a dictionary API::

      color_database['black']
      'black' in 'color_database

       for color in color_database:
           pass

    We can get a color directly using::

        color_database.black

    """

    ##############################################

    def __init__(self):
        self._colors = {}

    ##############################################

    def __len__(self):
        return len(self._colors)

    def __iter__(self):
        return iter(self._colors.values())

    def __contains__(self, name):
        return name in self._colors

    def __getitem__(self, name):
        return self._colors[str(name)]

    def __getattr__(self, name):
        return self._colors[name]

    ##############################################

    def iter_names(self):
        return iter(self._colors.keys())

    ##############################################

    def add(self, name, color):
        """Register a :class:`Color` instance"""
        # Fixme: color.name ???
        self._colors[str(name)] = color

    ##############################################

    def ensure_color(self, color):

        """Ensure *color* is a :class:`Color` instance"""

        if color is None:
            return None
        elif isinstance(color, Color):
            return color
        elif isinstance(color, str):
            if color.startswith('#'):
                return Color(color)
            else:
                return self[color]

        raise ValueError('Invalid color {}'.format(color))
