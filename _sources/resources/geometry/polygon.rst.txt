.. include:: /abbreviation.txt

.. _polygon-geometry-ressources-page:

=========
 Polygon
=========

Area and Barycenter
-------------------

Polygon area is determined by

.. math::
    \begin{align}
     \mathbf{A} &= \frac{1}{2} \sum_{i=0}^{n-1} P_i \otimes P_{i+1} \\
                &= \frac{1}{2} \sum_{i=0}^{n-1}
                \begin{vmatrix}
                 x_i & x_{i+1} \\
                 y_i & y_{i+1}
                \end{vmatrix} \\
                &= \frac{1}{2} \sum_{i=0}^{n-1} x_i y_{i+1} - x_{i+1} y_i
    \end{align}

where :math:`x_n = x_0`

Polygon barycenter is determined by

.. math::
    \begin{align}
    \mathbf{C} &= \frac{1}{6\mathbf{A}} \sum_{i=0}^{n-1}
                  (P_i + P_{i+1}) \times (P_i \otimes P_{i+1}) \\
               &= \frac{1}{6\mathbf{A}} \sum_{i=0}^{n-1}
                  \begin{pmatrix}
                      (x_i + x_{i+1}) (x_i y_{i+1} - x_{i+1} y_i) \\
                      (y_i + y_{i+1}) (x_i y_{i+1} - x_{i+1} y_i)
                  \end{pmatrix}
    \end{align}

References

  * On the Calculation of Arbitrary Moments of Polygons,
    Carsten Steger,
    Technical Report FGBV–96–05,
    October 1996
  * http://mathworld.wolfram.com/PolygonArea.html
  * https://en.wikipedia.org/wiki/Polygon#Area_and_centroid

Moments of Inertia
------------------

.. warning:: untrusted formulae

.. math::
     \begin{align}
     I_x    &= \frac{1}{12} \sum (y_i^2 + y_i y_{i+1} + y_{i+1}^2) (x_i y_{i+1} - x_{i+1} y_i) \\
     I_y    &= \frac{1}{12} \sum (x_i^2 + x_i x_{i+1} + x_{i+1}^2) (x_i y_{i+1} - x_{i+1} y_i) \\
     I_{xy} &= \frac{1}{24} \sum (x_i y_{i+1} + 2 x_i y_i + 2 x_{i+1} y_{i+1} + x_{i+1} y_i) (x_i y_{i+1} - x_{i+1} y_i)
     \end{align}

Reference

  * https://en.wikipedia.org/wiki/Second_moment_of_area#Any_cross_section_defined_as_polygon
