.. include:: /abbreviation.txt

.. _design-note-question-answer-page:

==================================
 Design Notes Questions & Answers
==================================

Originally, Patro was a Python implementation of the Valentina pattern making software, which only
focus to implement the core engine and not the graphical user interface.

A pattern (in flat pattern design) is build from geometric operations which can be turned to a
computer program and is thus a field of applications of CAD (Computer Aided Design).  It corresponds
more precisely to parametric modelling with dedicated features to fashion modelling and
manufacturing.

What is my opinion on Valentina / Seamly2D ?
--------------------------------------------

Valentina project was started in 2013 by Roman Telezhinsky (Ukraine) as C++ developer and Susan
Spencer (USA) as community manager.  Susan previously developed an Inkscape Python plugin to
generate pattern, see http://www.taumeta.org.

In late 2017 (see http://libregraphicsworld.org/blog/entry/valentina-seamly2d), Susan and Roman
decided to fork the project in two separate projects.  Susan renamed the project to Seamly2D.  In
August 2018, `Valentina <https://valentinaproject.bitbucket.io>`_ is still but slowly developed by
Roman and `Seamly2D <https://github.com/FashionFreedom/Seamly2D>`_ looks like a dead project.  Roman
seems disconnected with the user community and Susan seems unable to do something excepted making
noises and complaining about Roman (cf. Seamly2D forum and a lot of nearly empty web site etc.).  In
summary, it could be Roman is not the perfect developer boy, but it coded a lot of lines of code and
released a free software parametric pattern making software.  Concerning Susan, many things are
unclear on their past relations, what she did / doing, what is her vision, on is ability to
communicate, manage and technical expertise.

Valentina is coded in C++ and use the Qt framework.  Qt is definitely the best choice for a GUI
actually.  Notice Valentina uses Qt4 Widgets and Scene Graph, thus it could require a costly upgrade
to Qt5 QML (which is a common upgrade issue).  The GUI of Valentina represents a huge cost, probably
the main part of Valentina.

Actually Valentina has some design flaws, which is usual for a young project developed with a few
budget.

For example, since Valentina is designed as a kind of WYSIWYG software, we cannot modify a pattern
to a temporally inconsistent state.  For example Valentina will not accept to have a line defined by
point that don't exist anymore.  For a computer program, your are free to save something which is
broken and fix things later.  However for a GUI parametric modeller this flexibility is more
challenging.  Software like Fusion 360 implements a cache for dangling objects.

Can we implement such a tool as a plugin of another software ?
--------------------------------------------------------------

`Inkscape <https://inkscape.org>`_ is a well known free software SVG editor which support Python
scripting and plugin.  However it is not designed for CAD purpose and not for professional use
actually.  This solution is thus flawed.

`FreeCAD <http://freecadweb.org>`_ is a free software 3D parametric modeller designed for CAD which
also support Python.  This solution could be an option, in particular to implement 3D features.
However a 3D CAD software is very complex and challenging, moreover it is not competitive with
professional software which are available for "free" in some conditions, thus this solution is
risky.

What is the requirements of a pattern drafting software ?
---------------------------------------------------------

The core functionality of a CAD system for pattern drafting consists of these two software components :

* an **open** file format to store and exchange the pattern,
* a geometric engine to compute the pattern, e.g. to generate the layout of each fabric's piece of a garment.

The XML language is a natural candidate to define an open file format to store and exchange the
pattern. Valentina uses XML to sore measurements in *.vit* files and patterns in *.val* files.

Another solution to define and store a pattern is to use a programming language, it can be a
dedicated language or any programming language with a dedicated API.  Many graphical languages was
invented for specific usages, e.g. PostScript for printer, Metafont and MetaPost for publishing,
G-code for machining etc.

Usually the geometric operations of a pattern are simple in comparison to the requirements of a
mechanical or electronic CAD software.  In first hand it is only 2D and the number of operations
should be handled smoothly by a computer of these days, whereas it is still challenging for other
domains.

.. A pattern drafting software only need a good geometric engine to be designed efficiently.

Finally, a pattern drafting software requires an efficient graphical user interface so as to be used
by fashion designers and not only by hackers.  This software component is more challenging in therms
of software engineering, i.e. in therms of design and cost.

Why Python is a good language for this library ?
------------------------------------------------

The Python language has a large audience in engineering, due to its canonical syntax and richness of
its ecosystem (scientific libraries).

Python is a high level language and thus more productive.

Python is used as scripting language to extend many softwares, in particular the famous open source
3D creation suite `Blender <https://www.blender.org>`_, the parametric 3D modeller `FreeCad
<http://freecadweb.org>`_ as well as the SVG editor `Inkscape <https://inkscape.org/>`_.  Moreover
the 3D human model generator `MakeHuman <http://www.makehuman.org>`_ is written in Python.

Python can be easily extended by C libraries using `CFFI <http://cffi.readthedocs.io/en/latest>`_
and C++ libraries using `SWIG <http://www.swig.org>`_.

Python as other dynamic languages is able to evaluate code on the fly which provide an expression
evaluator for free.  This feature is even more pertinent in our case because of the canonical
nature of the syntax of Python which is natural to somebody initiated to a basic mathematical
language level.

Could we implement a full software using Python ?
-------------------------------------------------

The answer is *yes we can!* since |Qt|_ has as an official binding and another excellent one,
|PyQt|_.

..  (if we consider Qt is superior to GTK and WxWidgets)

But up to now Python has of course some drawbacks!

Its main drawback is due to the fact the standard interpreter cannot execute more than one *Python
bytecode* thread at once, this limitation so called Global Interpreter Lock is required for
implementation simplicity.

..  in true parallelism (multi-core)
.. Consequently we can do multi-threading, even on multi-core in some cases, but less easily than in Java or Cxx11.

Despite a GUI implemented in PyQt is almost of the time more faster than the human perception on a
computer of these days.  It can be sometime difficult to overcome latency arising from the software
stack.  Thus yes we can do it, but it could requires some tricks to achieve the performance of a C++
application.

How to generate drawings in standard format like PDF or SVG ?
-------------------------------------------------------------

SVG is not difficult to generate from Python since it is based on XML.  However the PDF format is
more challenging, for efficiency reason PDF is a binary format and is thus much more complicated
than PostScript which is a true programming language.

There is several possibilities to generate PDF.

The most disturbing one is to use the `LaTeX <https://en.wikipedia.org/wiki/LaTeX>`_ publishing
system in combination with the `PGF <http://www.texample.net/tikz/examples>`_ package which provide
an amazing graphical language on top of LaTeX.  This solution could terrify many peoples, but it do
the job very well for text and graphics.  However user must install a LaTeX environment from their
Linux distribution or using the `TexLive <https://www.tug.org/texlive>`_ distribution.

A more conventional solution requires a library that can generate PDF from standard graphical
operations.  Some libraries featuring that are :

* |Reportlab|_  open-source PDF Toolkit (more commercial and less known)
* Qt using QPainter API, Valentina solution, see https://wiki.qt.io/Handling_PDF
* `Cairo <https://www.cairographics.org/manual/cairo-PDF-Surfaces.html>`_
* |Matplotlib|_ (but more oriented to plot)
* and ???

What is the requirements of a geometric engine ?
------------------------------------------------

The requirements for a geometric engine are :

* Must support 2D, but 3D is not required
* Must handle smoothly a low complexity graphic scene, i.e. a pattern will never contains thousands of graphical entities like in mechanic or electronic PCB
* Required precision is low : a millimetre unit with one digit of precision is enough for pattern
  accuracy.  However we need more digits for computing so as to don't accumulate errors and for
  computer display so as to zoom correctly the pattern (e.g. 3 digits to zoom up to 100x).
* Is exact numerical computation useful in our case ? cf. Computational Geometry Algorithms Library (CGAL)
* We could support symbolic computation, excepted when a computation is only numerical.
