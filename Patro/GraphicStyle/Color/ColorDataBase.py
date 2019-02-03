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

__all__ = ['Color', 'ColorDataBase']

####################################################################################################

import colorsys

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
                self._red = color.red_float
                self._green = color.green_float
                self._blue = color.blue_float
            else:
                rgb = str(color)
                if not rgb.startswith('#'):
                    raise ValueError('Invalid color {}'.format(rgb))
                rgb = rgb[1:]
                red, green, blue = rgb[:2], rgb[2:4], rgb[-2:]
                self._red, self._green, self._blue = [self._to_float(int(x, 16))
                                                      for x in (red, green, blue)]
        elif number_of_args == 3:
            self._red, self._green, self._blue = [self._check_value(arg) for arg in args]
        else:
            self._red, self._green, self._blue = 0

        if 'hue' in kwargs:
            if 'light' in kwargs:
                hue, light, saturation = [kwargs[x] for x in ('hue', 'light', 'saturation')]
                red, green, blue = colorsys.hls_to_rgb(hue, light, saturation)
            elif 'value' in kwargs:
                hue, value, saturation = [kwargs[x] for x in ('hue', 'value', 'saturation')]
                red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
            else:
                raise ValueError('Missing color parameter')
            self._red, self._green, self._blue = [self._check_value(x) for x in (red, green, blue)]

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
        return self.__STR_FORMAT__.format(self.red, self.green, self.blue)

    ##############################################

    def __repr__(self):
        return 'Color({})'.format(str(self))

    ##############################################

    @staticmethod
    def _to_int(x):
        return int(x*255)

    @staticmethod
    def _to_float(x):
        return x/255

    ##############################################

    def _check_value(self, value):

        if isinstance(value, int):
            if 0 <= value <= 255:
                return self._to_float(value)

        if isinstance(value, float):
            if 0 <= value <= 1:
                # return int(value * 255)
                return value # keep float

        raise ValueError('Invalid colour {}'.format(value))

    ##############################################

    @property
    def red_float(self):
        return self._red

    @property
    def red(self):
        return self._to_int(self._red)

    @red.setter
    def red(self, value):
        self._red = self._check_value(value)

    @property
    def green_float(self):
        return self._green

    @property
    def green(self):
        return self._to_int(self._green)

    @green.setter
    def green(self, value):
        self._green = self._check_value(value)

    @property
    def blue_float(self):
        return self._blue

    @property
    def blue(self):
        return self._to_int(self._blue)

    @blue.setter
    def blue(self, value):
        self._blue = self._check_value(value)

    ##############################################

    # note hue and saturation is ambiguous

    @property
    def hls(self):
        return colorsys.rgb_to_hls(self._red, self._green, self._blue)

    @property
    def hsv(self):
        return colorsys.rgb_to_hsv(self._red, self._green, self._blue)

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
