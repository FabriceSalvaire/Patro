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

"""This modules implements the `SVG <https://www.w3.org/Graphics/SVG>`_ file format.

References:

* `SVG 1.1 (Second Edition) W3C Recommendation 16 August 2011 <https://www.w3.org/TR/SVG11>`_

"""

####################################################################################################

__all__ = [
    'Svg',
    'Anchor',
    'AltGlyph',
    'AltGlyphDef',
    'AltGlyphItem',
    'Animate',
    'AnimateMotion',
    'AnimateTransform',
    'Circle',
    'ClipPath',
    'ColorProfile',
    'Cursor',
    'Defs',
    'Desc',
    'Ellipse',
    'FeBlend',
    'Group',
    'Image',
    'Line',
    'LinearGradient',
    'Marker',
    'Mask',
    'Path',
    'Pattern',
    'Polyline',
    'Polygon',
    'RadialGradient',
    'Rect',
    'Stop',
    'Text',
    'TextRef',
    'TextSpan',
    'Use',
    ]

####################################################################################################

import logging

from Patro.Common.Xml.Objectivity import (
    # BoolAttribute,
    IntAttribute, FloatAttribute,
    FloatListAttribute,
    StringAttribute,
    XmlObjectAdaptator,
    TextXmlObjectAdaptator,
)

# Fixme: should we mix SVG format and ... ???
from Patro.GeometryEngine.Path import Path2D
from Patro.GeometryEngine.Transformation import AffineTransformation2D
from Patro.GeometryEngine.Vector import Vector2D

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def split_space_list(value):
    return [x for x in value.split(' ') if x]

####################################################################################################
#
# Conditional Processing Attributes
#   requiredFeatures
#   requiredExtensions
#   systemLanguage
#
####################################################################################################

####################################################################################################
#
# Core Attribute
#   id
#   xml:base
#   xml:lang
#   xml:space
#
####################################################################################################

class IdMixin:

    """Core attribute"""

    __attributes__ = (
        StringAttribute('id'),
    )

####################################################################################################
#
# Graphical Event Attributes
#   onactivate
#   onclick
#   onfocusin
#   onfocusout
#   onload
#   onmousedown
#   onmousemove
#   onmouseout
#   onmouseover
#   onmouseup
#
####################################################################################################

####################################################################################################

class PresentationAttributes:

    # https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute

    # Fixme: type !!!

    alignment_baseline = None # check
    baseline_shift = None # check
    clip = None # check
    clip_path = None # check
    clip_rule = None # check
    color = None # check
    color_interpolation = None # check
    color_interpolation_filters = None # check
    color_profile = None # check
    color_rendering = None # check
    cursor = None # check
    direction = None # check
    display = None # check
    dominant_baseline = None # check
    enable_background = None # check
    fill = None
    fill_opacity = 1
    fill_rule = 'nonzero'
    #! filter = None # check
    flood_color = None # check
    flood_opacity = None # check
    font_family = None # check
    font_size = None # check
    font_size_adjust = None # check
    font_stretch = None # check
    font_style = None # check
    font_variant = None # check
    font_weight = None # check
    glyph_orientation_horizontal = None # check
    glyph_orientation_vertical = None # check
    image_rendering = None # check
    kerning = None # check
    letter_spacing = None # check
    lighting_color = None # check
    marker_end = None # check
    marker_mid = None # check
    marker_start = None # check
    mask = None # check
    opacity = 1
    overflow = None # check
    paint_order = None
    pointer_events = None # check
    shape_rendering = None # check
    stop_color = None # check
    stop_opacity = None # check
    stroke = None
    stroke_dasharray = None # check
    stroke_dashoffset = None # check
    stroke_linecap = 'butt'
    stroke_linejoin = 'miter'
    stroke_miterlimit = 4
    stroke_opacity = 1
    stroke_width = 1 # px
    style = None
    text_anchor = None # check
    text_decoration = None # check
    text_rendering = None # check
    transform = AffineTransformation2D.Identity()
    unicode_bidi = None # check
    vector_effect = None
    visibility = None # check
    word_spacing = None # check
    writing_mode = None # check

####################################################################################################

