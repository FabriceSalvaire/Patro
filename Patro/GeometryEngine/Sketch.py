####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2022 Fabrice Salvaire
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

"""Module to implement a sketch.

"""

####################################################################################################

__all__ = ['Sketch', 'Distance']

####################################################################################################

from .Line import Line2D
from .Segment import Segment2D
from .Vector import Vector2D

####################################################################################################

def Distance(vector1: Vector2D, vector2: Vector2D) -> float:
    return (vector2 - vector1).magnitude

####################################################################################################

class SketchPrimitive:

    ##############################################

    # None
    def __init__(self, sketch: 'Sketch', name: str, description: str) -> None:
        self._sketch = sketch
        self._sketch._add_primitive(self)
        self._name = name
        self._description = description

    ##############################################

    @property
    def sketch(self) -> 'Sketch':
        return self._sketch

    # @sketch.setter
    # def sketch(self, value):
    #     self._sketch = value

    ##############################################

    @property
    def name(self) -> str:
        return self._name

    # @name.setter
    # def name(self, value):
    #     self._name = value

    ##############################################

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

####################################################################################################

class SketchPoint(SketchPrimitive):

    ##############################################

    def __init__(self, sketch: 'Sketch', vector: Vector2D, **kgwars) -> None:
        super().__init__(**kgwars)
        self.p = vector
        # Fixme:
        self._on = kgwars.get('on', None)

####################################################################################################

class SketchLine:

    ##############################################

    def __init__(self, point: Vector2D=None, vector: Vector2D=None, **kgwars) -> None:
        super().__init__(**kgwars)
        if 'line' in kwargs:
            self.p = line
        elif point is not None and vector is not None:
            self.p = Line2D(point, vector)
        else:
            ValueError()
        self._trim_before = None
        self._trim_after = None

    ##############################################

    def trim(self, at: SketchPoint, distance: float) -> None:
        pass

    ##############################################

    def point(self, distance: float=None, at: SketchPoint=None) -> SketchPoint:
        line = self.p
        if distance is None and at is None:
            p = line.p
        else:
            if at is None:
                at = line.p
            else:
                at = at.p
            p = line.point_at_distance(distance, at)
        return SketchPoint(self.sketch, p, on=self)

    ##############################################

    def parallel(self, at: SketchPoint, from_: 'SketchLine', to: 'SketchLine') -> 'SketchLine':
        pline = self.p.parallel_line_at(at.p)
        pline = SketchLine(line=pline)
        if to is not None:
            p_to = pline.intersection(to)
        if from_ is not None:
            p_from = pline.intersection(from_)
        if from_ is None and to is None:
            return pline
        if from_ is not None:
            return p_to, pline
        elif to is None:
            return p_from, pline
        else:
            return p_from, p_to, pline

    ##############################################

    def perpendicular(self, at: SketchLine, distance: float, direction: bool) -> SketchLine:
        # Fixme:
        pline = self.p.orthogonal_line_at(at.p)
        p = pline.point_at_distance(distance)
        return p, pline

####################################################################################################

class SketchSegment:

    ##############################################

    def __init__(self, point1: Vector2D, point2: Vector2D, **kgwars) -> None:
        super().__init__(**kgwars)
        self.p = Segment2D(point1, point2)

####################################################################################################

class Sketch:

    """Class to implement 2D sketch."""

    ##############################################

    def __init__(self, title: str, measurements: None) -> None:
        self._primitives = []
        self._title = title

    ##############################################

        @property
        def title(self):
            return self._title

        @title.setter
        def title(self, value):
            self._title = value

    ##############################################

    @property
    def origin(self) -> Vector2D:
        return Vector2D(0, 0)

    ##############################################

    def _add_primitive(self, obj: SketchPrimitive) -> None:
        self._primitives.append(obj)

    ##############################################

    def point(self, x: float, y: float, **kgwars: dict) -> SketchPoint:
        v = Vector2D(x, y)
        return SketchPoint(self, v, **kgwars)

    ##############################################

    def middle(self, point1: SketchPoint, point2: SketchPoint, **kgwars: dict) -> SketchPoint:
        v = Vector2D.middle(point1.p, point2.p)
        return SketchPoint(self, v, **kgwars)

    ##############################################

    def line(self, at: Vector2D, vector: Vector2D, **kgwars: dict) -> SketchLine:
        # trim_before
        if at is None:
            at = self.origin
        return SketchLine(self, at, vector, **kgwars)

    ##############################################

    def hline(self, at: Vector2D, **kgwars: dict) -> SketchLine:
        v = Vector2D(1, 0)
        return self.line(at, v, **kgwars)

    def vline(self, at: Vector2D, **kgwars: dict) -> SketchLine:
        v = Vector2D(0, 1)
        return self.line(at, v, **kgwars)

    ##############################################

    def segment(self, point1: SketchPoint, point2: SketchPoint, **kgwars: dict) -> SketchSegment:
        return SketchSegment(self, point1, point2, **kgwars)

    ##############################################

    def constrained_point(self, **kgwars: dict) -> SketchPoint:
        # from_
        # on
        # distance
        # direction
        from_ = kgwars['from_']
        on = kgwars['on']
        distance = kgwars['distance']
        direction = kgwars['direction']
        line = on.p
        reverse = True if line.v.dot((direction.p.v - line.p)) < 0 else False
        return on.triangle_projected_point(from_, distance, reverse=False)
