.. include:: /abbreviation.txt

.. _svg-ressources-page:

=================
 SVG File Format
=================

Reference Documentations
------------------------

* `Scalable Vector Graphics (SVG) W3C Home Page <https://www.w3.org/Graphics/SVG>`_
* `An SVG Primer for Today's Browsers W3C Working Draft — September 2010 <https://www.w3.org/Graphics/SVG/IG/resources/svgprimer.html>`_
* `Scalable Vector Graphics (SVG) 1.1 (Second Edition) W3C Recommendation 16 August 2011 <https://www.w3.org/TR/SVG11/>`_
* `Mozilla SVG Documentation <https://developer.mozilla.org/en-US/docs/Web/SVG>`_

SVG Coordinate System
---------------------

SVG uses the screen coordinate system where the X axis points towards the right direction and the Y
axis points towards the bottom direction, thus the origin is at the upper left-hand corner of the
drawing frame.

Inkscape Software
-----------------

Inkscape can save a SVG file in several ways:

* simple: the file will only contains pure SVG
* Inkscape: the file will contains Inkscape extension
* optimised: perform some optimisations on the output
* compressed: file is compressed using the zip algorithm

**Notes on how Inkscape generates SVG**:

* As opposite to the SVG Specification, Inkscape set the origin at the bottom of the document, thus

    :math:`\mathbf{Y}_{\mathrm{Inkscape}} = \mathbf{Page\ Height} - \mathbf{Y}_{\mathrm{SVG}}`

    The transformation is a composition of a Y axis parity and a translation on the Y axis of the page height.

    See also https://bugs.launchpad.net/inkscape/+bug/170049

* It uses a *group* as top layer and a *transform*
* It uses a mix of absolute and incremental coordinates
* **It spoils in several ways the object's coordinates**: values are transformed and rounded.
   Thus **Inkscape should not be be used to make or edit a file which require accurate coordinates.**

Inkscape SVG example
~~~~~~~~~~~~~~~~~~~~

This example uses a margin of 20 and paint

* an horizontal line of length 100 from the origin (20, 20)
* a vertical line of length 100 from the origin
* a 45° line of length 80 from the origin
* the viewport is (0, 0, 140, 140)

**Note: this extract is incomplete**

.. code-block:: text

    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg width="140.00003mm" height="141mm" viewBox="0 0 140.00003 141">
      <g id="layer1" transform="translate(2.037847e-4,-156)">
        <path id="path-x"  d="m 19.999999,276.73109 99.999651,0.13765" />
        <path id="path-y"  d="M 20.145247,277 V 177" />
        <path id="path-45" d="m 20.084712,276.91488 79.830575,-79.8386" />
      </g>
    </svg>

This SVG file must be interpreted as follow

* Draw a line from (20, 276-156) to +(100, 0) (note: l is deduced from m),

    which gives (20, 120) to (120, 120),

    and in Inkscape coordinates (20, 20) to (120, 20) since 140 - 120 = 20

* Draw a line from (20, 276-156) to (20, 176-156),

    which gives (20, 120) to (20, 20),

    and in Inkscape coordinates (20, 20) to (20, 120)

* Draw a line from (20, 276-156) to +(80, -80),

    which gives (20, 120) to (100, 40),

  and in Inkscape coordinates (20, 20) to (100, 100)