class InheritAttribute(StringAttribute):

    ##############################################

    @classmethod
    def from_xml(cls, value):
        if value == 'inherit':
            return value
        else:
            return cls._from_xml(value)

    ##############################################

    @classmethod
    def _from_xml(cls, value):
        raise NotImplementedError

####################################################################################################

class NumberAttribute(InheritAttribute):
    @classmethod
    def _from_xml(cls, value):
        return float(value)

####################################################################################################

class PercentValue:

    ##############################################

    def __init__(self, value):
        self._value = float(value) / 100

    ##############################################

    def __float__(self):
        return self._value

####################################################################################################

class UnitValue:

    ##############################################

    def __init__(self, value, unit):
        self._value = float(value)
        self._unit = unit

    ##############################################

    def __float__(self):
        return self._value

    ##############################################

    def __str__(self):
        return self._unit

####################################################################################################

class PercentLengthAttribute(InheritAttribute):

    ##############################################

    @classmethod
    def _from_xml(cls, value):
        # length ::= number ("em" | "ex" | "px" | "in" | "cm" | "mm" | "pt" | "pc" | "%")?
        if value.endswith('%'):
            return PercentValue(value[:-1])
        elif value[-1].isalpha():
            return UnitValue(value[:-2], value[-2])
        else:
            return float(value)

    ##############################################

    @classmethod
    def _to_xml(cls, value):

        # Fixme: ok ???
        if isinstance(value, PercentValue):
            return '{}%'.format(float(value))
        elif isinstance(value, UnitValue):
            return '{}{}'.format(float(value), value.unit)
        else:
            return str(value)

####################################################################################################

class ColorMixin:

    __attributes__ = (
        StringAttribute('fill'), # none inherit red #ffbb00
        StringAttribute('stroke'),
    )

####################################################################################################

class StrokeMixin:

    __attributes__ = (
        StringAttribute('stroke_line_cap', 'stroke-linecap'),
        StringAttribute('stroke_line_join', 'stroke-linejoin'),
        NumberAttribute('stroke_miter_limit', 'stroke-miterlimit'),
        PercentLengthAttribute('stroke_width', 'stroke-width'),
        FloatListAttribute('stroke_dasharray', 'stroke-dasharray') # stroke-dasharray="20,10,5,5,5,10"
    )

    LINE_CAP_STYLE = (
        'butt',
        'round',
        'square',
        'inherit',
    )

    LINE_JOIN_STYLE = (
        'miter',
        'round',
        'bevel',
        'inherit',
    )

####################################################################################################

class PathMixin(ColorMixin, StrokeMixin):
    pass

####################################################################################################

class FontMixin:

    __attributes__ = (
        StringAttribute('font_size', 'font-size'),
        StringAttribute('font_family', 'font-family'),
    )

    # font-face-format
    # font-face-name
    # font-face-src
    # font-face-uri

    # text-anchor

    # glyph 	Defines the graphics for a given glyph
    # glyphRef 	Defines a possible glyph to use
    # hkern

####################################################################################################
####################################################################################################

class StyleMixin:

    __attributes__ = (
        StringAttribute('style'),
    )

####################################################################################################
#
# Shared attributes
#
####################################################################################################

class PositionMixin:

    __attributes__ = (
        FloatAttribute('x'),
        FloatAttribute('y'),
    )

####################################################################################################

class CenterMixin:

    __attributes__ = (
        FloatAttribute('cx'), # x-axis center of the circle
        FloatAttribute('cy'),
    )

####################################################################################################

class DeltaMixin:

    __attributes__ = (
        FloatAttribute('dx'),
        FloatAttribute('dy'),
    )

####################################################################################################

class RadiusMixin:

    __attributes__ = (
        FloatAttribute('rx'), # x-axis radius (to round the element)
        FloatAttribute('ry'),
    )

####################################################################################################

class PointsMixin:

    __attributes__ = (
        StringAttribute('points'), # points="200,10 250,190 160,210"
    )

####################################################################################################

class SizeMixin:

    __attributes__ = (
        StringAttribute('height'),
        StringAttribute('width'),
    )

####################################################################################################

