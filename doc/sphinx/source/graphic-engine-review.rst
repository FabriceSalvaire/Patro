.. include:: project-links.txt
.. include:: abbreviation.txt

.. _graphic-engine-review-page:

=======================
 Graphic Engine Review
=======================

Common Features
---------------

* transformation: reflect, slant
* clipping path
* path
* pen: invisible, hex
* arrow tips
* marker
* label

Tikz
----

* circle on path
* sin parabola path
* filling: shading
* scope : style, transformation
* label : anchor, alignment, position on path
* pen

  * line width : ultra thin, very thin, thin, semithick, thick, very thick, ultra thick
  * line cape / join
  * dash pattern
  * double line
* node : edge, anchor, shape

Asymptote
---------

http://asymptote.sourceforge.net

Examples::

    draw((0,0)--(100,100));
    draw((0,0)--(2,1),Arrow);
    draw((0,0)--(1,0)--(1,1)--(0,1)--cycle);
    label("$A$",(0,0),SW);

DPic
----

