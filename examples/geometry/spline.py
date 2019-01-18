####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
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

from Patro.GeometryEngine.Spline import BSpline2D
from Patro.GeometryEngine.Vector import Vector2D

import numpy as np
import matplotlib.pyplot as plt

####################################################################################################

def plot_spline(spline, control=True, deboor=True, naive=False, offset=0):

    # for k in range(spline.order):
    #     for i in range(spline.degree-k, spline.order):
    #         print(i, k)
    #         axes.plot(ts, [spline.basis_function(i, k, t) for t in ts])

    offset = np.array((0, offset))

    if control:
        control_point_array = spline.point_array + offset
        axes.plot(control_point_array[:,0], control_point_array[:,1])

    if naive:
        knots = spline.knots
        print(knots)
        # for t_inf in spline.knot_iter:
        #     ts = np.linspace(t_inf, t_inf +1, 30)
        for i in range(len(spline.knots) -1):
            t_inf, t_sup = spline.knots[i], spline.knots[i+1]
            if t_sup == spline.end_knot:
                t_sup -= 1e-6
            ts = np.linspace(t_inf, t_sup, 30)
            if t_inf < t_sup:
                curve_points = np.zeros((len(ts), 2))
                for i, t in enumerate(ts):
                    p = spline.point_at_t(t, naive=True)
                    curve_points[i] = p
                curve_points += offset
                axes.plot(curve_points[:,0], curve_points[:,1])

    if deboor:
        end_knot = spline.end_knot
        if not spline.uniform:
            end_knot -= 1e-6
        print('end knot', spline.uniform, end_knot)
        ts = np.linspace(0, end_knot, 50)
        curve_points = np.zeros((len(ts), 2))
        for i, t in enumerate(ts):
            p = spline.point_at_t(t)
            curve_points[i] = p
        curve_points += offset
        axes.plot(curve_points[:,0], curve_points[:,1], 'o')

####################################################################################################

# degree = 3
# order = degree +1
# for number_of_points in range(order, order + 5):
#     print(BSpline2D.uniform_knots(degree, number_of_points))

# points = (
#     Vector2D(1, 1),
#     Vector2D(2, 2),
#     Vector2D(3, 2),
#     Vector2D(4, 1),
# )
# degree = 3
# spline = BSpline2D(points, degree)
# plot_spline(spline)

points = (
    Vector2D(0, 0),
    Vector2D(5, 5),
    Vector2D(10, -5),
    Vector2D(15, 5),
    Vector2D(20, -5),
    Vector2D(25, 5),
)
degree = 3
spline = BSpline2D(points, degree)

# spline2 = spline
# spline2 = spline2.insert_knot(1.5)
# spline2 = spline2.insert_knot(2.5)

spline2 = spline.to_bezier_form()
bezier_curves = spline.to_bezier()
print(bezier_curves)

figure, axes = plt.subplots()
axes.grid(True)
plot_spline(spline, deboor=True, naive=True, offset=-.1)
plot_spline(spline2, deboor=True, naive=True, offset=.1)
plt.show()