class TransformAttribute(StringAttribute):

    TRANSFORM = (
        'matrix',
        'rotate',
        'scale',
        'skewX',
        'skewY',
        'translate'
    )

    ##############################################

    @classmethod
    def from_xml(cls, value):

        if isinstance(value, AffineTransformation2D):
            # Python value
            return value
        else:
            transforms = []
            for transform in split_space_list(value):
                pos0 = value.find('(')
                pos1 = value.find(')')
                if pos0 == -1 or pos1 != len(value) -1:
                    raise ValueError
                transform_type = value[:pos0]
                values = [float(x) for x in value[pos0+1:-1].split(',')]
                transforms.append((transform_type, values))
                # Fixme:

            # return transforms
            return cls.to_python(transforms, concat=True)

    ##############################################

    @classmethod
    def to_xml(cls, value):
        # Fixme: wrong if value is AffineTransformation2D !!!
        # Fixme: to func
        return 'matrix({})'.format(' '.join([str(x) for x in value.to_list()]))

    ##############################################

    @classmethod
    def to_python(cls, transforms, concat=True):

        def complete(values, size):
            return values + [0]*(size - len(values))

        global_transform = AffineTransformation2D.Identity()
        py_transforms = []
        for name, values in transforms:
            transform = None
            if name == 'matrix':
                array = [values[i] for i in (0, 2, 4, 1, 3, 5)] + [0, 0, 1]
                transform = AffineTransformation2D(array)
            elif name == 'translate':
                vector = Vector2D(complete(values, 2))
                transform = AffineTransformation2D.Translation(vector)
            elif name == 'scale':
                transform = AffineTransformation2D.Scale(*values)
            elif name == 'rotate':
                angle, *vector = complete(values, 3)
                vector = Vector2D(vector)
                transform = AffineTransformation2D.RotationAt(vector, angle)
            elif name == 'skewX':
                angle = values[0]
                raise NotImplementedError
            elif name == 'skewY':
                angle = values[0]
                raise NotImplementedError
            else:
                raise NotImplementedError
            if concat:
                global_transform = transform * global_transform
            else:
                py_transforms.append(transform)

        if concat:
            return global_transform
        else:
            return py_transforms

####################################################################################################

class TransformMixin:

    __attributes__ = (
        TransformAttribute('transform'), # matrix(1,0,0,-1,0,1.)
    )

####################################################################################################
####################################################################################################

# The available filter elements in SVG are:
#
#  <feBlend> - filter for combining images
#  <feColorMatrix> - filter for color transforms
#  <feComponentTransfer>
#  <feComposite>
#  <feConvolveMatrix>
#  <feDiffuseLighting>
#  <feDisplacementMap>
#  <feFlood>
#  <feGaussianBlur>
#  <feImage>
#  <feMerge>
#  <feMorphology>
#  <feOffset> - filter for drop shadows
#  <feSpecularLighting>
#  <feTile>
#  <feTurbulence>
#  <feDistantLight> - filter for lighting
#  <fePointLight> - filter for lighting
#  <feSpotLight> - filter for lighting

####################################################################################################

class SvgElementMixin(IdMixin, StyleMixin, TransformMixin):
    pass

####################################################################################################
#
# Svg Root Element
#
####################################################################################################

class Svg(PositionMixin, SizeMixin, XmlObjectAdaptator):

    """Creates an SVG document fragment"""

    __tag__ = 'svg'

    # xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve"

    __attributes__ = (
        StringAttribute('version'),
        FloatListAttribute('view_box', 'viewBox'),
        # the points "seen" in this SVG drawing area. 4 values separated by white space or
        # commas. (min x, min y, width, height)
        StringAttribute('preserve_aspect_ratio', 'preserveAspectRatio'),
        # 'none' or any of the 9 combinations of 'xVALYVAL' where VAL is 'min', 'mid' or 'max'.
        # (default xMidYMid)
        StringAttribute('zoom_and_pan', 'zoomAndPan')
        # 'magnify' or 'disable'. Magnify option allows users to pan and zoom your file
        # (default magnify)
    )

    # x="top left corner when embedded (default 0)"
    # y="top left corner when embedded (default 0)"
    # width="the width of the svg fragment (default 100%)"
    # height="the height of the svg fragment (default 100%)"

####################################################################################################
#
# SVG Elements by name
#
####################################################################################################

class Anchor(XmlObjectAdaptator):

    """Creates a link around SVG elements"""

    __tag__ = 'a'

    # xlink:show
    # xlink:actuate
    # xlink:href
    # target

####################################################################################################

