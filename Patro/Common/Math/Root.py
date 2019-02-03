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

"""This module implements root finding for second and third degree equation.
"""

####################################################################################################

__all__ = [
    'quadratic_root',
    'cubic_root',
    'fifth_root',
    'fifth_root_normalised',
]

####################################################################################################

from math import acos, cos, pi, sqrt

try:
    import sympy
except ImportError:
    sympy = None

from .Functions import sign

####################################################################################################

def quadratic_root(a, b, c):

    # https://en.wikipedia.org/wiki/Quadratic_equation

    if a == 0 and b == 0:
        return None
    if a == 0:
        return - c / b

    D = b**2 - 4*a*c

    if D < 0:
        return None # not real

    b = -b
    s = 1 / (2*a)
    if D > 0:
        # Fixme: sign of b ???
        r1 = (b - sqrt(D)) * s
        r2 = (b + sqrt(D)) * s
        return r1, r2
    else:
        return b * s

####################################################################################################

def cubic_root(a, b, c, d):

    if a == 0:
        return quadratic_root(b, c, d)
    else:
        return cubic_root_sympy(a, b, c, d)

####################################################################################################

def x_symbol():
    return sympy.Symbol('x', real=True)

def real_roots(expression, x):
    return [i.n() for i in sympy.real_roots(expression, x)]

####################################################################################################

def cubic_root_sympy(a, b, c, d):
    x = x_symbol()
    E = a*x**3 + b*x**2 + c*x + d
    return real_roots(E, x)

####################################################################################################

def cubic_root_normalised(a, b, c):
    x = x_symbol()
    E = x**3 + a*x**2 + b*x + c
    return real_roots(E, x)

####################################################################################################

def fourth_root_normalised(a, b, c, d):
    x = x_symbol()
    E = x**4 + a*x**3 + b*x**2 + c*x + d
    return real_roots(E, x)

####################################################################################################

def fifth_root_sympy(a, b, c, d, e, f):
    x = x_symbol()
    E = a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f
    return real_roots(E, x)

####################################################################################################

def fifth_root_normalised(a, b, c, d, e):
    x = x_symbol()
    E = x**5 + a*x**4 + b*x**3 + c*x**2 + d*x + e
    return real_roots(E, x)

####################################################################################################

def fifth_root(*args):
    # Fixme: RuntimeWarning: divide by zero encountered in double_scalars
    a = args[0]
    if a == 0:
        return fifth_root_sympy(*args)
    else:
        return fifth_root_normalised(*[x/a for x in args[1:]])

####################################################################################################

def cubic_root_normalised(a, b, c):

    # Reference: ???
    # converted from haskell http://hackage.haskell.org/package/cubicbezier-0.6.0.5

    q = (a**2 - 3*b) / 9
    q3 = q**3
    m2sqrtQ = -2 * sqrt(q)
    r = (2*a**3 - 9*a*b + 27*c) / 54
    r2 = r**2
    d = - sign(r)*((abs(r) + sqrt(r2-q3))**1/3) # Fixme: sqrt ??

    if d == 0:
        e = 0
    else:
        e = q/d

    if r2 < q3:
        t = acos(r/sqrt(q3))
        return [
            m2sqrtQ * cos(t/3)          - a/3,
            m2sqrtQ * cos((t + 2*pi)/3) - a/3,
            m2sqrtQ * cos((t - 2*pi)/3) - a/3,
        ]
    else:
        return [d + e - a/3]

####################################################################################################

def _cubic_root(a, b, c, d):

    # https://en.wikipedia.org/wiki/Cubic_function

    # x, a, b, c, d = symbols('x a b c d')
    # solveset(x**3+b*x**2+c*x+d, x)

    # D0 = b**2 - 3*c
    # D1 = 2*b**3 - 9*b*c + 27*d
    # DD = D1**2 - 4*D0**3
    # C = ((D1 + sqrt(DD) /2)**(1/3)
    # - (b + C                      + D0/C                        ) /3
    # - (b + (-1/2 - sqrt(3)*I/2)*C + D0/((-1/2 - sqrt(3)*I/2)*C) ) /3
    # - (b + (-1/2 + sqrt(3)*I/2)*C + D0/((-1/2 + sqrt(3)*I/2)*C) ) /3

    # Fixme: divide by a ???

    D = 18*a*b*c*d - 4*b**3*d + b**2*c**2 - 4*a*c**3 - 27*a**2*d**2
    D0 = b**2 - 3*a*c

    if D == 0:
        if D0 == 0:
            return - b / (3*a) # triple root
        else:
            r1 = (9*a*d - b*c) / (2*D0) # double root
            r2 = (4*a*b*c - 9*a**2*d - b**3) / (a*D0) # simple root
            return r1, r2
    else:
        D1 = 2*b**3 - 9*a*b*c + 27*a**2*d
        # DD = - D / (27*a**2)
        DD = D1**2 - 4*D0**3

        # Fixme: need more info ...
        # can have 3 real roots, e.g. 3*x**3 - 25*x**2 + 27*x + 9

        # C1 = pow((D1 +- sqrt(DD))/2, 1/3)
        # r = - (b + C + D0/C) / (3*a)

        raise NotImplementedError
