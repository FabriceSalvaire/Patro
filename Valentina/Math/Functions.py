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

import math

####################################################################################################

def rint(f):
    return int(round(f))

####################################################################################################

def ceil_int(f):
    return int(math.ceil(f))

####################################################################################################

def middle(a, b):
    return .5*(a + b)

####################################################################################################

def cmp(a, b):
    return (a > b) - (a < b)

# Fixme: sign_of ?
def sign(x):
    return cmp(x, 0)

def epsilon_float(a, b, epsilon = 1e-3):
    return abs(a-b) <= epsilon

def trignometric_clamp(x):

    """ Clamp *x* in the range [-1.,1]. """

    if x > 1.:
        return 1.
    elif x < -1.:
        return -1.
    else:
        return x

####################################################################################################

def is_in_trignometric_range(x):
    return -1. <= x <= 1