class AltGlyph(PositionMixin, DeltaMixin, XmlObjectAdaptator):

    """Provides control over the glyphs used to render particular character data"""

    __tag__ = 'altGlyph'

    # rotate
    # glyphRef
    # format
    # xlink:href

####################################################################################################

class AltGlyphDef(IdMixin, XmlObjectAdaptator):

    """Defines a substitution set for glyphs"""

    __tag__= 'altGlyphDef'

####################################################################################################

class AltGlyphItem(IdMixin, XmlObjectAdaptator):

    """Defines a candidate set of glyph substitutions"""

    __tag__ = 'altGlyphItem'

####################################################################################################

class Animate(XmlObjectAdaptator):

    """Defines how an attribute of an element changes over time"""

    __tag__ = 'animate'

    # attributeName="the name of the target attribute"
    # by="a relative offset value"
    # from="the starting value"
    # to="the ending value"
    # dur="the duration"
    # repeatCount="the number of time the animation will take place"

####################################################################################################

class AnimateMotion(XmlObjectAdaptator):

    """Causes a referenced element to move along a motion path"""

    __tag__ = 'animateMotion'

    # calcMode="the interpolation mode for the animation. Can be 'discrete', 'linear', 'paced', 'spline'"
    # path="the motion path"
    # keyPoints="how far along the motion path the object shall move at the moment in time"
    # rotate="applies a rotation transformation"
    # xlink:href="an URI reference to the <path> element which defines the motion path"

####################################################################################################

class AnimateTransform(XmlObjectAdaptator):

    """Animates a transformation attribute on a target element, thereby allowing animations to control
    translation, scaling, rotation and/or skewing

    """

    __tag__ = 'animateTransform'

    # by="a relative offset value"
    # from="the starting value"
    # to="the ending value"
    # type="the type of transformation which is to have its values change over time. Can be 'translate', 'scale', 'rotate', 'skewX', 'skewY'"

####################################################################################################

class Circle(CenterMixin, PathMixin, SvgElementMixin, XmlObjectAdaptator):

    """Defines a circle"""

    __tag__ = 'circle'

    __attributes__ = (
        FloatAttribute('r'), # circle's radius. Required.
    )

####################################################################################################

class ClipPath(XmlObjectAdaptator):

    """Clipping is about hiding what normally would be drawn. The stencil which defines what is and
    what isn't drawn is called a clipping path

    """

    __tag__ = 'clipPath'

    # clip-path="the referenced clipping path is intersected with the referencing clipping path"
    # clipPathUnits="'userSpaceOnUse' or 'objectBoundingBox'. The second value makes units of children a fraction of the object bounding box which uses the mask (default: 'userSpaceOnUse')"

####################################################################################################

class ColorProfile(XmlObjectAdaptator):

    """Specifies a color profile description (when the document is styled using CSS)"""

    __tag__ = 'color-profile'

    # local="the unique ID for a locally stored color profile"
    # name=""
    # rendering-intent="auto|perceptual|relative-colorimetric|saturation|absolute-colorimetric"
    # xlink:href="the URI of an ICC profile resource"

####################################################################################################

class Cursor(PositionMixin, XmlObjectAdaptator):

    """Defines a platform-independent custom cursor"""

    __tag__ = 'cursor'

    # x="the x-axis top-left corner of the cursor (default is 0)"
    # y="the y-axis top-left corner of the cursor (default is 0)"
    # xlink:href="the URI of the image to use as the cursor

####################################################################################################

class Defs(XmlObjectAdaptator):

    """A container for referenced elements"""

    __tag__ = 'defs'

####################################################################################################

class Desc(XmlObjectAdaptator):

    """A text-only description for container elements or graphic elements in SVG (user agents may
    display the text as a tooltip)"""

    __tag__ = 'desc'

####################################################################################################

class Ellipse(CenterMixin, PathMixin, StyleMixin, XmlObjectAdaptator):

    """Defines an ellipse"""

    __tag__ = 'ellipse'

    __attributes__ = (
        FloatAttribute('rx'),
        FloatAttribute('ry'),
    )

####################################################################################################

