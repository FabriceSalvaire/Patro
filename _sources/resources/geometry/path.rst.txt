.. include:: /abbreviation.txt

.. _path-geometry-ressources-page:

======
 Path
======

Bulge
-----

Let :math:`\mathbf{P}_0`, :math:`\mathbf{P}_1`, :math:`\mathbf{P}_2` the vertices and :math:`R` the
bulge radius.

The deflection :math:`\theta = 2 \alpha` at the corner is

.. math::
   \mathbf{D}_1 \cdot \mathbf{D}_0 = (\mathbf{P}_2 - \mathbf{P}_1) \cdot (\mathbf{P}_1 - \mathbf{P}_0) = \cos(\pi - \theta)

The bisector direction is

.. math::
   \mathbf{Bis} = \mathbf{D}_1 - \mathbf{D}_0 = (\mathbf{P}_2 - \mathbf{P}_1) - (\mathbf{P}_1 - \mathbf{P}_0) = \mathbf{P}_2 -2 \mathbf{P}_1 + \mathbf{P}_0

Bulge Center is

.. math::
    \mathbf{C} = \mathbf{P}_1 + \frac{R}{\sin \alpha} \mathbf{Bis}

Extremities are

.. math::
    \begin{align}
    \mathbf{P}_1' &= \mathbf{P}_1 - \frac{R}{\tan \alpha} \mathbf{D}_0 \\
    \mathbf{P}_1'' &= \mathbf{P}_1 +  \frac{R}{\tan \alpha} \mathbf{D}_1
    \end{align}
