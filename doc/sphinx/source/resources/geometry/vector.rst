.. include:: /abbreviation.txt

.. _vector-geometry-ressources-page:

========
 Vector
========

Dot and Cross Product
=====================

The dot product is defined by the formula

.. math::
   \mathbf{u} \cdot  \mathbf{v} = \|\mathbf{u}\| \  \|\mathbf{v}\| \cos(\theta) = \mathbf{u}_i \mathbf{v}^i

The cross product is defined by the formula

.. math::
   \mathbf{u} \times \mathbf{v} = \|\mathbf{u}\| \  \|\mathbf{v}\| \sin(\theta) \mathbf{n} = \varepsilon^i{}_{jk} \mathbf{u}^j \mathbf{v}^k \mathbf{e}_i

where :math:`\mathbf{n}` is a unit vector perpendicular to the plane containing :math:`\mathbf{u}`
and :math:`\mathbf{u}` in the direction given by the right-hand rule.

where :math:`\varepsilon^i{}_{jk} = \delta^{il} \varepsilon_{ljk}`, :math:`\varepsilon_{ljk}` is the
Levi-Civita symbol, and :math:`\delta^{il}` is the generalized Kronecker delta.

The projection and the deviation of a vector to a directional vector is

.. math::
   \begin{align}
   \mathrm{projection} &= \mathbf{u} \cdot \frac{\mathbf{d}}{\|d\|} = \mathbf{u} \cdot \widehat{\mathbf{d}} \\[.5em]
   \mathrm{deviation}  &= \mathbf{u} \times \frac{\mathbf{d}}{\|d\|} = \mathbf{u} \times \widehat{\mathbf{d}}
   \end{align}

where the projection is the length of the adjacent side of the right triangle made by the two
vectors, the deviation is the length of the opposite side, respectively.  The length of
:math:`\mathbf{u}` is the hypotenuse.