class FeBlend(XmlObjectAdaptator):

    """Composes two objects together according to a certain blending mode"""

    __tag__ = 'feBlend'

    # mode="the image blending modes: normal|multiply|screen|darken|lighten"
    # in="identifies input for the given filter primitive: SourceGraphic | SourceAlpha | BackgroundImage | BackgroundAlpha | FillPaint | StrokePaint | <filter-primitive-reference>"
    # in2="the second input image to the blending operation"

####################################################################################################

class Group(FontMixin, PathMixin, SvgElementMixin, XmlObjectAdaptator):

    """Used to group together elements"""

    __tag__ = 'g'

    __attributes__ = (
        StringAttribute('clip_path', 'clip-path', None),
        StringAttribute('data_name', 'data-name'),
        #fill="the fill color for the group"
        #opacity="the opacity for the group"
    )

####################################################################################################

class Image(PositionMixin, SizeMixin, XmlObjectAdaptator):

    """Defines an image"""

    __tag__ = 'image'

    # x="the x-axis top-left corner of the image"
    # y="the y-axis top-left corner of the image"
    # width="the width of the image". Required.
    # height="the height of the image". Required.
    # xlink:href="the path to the image". Required.

####################################################################################################

class Line(PathMixin, SvgElementMixin, XmlObjectAdaptator):

    """Defines a line"""

    __tag__ = 'line'

    __attributes__ = (
        FloatAttribute('x1'), # x start point of the line
        FloatAttribute('y1'),
        FloatAttribute('x2'), # x end point of the line
        FloatAttribute('y2'),
    )

####################################################################################################

class LinearGradient(IdMixin, XmlObjectAdaptator):

    """Defines a linear gradient. Linear gradients fill the object by using a vector, and can be defined
    as horizontal, vertical or angular gradients.

    """

    __tag__ = 'linearGradient'

    # id="the unique id used to reference this pattern. Required to reference it"
    # gradientUnits="'userSpaceOnUse' or 'objectBoundingBox'. Use the view box or object to determine relative position of vector points. (Default 'objectBoundingBox')"
    # gradientTransform="the transformation to apply to the gradient"
    # x1="the x start point of the gradient vector (number or % - 0% is default)"
    # y1="the y start point of the gradient vector. (0% default)"
    # x2="the x end point of the gradient vector. (100% default)"
    # y2="the y end point of the gradient vector. (0% default)"
    # spreadMethod="'pad' or 'reflect' or 'repeat'"
    # xlink:href="reference to another gradient whose attribute values are used as defaults and stops included. Recursive"

####################################################################################################

class Marker(XmlObjectAdaptator):

    """Markers can be placed on the vertices of lines, polylines, polygons and paths. These elements can
    use the marker attributes "marker-start", "marker-mid" and "marker-end"' which inherit by
    default or can be set to 'none' or the URI of a defined marker. You must first define the marker
    before you can reference it via its URI. Any kind of shape can be put inside marker. They are
    drawn on top of the element they are attached to markerUnits="'strokeWidth' or
    'userSpaceOnUse'. If 'strokeWidth' is used then one unit equals one stroke width. Otherwise, the
    marker does not scale and uses the the same view units as the referencing element (default
    'strokeWidth')

    """

    __tag__ = 'marker'

    # refx="the position where the marker connects with the vertex (default 0)"
    # refy="the position where the marker connects with the vertex (default 0)"
    # orient="'auto' or an angle to always show the marker at. 'auto' will compute an angle that makes the x-axis a tangent of the vertex (default 0)"
    # markerWidth="the width of the marker (default 3)"
    # markerHeight="the height of the marker (default 3)"
    # viewBox="the points "seen" in this SVG drawing area. 4 values separated by white space or commas. (min x, min y, width, height)"

####################################################################################################

class Mask(PositionMixin, SizeMixin, XmlObjectAdaptator):

    """Masking is a combination of opacity values and clipping. Like clipping you can use shapes, text
    or paths to define sections of the mask. The default state of a mask is fully transparent which
    is the opposite of clipping plane. The graphics in a mask sets how opaque portions of the mask
    are

    """

    __tag__ = 'mask'

    # maskUnits="'userSpaceOnUse' or 'objectBoundingBox'. Set whether the clipping plane is relative the full view port or object (default: 'objectBoundingBox')"
    # maskContentUnits="Use the second with percentages to make mask graphic positions relative the object. 'userSpaceOnUse' or 'objectBoundingBox' (default: 'userSpaceOnUse')"
    # x="the clipping plane of the mask (default: -10%)"
    # y="the clipping plane of the mask (default: -10%)"
    # width="the clipping plane of the mask (default: 120%)"
    # height="the clipping plane of the mask (default: 120%)"

