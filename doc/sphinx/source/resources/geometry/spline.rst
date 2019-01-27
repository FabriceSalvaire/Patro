.. include:: ../../abbreviation.txt

.. _spline-geometry-ressources-page:

===============
 Spline Curves
===============

B-spline Basis
--------------

A nonuniform, nonrational B-spline of order `k` is a piecewise polynomial function of degree
:math:`k - 1` in a variable `t`.

.. check: k+1 knots ???

.. It is defined over :math:`k + 1` locations :math:`t_i`, called knots, which must be in
   non-descending order :math:`t_i \leq t_{i+1}`. This series defines a knot vector :math:`T = (t_0,
   \ldots, t_{k})`.

A set of non-descending breaking points, called knot, :math:`t_0 \le t_1 \le \ldots \le t_m` defines
a knot vector :math:`T = (t_0, \ldots, t_{m})`.

If each knot is separated by the same distance `h` (where :math:`h = t_{i+1} - t_i`) from its
predecessor, the knot vector and the corresponding B-splines are called "uniform".

Given a knot vector `T`, the associated B-spline basis functions, :math:`B_i^k(t)` are defined as:

.. t \in [t_i, t_{i+1}[

.. math::
    B_i^1(t) =
    \left\lbrace
    \begin{array}{l}
       1 \;\textrm{if}\; t_i \le t < t_{i+1} \\
       0 \;\textrm{otherwise}
    \end{array}
    \right.

.. math::
   \begin{split}
    B_i^k(t) &= \frac{t - t_i}{t_{i+k-1} - t_i} B_i^{k-1}(t)
              + \frac{t_{i+k} - t}{t_{i+k} - t_{i+1}} B_{i+1}^{k-1}(t) \\
             &= w_i^{k-1}(t) B_i^{k-1}(t) + [1 - w_{i+1}^{k-1}(t)] B_{i+1}^{k-1}(t)
   \end{split}

where

.. math::
    w_i^k(t) =
    \left\lbrace
    \begin{array}{l}
       \frac{t - t_i}{t_{i+k} - t_i} \;\textrm{if}\; t_i < t_{i+k} \\
       0 \;\textrm{otherwise}
    \end{array}
    \right.

These equations have the following properties, for :math:`k > 1` and :math:`i = 0, 1, \ldots, n` :

* Positivity: :math:`B_i^k(t) > 0`, for :math:`t_i < t < t_{i+k}`
* Local Support: :math:`B_i^k(t) = 0`, for :math:`t_0 \le t \le t_i` and :math:`t_{i+k} \le t \le t_{n+k}`
* Partition of unity: :math:`\sum_{i=0}^n B_i^k(t)= 1`, for :math:`t \in [t_0, t_m]`
* Continuity: :math:`B_i^k(t)` as :math:`C^{k-2}` continuity at each simple knot

.. The B-spline contributes only in the range between the first and last of these knots and is zero
   elsewhere.

B-spline Curve
--------------

A B-spline curve of order `k` is defined as a linear combination of control points :math:`p_i` and
B-spline basis functions :math:`B_i^k(t)` given by

.. math::
    S^k(t) = \sum_{i=0}^{n} p_i\; B_i^k(t) ,\quad n \ge k - 1,\; t \in [t_{k-1}, t_{n+1}]

In this context the control points are called De Boor points. The basis functions :math:`B_i^k(t)`
is defined on a knot vector

.. math::
    T = (t_0, t_1, \ldots, t_{k-1}, t_k, t_{k+1}, \ldots, t_{n-1}, t_n, t_{n+1}, \ldots, t_{n+k})

where there are :math:`n+k+1` elements, i.e. the number of control points :math:`n+1` plus the order
of the curve `k`.  Each knot span :math:`t_i \le t \le t_{i+1}` is mapped onto a polynomial curve
between two successive joints :math:`S(t_i)` and :math:`S(t_{i+1})`.

Unlike Bézier curves, B-spline curves do not in general pass through the two end control points.
Increasing the multiplicity of a knot reduces the continuity of the curve at that knot.
Specifically, the curve is :math:`(k-p-1)` times continuously differentiable at a knot with
multiplicity :math:`p (\le k)`, and thus has :math:`C^{k-p-1}` continuity.  Therefore, the control
polygon will coincide with the curve at a knot of multiplicity :math:`k-1`, and a knot with
multiplicity `k` indicates :math:`C^{-1}` continuity, or a discontinuous curve.  Repeating the knots
at the end `k` times will force the endpoints to coincide with the control polygon.  Thus the first
and the last control points of a curve with a knot vector described by

.. math::
    \begin{eqnarray}
    T = (
    \underbrace{t_0, t_1, \ldots, t_{k-1},}_{\mbox{$k$ equal knots}}
    \quad
    \underbrace{t_k, t_{k+1}, \ldots, t_{n-1}, t_n,}_{\mbox{$n$-$k$+1 internal knots}}
    \quad
    \underbrace{t_{n+1}, \ldots, t_{n+k}}_{\mbox{$k$ equal knots}})
    \end{eqnarray}

coincide with the endpoints of the curve.  Such knot vectors and curves are known as *clamped*. In
other words, *clamped/unclamped* refers to whether both ends of the knot vector have multiplicity
equal to `k` or not.

**Local support property**: A single span of a B-spline curve is controlled only by `k` control
points, and any control point affects `k` spans.  Specifically, changing :math:`p_i` affects the
curve in the parameter range :math:`t_i < t < t_{i+k}` and the curve at a point where :math:`t_r < t
< t_{r+1}` is determined completely by the control points :math:`p_{r-(k-1)}, \ldots, p_r`.

**B-spline to Bézier property**: From the discussion of end points geometric property, it can be
seen that a Bézier curve of order `k` (degree :math:`k-1`) is a B-spline curve with no internal
knots and the end knots repeated `k` times.  The knot vector is thus

.. math::
 \begin{eqnarray}
    T = (
    \underbrace{t_0, t_1, \ldots, t_{k-1}}_{\mbox{$k$ equal knots}}
    ,\quad
    \underbrace{t_{n+1}, \ldots, t_{n+k}}_{\mbox{$k$ equal knots}}
    )
    \end{eqnarray}

where :math:`n+k+1 = 2k` or :math:`n = k-1`.

Algorithms for B-spline curves
------------------------------

Evaluation and subdivision algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A B-spline curve can be evaluated at a specific parameter value `t` using the de Boor algorithm,
which is a generalization of the de Casteljau algorithm.  The repeated substitution of the recursive
definition of the B-spline basis function into the previous definition and re-indexing leads to the
following de Boor algorithm:

..  math::
   S(t) = \sum_{i=0}^{n+j} p_i^j B_i^{k-j}(t) ,\quad j = 0, 1, \ldots, k-1

where

.. math::
   p_i^j = \Big[1 - w_i^j\Big] p_{i-1}^{j-1} + w_i^j p_i^{j-1}, \; j > 0

with

.. math::

  w_i^j = \frac{t - t_i}{t_{i+k-j} - t_i} \quad \textrm{and} \; p_j^0 = p_j

For :math:`j = k-1`, the B-spline basis function reduces to :math:`B_l^1` for :math:`t \in [t_l,
t_{l+1}]`, and :math:`p_l^{k-1}` coincides with the curve :math:`S(t) = p_l^{k-1}`.

The de Boor algorithm is a generalization of the de Casteljau algorithm. The de Boor algorithm also
permits the subdivision of the B-spline curve into two segments of the same order.

De Boor Algorithm
~~~~~~~~~~~~~~~~~

Let the index `l` define the knot interval that contains the position, :math:`t \in [t_l ,
t_{l+1}]`.  We can see in the recursion formula that only B-splines with :math:`i = l-K, \dots, l`
are non-zero for this knot interval, where :math:`K = k - 1` is the degree.  Thus, the sum is
reduced to:

.. math::
    S^k(t) = \sum _{i=l-K}^{l} p_{i} B_i^k(t)

The algorithm does not compute the B-spline functions :math:`B_i^k(t)` directly.  Instead it
evaluates :math:`S(t)` through an equivalent recursion formula.

Let :math:`d _i^r` be new control points with :math:`d_i^1 = p_i` for :math:`i = l-K, \dots, l`.

For :math:`r = 2, \dots, k` the following recursion is applied:

.. math::
    d_i^r = (1 - w_i^r) d_{i-1}^{r-1} + w_i^r d_i^{r-1} \quad i = l-K+r, \dots, l

    w_i^r = \frac{t - t_i}{t_{i+1+l-r} - t_{i}}

Once the iterations are complete, we have :math:`S^k(t) = d_l^k`.

.. , meaning that :math:`d_l^k` is the desired result.

De Boor's algorithm is more efficient than an explicit calculation of B-splines :math:`B_i^k(t)`
with the Cox-de Boor recursion formula, because it does not compute terms which are guaranteed to be
multiplied by zero.

..
    :math:`S(t) = p_j^k` for :math:`t \in [t_j , t_{j+1}[` for :math:`k \le j \le n` with the following relation:
    .. math::
        \begin{split}
        p_i^{r+1} &= \frac{t - t_i}{t_{i+k-r} - t} p_i^r + \frac{t_{i+k-r} - t_i}{t_{i+k-r} - t_i} p_{i-1}^r \\
                  &= w_i^{k-r}(t) p_i^r +  (1 - w_i^{k-r}(t)) p_{i-1}^r
        \end{split}

Knot insertion
~~~~~~~~~~~~~~

A knot can be inserted into a B-spline curve without changing the
geometry of the curve.  The new curve is identical to

.. math::
    \begin{array}{lcl}
    \sum_{i=0}^n p_i B_i^k(t) & \textrm{becomes} & \sum_{i=0}^{n+1} \bar{p}_i \bar B_i^k(t) \\
    \mbox{over}\; T = (t_0, t_1, \ldots, t_l, t_{l+1}, \ldots) & &
    \mbox{over}\; T = (t_0, t_1, \ldots, t_l, \bar t, t_{l+1}, \ldots) & &
    \end{array}

when a new knot :math:`\bar t` is inserted between knots :math:`t_l` and :math:`t_{l+1}`.  The new
de Boor points are given by

.. math::
    \bar{p}_i = (1 - w_i) p_{i-1} + w_i p_i

where

.. math::
    w_i =
    \left\{ \begin{array}{ll}
    1 & i \le l-k+1 \\
    0 & i \ge l+1 \\
    \frac{\bar{t} - t_i}{t_{l+k-1} - t_i} & l-k+2 \le i \leq l
    \end{array}
    \right.

The above algorithm is also known as **Boehm's algorithm**.  A more general (but also more complex)
insertion algorithm permitting insertion of several (possibly multiple) knots into a B-spline knot
vector, known as the Oslo algorithm, was developed by Cohen et al.

A B-spline curve is :math:`C^{\infty}` continuous in the interior of a span.  Within exact
arithmetic, inserting a knot does not change the curve, so it does not change the continuity.
However, if any of the control points are moved after knot insertion, the continuity at the knot
will become :math:`C^{k-p-1}`, where `p` is the multiplicity of the knot.

The B-spline curve can be subdivided into Bézier segments by knot insertion at each internal knot
until the multiplicity of each internal knot is equal to `k`.

References
----------

* Computer Graphics, Principle and Practice, Foley et al., Adison Wesley
* http://web.mit.edu/hyperbook/Patrikalakis-Maekawa-Cho/node15.html
