.. include:: ../../abbreviation.txt

.. _transformation-geometry-ressources-page:

=================
 Transformations
=================

Transformation matrices
-----------------------

To transform a vector, we multiply the vector with a transformation matrix

.. math::
     \begin{pmatrix} x' \\ y' \end{pmatrix} = \mathbf{T} \begin{pmatrix} x \\ y \end{pmatrix}

Usual transformation matrices in 2D are

.. math::
    \begin{align}
    \mathbf{Id} &= \begin{bmatrix}
      1 & 0 \\
      0 & 1
    \end{bmatrix} \\[1em]
    \mathbf{Scale}(s_x, s_y) &= \begin{bmatrix}
       s_x & 0 \\
       0   & s_y
    \end{bmatrix} \\[1em]
    \mathbf{Rotation}(\theta) &= \begin{bmatrix}
       \cos\theta & \sin\theta \\
      -\sin\theta & \cos\theta
    \end{bmatrix} \\[1em]
    \end{align}

For translation and affine transformation, we must introduce the concept of homogeneous coordinate
which add a virtual third dimension:

.. math::
    \mathbf{V} = \begin{bmatrix}
       x \\
       y \\
       1
    \end{bmatrix}

Then the translation and affine transformation matrix are expressed as:

.. math::
    \begin{align}
    \mathbf{Translation}(t_x, t_y) &= \begin{bmatrix}
       1 & 0 & t_x \\
       0 & 1 & t_y \\
       0 & 0 & 1
    \end{bmatrix} \\[1em]
    \mathbf{Generic} &= \begin{bmatrix}
       r_{11} & r_{12} & t_x \\
       r_{12} & r_{22} & t_y \\
       0 & 0 & 1
    \end{bmatrix}
    \end{align}

To compose transformations, we must multiply the transformations in this order:

.. math::
     \mathbf{T} = \mathbf{T_n} \ldots \mathbf{T_2} \mathbf{T_1}

Note the matrix multiplication is not commutative.