####################################################################################################

class PathDataAttribute(StringAttribute):

    """Define a path data attribute.

    Path data can contain newline characters and thus can be broken up into multiple lines to
    improve readability. Because of line length limitations with certain related tools, it is
    recommended that SVG generators split long path data strings across multiple lines, with each
    line not exceeding 255 characters. Also note that newline characters are only allowed at certain
    places within path data.

    The syntax of path data is concise in order to allow for minimal file size and efficient
    downloads, since many SVG files will be dominated by their path data. Some of the ways that SVG
    attempts to minimize the size of path data are as follows:

     * All instructions are expressed as one character (e.g., a moveto is expressed as an M).
     * Superfluous white space and separators such as commas can be eliminated
       (e.g., "M 100 100 L 200 200" contains unnecessary spaces and
       could be expressed more compactly as "M100 100L200 200").
     * The command letter can be eliminated on subsequent commands if the same command
       is used multiple times in a row (e.g., you can drop the second
       "L" in "M 100 200 L 200 100 L -100 -200" and use
       "M 100 200 L 200 100 -100 -200" instead).
     * Relative versions of all commands are available (uppercase means absolute coordinates,
       lowercase means relative coordinates).
     * Alternate forms of lineto are available to optimize the special cases of horizontal and
       vertical lines (absolute and relative).
     * Alternate forms of curve are available to optimize the special cases where some
       of the control points on the current segment can be determined automatically
       from the control points on the previous segment.

    The following commands are available for path data:

     * Move to
       M x y
       m dx dy
     * Line to
       L x y
       l dx dy
     * Horizontal Line to
       H x
       h dx
     * Vertical Line to
       V y
       v dy
     * Cubic Bézier Curve
       C x1 y1, x2 y2, x y
       c dx1 dy1, dx2 dy2, dx dy
     * Smooth Cubic Bézier Curve
       S x2 y2, x y
       s dx2 dy2, dx dy"
     * Quadratic Bézier Curve
       Q x1 y1, x y
       q dx1 dy1, dx dy
     * Smooth Quadratic Bézier Curve
       T x y
       t dx dy
     * Elliptical Arc
       A rx ry x-axis-rotation large-arc-flag sweep-flag x y
       a rx ry x-axis-rotation large-arc-flag sweep-flag dx dy
     * Close Path
       Z

    """

    NUMBER_OF_ARGS = {
        'm':2,
        'l':2,
        'h':1,
        'v':1,
        'c':6,
        's':4,
        'q':4,
        't':3,
        'a':7,
        'z':0,
        }

    COMMANDS = ''.join(NUMBER_OF_ARGS.keys())

    _logger = _module_logger.getChild('PathDataAttribute')

    ##############################################

    @classmethod
    def from_xml(cls, svg_path):

        # cls._logger.info('SVG path:\n'+ svg_path)

        # Replace comma separator by space
        cleaned_svg_path = svg_path.replace(',', ' ')
        # Add space after letter
        data_path = ''
        for c in cleaned_svg_path:
            data_path += c
            if c.isalpha:
                data_path += ' '
        # Convert float values
        parts = []
        for part in split_space_list(cleaned_svg_path):
            if not(len(part) == 1 and part.isalpha()):
                part = float(part)
            parts.append(part)

        commands = []
        command = None # last command
        number_of_args = None
        i = 0
        while i < len(parts):
            part = parts[i]
            if isinstance(part, str):
                command = part
                command_lower = command.lower()
                if command_lower not in cls.COMMANDS:
                    raise ValueError("Invalid path instruction: '{}' in\n{}".format(command, svg_path))
                number_of_args = cls.NUMBER_OF_ARGS[command_lower]
                i += 1 # move to first arg
            # else repeated instruction
            next_i = i + number_of_args
            args = parts[i:next_i]
            commands.append((command, args))
            i = next_i
            # for implicit line to
            if command == 'm':
                command = 'l'
            elif command == 'M':
                command = 'L'

        # return commands
        # Fixme: do later ???
        return cls.to_geometry(commands)

    ##############################################

    @classmethod
    def to_xml(cls, value):

        path_data = ''
        for command in value:
            if path_data:
                path_data += ' '
            path_data += ' '.join(list(command[0]) + [str(x) for x in command[1]])
        return path_data

    ##############################################

    @classmethod
    def as_vector(cls, args):

        number_of_args = len(args)
        number_of_vectors = number_of_args // 2
        if number_of_args != number_of_vectors * 2:
            raise ValueError('len(args) is not // 2: {}'.format(number_of_args))
        return [Vector2D(args[i:i+2]) for i in range(0, number_of_args, 2)]

    ##############################################

    @classmethod
    def to_geometry(cls, commands):

        # cls._logger.info('Path:\n' + str(commands).replace('), ', '),\n '))
        path = None
        for command, args in commands:
            command_lower = command.lower()
            absolute = command_lower != command # Upper case means absolute
            # if is_lower:
            #     cls._logger.warning('incremental command')
            #     raise NotImplementedError
            if path is None:
                if command_lower != 'm':
                    raise NameError('Path must start with m')
                path = Path2D(args) # Vector2D()
            else:
                if command_lower == 'l':
                    path.line_to(args, absolute=absolute)
                elif command == 'h':
                    path.horizontal_to(*args, absolute=False)
                elif command == 'H':
                    path.absolute_horizontal_to(*args)
                elif command_lower == 'v':
                    path.vertical_to(*args, absolute=absolute)
                elif command == 'V':
                    path.absolute_vertical_to(*args)
                elif command_lower == 'c':
                    path.cubic_to(*cls.as_vector(args), absolute=absolute)
                elif command_lower == 's':
                    path.stringed_quadratic_to(*cls.as_vector(args), absolute=absolute)
                elif command_lower == 'q':
                    path.quadratic_to(*cls.as_vector(args), absolute=absolute)
                elif command_lower == 't':
                    path.stringed_cubic_to(*cls.as_vector(args), absolute=absolute)
                elif command_lower == 'a':
                    radius_x, radius_y, angle, large_arc, sweep, x, y = args
                    point = Vector2D(x, y)
                    path.arc_to(point, radius_x, radius_y, angle, bool(large_arc), bool(sweep), absolute=absolute)
                elif command_lower == 'z':
                    path.close()

        return path

