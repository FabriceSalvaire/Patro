####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2017 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

"""This module implements a 2D geometry engine which implement standard `geometric primitives
<https://en.wikipedia.org/wiki/Geometric_primitive>`_ like line, conic and Bézier curve.

.. note:: This module is a candidate for a dedicated project.

Purpose
-------

The purpose of this module is to provide all the required algorithms in Python language for a 2D
geometry engine.  In particular it must avoid the use of a third-party libraries which could be over
sized for our purpose and challenging to trust.

It is not designed to provide optimised algorithms for a large number of graphic entities.  Such
optimisations could be provided in addition, in particular if the Python implementation has dramatic
performances.

Bibliographical References
--------------------------

All complex algorithms in this module should have strong references matching theses criteria by
preference order:

* a citation to an article from a well known peer reviewed journal,
* a citation to a reference book authored by a well known author,
* a well written article which can be easily trusted ( in this case an electronic copy of this
  article should be added to the repository).

However a Wikipedia article will usually not fulfils the criteria due to the weakness of this
collaborative encyclopedia: article quality, review process, content modification over time.

"""

####################################################################################################

from .Primitive import Primitive2DMixin
from .Vector import Vector2D

####################################################################################################

# Fixme: to fix cyclic import issue
Primitive2DMixin.__vector_cls__ = Vector2D
