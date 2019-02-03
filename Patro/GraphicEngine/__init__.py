####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Fabrice Salvaire
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

"""This module implements a 2D graphic engine as a scene rendered by a painter class.

A scene contains graphic items like text, image line, circle and Bézier curve.  A painter class is
responsible to render the scene on the screen or a graphic file format.

These painters are available for screen rendering:

* Matplotlib : :mod:`Patro.GraphicEngine.Painter.MplPainter`
* Qt         : :mod:`Patro.GraphicEngine.Painter.QtPainter`

These painters are available for graphic file format:

* DXF   : :mod:`Patro.GraphicEngine.Painter.DxfPainter`
* LaTeX : :mod:`Patro.GraphicEngine.Painter.TexPainter`
* PDF   : :mod:`Patro.GraphicEngine.Painter.PdfPainter`
* SVG   : :mod:`Patro.GraphicEngine.Painter.SvgPainter`

"""