####################################################################################################

class Path(PathMixin, SvgElementMixin, XmlObjectAdaptator):

    """Defines a path"""

    __tag__ = 'path'
    __attributes__ = (
        PathDataAttribute('path_data', 'd'), # a set of commands which define the path
        FloatAttribute('path_length', 'pathLength'),
        # If present, the path will be scaled so that the computed path length of the points equals
        # this value
    )

####################################################################################################

class Pattern(IdMixin, PositionMixin, SizeMixin, XmlObjectAdaptator):

    """Defines the coordinates you want the view to show and the size of the view. Then you add shapes
    into your pattern. The pattern repeats when an edge of the view box (viewing area) is hit

    """

    __tag__ = 'pattern'

    # id="the unique id used to reference this pattern." Required.
    # patternUnits="'userSpaceOnUse' or 'objectBoundingBox'. The second value makes units of x, y, width, height a fraction (or %) of the object bounding box which uses the pattern."
    # patternContentUnits="'userSpaceOnUse' or 'objectBoundingBox'"
    # patternTransform="allows the whole pattern to be transformed"
    # x="pattern's offset from the top-left corner (default 0)"
    # y="pattern's offset from the top-left corner. (default 0)"
    # width="the width of the pattern tile (default 100%)"
    # height="the height of the pattern tile (default 100%)"
    # viewBox="the points "seen" in this SVG drawing area. 4 values separated by white space or commas. (min x, min y, width, height)"
    # xlink:href="reference to another pattern whose attribute values are used as defaults and any children are inherited. Recursive"

####################################################################################################

class Polyline(PointsMixin, PathMixin, SvgElementMixin, XmlObjectAdaptator):

    """Defines a graphic that contains at least three sides"""

    __tag__ = 'polyline'

####################################################################################################

class Polygon(Polyline, XmlObjectAdaptator):

    """Defines any shape that consists of only straight lines"""

    __tag__ = 'polyline'

    # fill-rule="part of the FillStroke presentation attributes"

