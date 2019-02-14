.. include:: /abbreviation.txt

.. _introduction-geometry-ressources-page:

============================
 Introduction and Notations
============================

The text of this section is not written as an educational content but as a reference material for a
reader which has a some mathematical knowledge.

* :math:`\mathbf{u}` denotes a vector
* :math:`\widehat{\mathbf{u}}` denotes a unitary vector
* :math:`\mathbf{u}_i \mathbf{v}^i` uses the Einstein notation (or summation convention)
* dot (inner) product is denoted by :math:`\cdot`
* cross product is denoted by :math:`\times`
* :math:`\delta^{ij}` is the generalized Kronecker delta

   .. math::
       \delta_{ij} =
       \begin{cases}
           0 & \text{if } i \neq j, \\
           1 & \text{if } i = j.
       \end{cases}

* :math:`\varepsilon_{ijk}` is theLevi-Civita symbol

  In two dimensions, the Levi-Civita symbol is defined by:

  .. math::
      \varepsilon_{ij} =
      \begin{cases}
         +1       & \text{if } (i, j) = (1, 2) \\
         -1       & \text{if } (i, j) = (2, 1) \\
         \;\;\,0  & \text{if } i = j
     \end{cases}

  In three dimensions, the Levi-Civita symbol is defined by:

  .. math::
      \varepsilon_{ijk} =
      \begin{cases}
          +1      & \text{if } (i,j,k) \text{ is } (1,2,3), (2,3,1), \text{ or } (3,1,2), \\
          -1      & \text{if } (i,j,k) \text{ is } (3,2,1), (1,3,2), \text{ or } (2,1,3), \\
          \;\;\,0 & \text{if } i = j, \text{ or } j = k, \text{ or } k = i
     \end{cases}