####################################################################################################

class RadialGradient(XmlObjectAdaptator):

    """Defines a radial gradient. Radial gradients are created by taking a circle and smoothly changing
    values between gradient stops from the focus point to the outside radius.

    """

    __tag__ = 'radialGradient'

    # gradientUnits="'userSpaceOnUse' or 'objectBoundingBox'. Use the view box or object to determine relative position of vector points. (Default 'objectBoundingBox')"
    # gradientTransform="the transformation to apply to the gradient"
    # cx="the center point of the gradient (number or % - 50% is default)"
    # cy="the center point of the gradient. (50% default)"
    # r="the radius of the gradient. (50% default)"
    # fx="the focus point of the gradient. (0% default)"
    # fy="The focus point of the gradient. (0% default)"
    # spreadMethod="'pad' or 'reflect' or 'repeat'"
    # xlink:href="Reference to another gradient whose attribute values are used as defaults and stops included. Recursive"

####################################################################################################

class Rect(PositionMixin, RadiusMixin, SizeMixin, PathMixin, SvgElementMixin, XmlObjectAdaptator):

    """Defines a rectangle"""

    __tag__ = 'rect'

    ##############################################

    @property
    def geometry(self):

        # Fixme: width is str
        width = float(self.width)
        height = float(self.height)

        # Fixme: which one ???
        radius_x = self.rx
        radius_y = self.ry
        if radius_y == 0:
            radius = None
        else:
            radius = radius_y

        point = Vector2D(self.x, self.y)
        path = Path2D(point)
        path.horizontal_to(width)
        path.vertical_to(height, radius=radius)
        path.horizontal_to(-width, radius=radius)
        path.close(radius=radius, close_radius=radius)

        return path

####################################################################################################

class Stop(XmlObjectAdaptator):

    """The stops for a gradient"""

    __tag__ = 'stop'

    # offset="the offset for this stop (0 to 1/0% to 100%)". Required.
    # stop-color="the color of this stop"
    # stop-opacity="the opacity of this stop (0 to 1)"

####################################################################################################

class Style(TextXmlObjectAdaptator):

    """Defines style"""

    __tag__ = 'style'

####################################################################################################

class Text(PositionMixin, DeltaMixin, FontMixin, ColorMixin, SvgElementMixin, TextXmlObjectAdaptator):

    """Defines a text"""

    __tag__ = 'text'

    # x="a list of x-axis positions. The nth x-axis position is given to the nth character in the text. If there are additional characters after the positions run out they are placed after the last character. 0 is default"
    # y="a list of y-axis positions. (see x). 0 is default"
    # dx="a list of lengths which moves the characters relative to the absolute position of the last glyph drawn. (see x)"
    # dy="a list of lengths which moves the characters relative to the absolute position of the last glyph drawn. (see x)"
    # rotate="a list of rotations. The nth rotation is performed on the nth character. Additional characters are NOT given the last rotation value"
    # textLength="a target length for the text that the SVG viewer will attempt to display the text between by adjusting the spacing and/or the glyphs. (default: The text's normal length)"
    # lengthAdjust="tells the viewer what to adjust to try to accomplish rendering the text if the length is specified. The two values are 'spacing' and 'spacingAndGlyphs'"

    __attributes__ = (
        # Fixme: common ???
        StringAttribute('_class', 'class', None),
        StringAttribute('style'),
    )

####################################################################################################

class TextRef(XmlObjectAdaptator):

    """References any <text> element in the SVG document and reuse it"""

    __tag__ = 'tref'

####################################################################################################

class TextSpan(Text, XmlObjectAdaptator):

    """Identical to the <text> element but can be nested inside text tags and inside itself"""

    __tag__ = 'textspan'

####################################################################################################

class Use(PositionMixin, SizeMixin, XmlObjectAdaptator):

    """Uses a URI to reference a <g>, <svg> or other graphical element with a unique id attribute and
    replicate it. The copy is only a reference to the original so only the original exists in the
    document. Any change to the original affects all copies.

    """

    __tag__ = 'use'

    # x="the x-axis top-left corner of the cloned element"
    # y="the y-axis top-left corner of the cloned element"
    # width="the width of the cloned element"
    # height="the height of the cloned element"
    # xlink:href="a URI reference to the cloned element"
