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

# cf. also http://lxml.de/objectify.html

####################################################################################################

__all__ = [
    'BoolAttribute',
    'FloatAttribute',
    'FloatListAttribute',
    'IntAttribute',
    'StringAttribute',
    'XmlObjectAdaptator',
]

####################################################################################################

import logging
# from collections import OrderedDict

from lxml import etree

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Attribute:

    """Class to define XML element attribtes"""

    ##############################################

    def __init__(self, py_attribute, xml_attribute=None, default=None):

        self._py_attribute = py_attribute

        if xml_attribute is None:
            self._xml_attribute = py_attribute
        else:
            self._xml_attribute = xml_attribute

        self._default = default

    ##############################################

    @property
    def py_attribute(self):
        return self._py_attribute

    @property
    def py_cls_attribute(self):
        """Return the private identifier used for :class:`XmlObjectAdaptator`"""
        return '_' + self._py_attribute

    @property
    def xml_attribute(self):
        return self._xml_attribute

    @property
    def default(self):
        return self._default

    ##############################################

    def __repr__(self):
        return '{} {}'.format(self.__class__.__name__, self._py_attribute)

    ##############################################

    @classmethod
    def from_xml(cls, value):
        """Convert a value from XML to Python"""
        raise NotImplementedError

    ##############################################

    @classmethod
    def to_xml(cls, value):
        """Convert a value from Python to XML"""
        return str(value)

    ##############################################

    def set_property(self, cls):

        """Define a property for this attribute in :class:`XmlObjectAdaptator`"""

        py_cls_attribute = self.py_cls_attribute
        setattr(cls,
                self.py_attribute,
                property(lambda self: getattr(self, py_cls_attribute),
                         lambda self, value: setattr(self, py_cls_attribute, value),
                ))

    ##############################################

    def get_attribute(self, instance):
        """Get an attribute of an :class:`XmlObjectAdaptator` instance"""
        return getattr(instance, self.py_cls_attribute)

    ##############################################

    def set_attribute(self, instance, value):
        """Set an attribute of an :class:`XmlObjectAdaptator` instance"""
        setattr(instance, self.py_cls_attribute, value)

####################################################################################################

class BoolAttribute(Attribute):

    ##############################################

    @classmethod
    def from_xml(cls, value):
        if value == "true" or value == "1":
            return True
        elif value == "false" or value == "0":
            return False
        else:
            raise ValueError("Incorrect boolean value {}".format(value))

    ##############################################

    @classmethod
    def to_xml(cls, value):
        return 'true' if value else 'false'

####################################################################################################

class IntAttribute(Attribute):

    ##############################################

    @classmethod
    def from_xml(cls, value):
        return int(value)

####################################################################################################

class FloatAttribute(Attribute):

    ##############################################

    @classmethod
    def from_xml(cls, value):
        return float(value)

####################################################################################################

class FloatListAttribute(Attribute):

    ##############################################

    @classmethod
    def from_xml(self, value):

        if value == 'none' or value is None:
            return None
        elif isinstance(value, (tuple, list)): # Python value
            return value
        else:
            if ' ' in value:
                separator = ' '
            elif ',' in value:
                separator = ','
            else:
                return [float(value)]
            return [float(x) for x in value.split(separator)]

    ##############################################

    @classmethod
    def to_xml(cls, value):
        return ' '.join([str(x) for x in value])

####################################################################################################

class StringAttribute(Attribute):

    ##############################################

    @classmethod
    def from_xml(cls, value):
        return str(value)

####################################################################################################

class XmlObjectAdaptatorMetaClass(type):

    """Metaclass to collect attributes from super-classes and define a property for each attribute"""

    _logger = _module_logger.getChild('XmlObjectAdaptatorMetaClass')

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        # cls._logger.info(str((cls, class_name, super_classes, class_attribute_dict)))
        type.__init__(cls, class_name, super_classes, class_attribute_dict)

        # Collect attributes from super-classes and update
        super_attributes = cls.register_from_super_class(super_classes)
        cls.__attributes__ = super_attributes + list(cls.__attributes__)

        # Define a property for each attribute
        for attribute in cls.__attributes__:
            # cls._logger.info('Register {}'.format(attribute))
            attribute.set_property(cls)

    ##############################################

    def register_from_super_class(cls, super_classes):

        """Collect attributes from super-classes"""

        # Fixme: use set ???

        super_attributes = []
        for super_class in super_classes:
            # __mro__ = [cls, ..., object]
            super_attributes += cls.register_from_super_class(super_class.__mro__[1:-1]) # super_class.__subclasses__()
            if hasattr(super_class, '__attributes__'):
                super_attributes += list(super_class.__attributes__)
        return super_attributes

####################################################################################################

class XmlObjectAdaptator(metaclass=XmlObjectAdaptatorMetaClass):

    """Class to implement an object oriented adaptor for XML elements."""

    __tag__ = None # XML tag
    __attributes__ = ()

    ##############################################

    def __init__(self, *args, **kwargs):

        if args:
            self._init_from_xml(args[0])
        elif kwargs:
            self._init_from_kwargs(kwargs)

    ##############################################

    def __repr__(self):
        return '{} {}'.format(self.__class__.__name__, self.to_dict())

    ##############################################

    def _init_from_xml(self, xml_element):

        xml_attributes = xml_element.attrib
        for attribute in self.__attributes__:
            xml_attribute = attribute.xml_attribute
            if xml_attribute in xml_attributes:
                value = attribute.from_xml(xml_attributes[xml_attribute])
            else:
                value = attribute.default
            attribute.set_attribute(self, value)

    ##############################################

    def _init_from_kwargs(self, kwargs):

        for attribute in self.__attributes__:
            py_attribute = attribute.py_attribute
            # Fixme: duplicated code
            if py_attribute in kwargs:
                # Fixme: see VitFormat.py StrokeStyleAttribute !!!
                value = attribute.from_xml(kwargs[py_attribute])
            else:
                value = attribute.default
            attribute.set_attribute(self, value)

    ##############################################

    @classmethod
    def get_dict(cls, instance, exclude=()):
        """Return a dict containing the attributes"""
        return {
            attribute.py_attribute:getattr(instance, attribute.py_attribute)
            for attribute in cls.__attributes__
            if attribute.py_attribute not in exclude
        }

    ##############################################

    def to_dict(self, exclude=()):
        """Return a dict containing the attributes"""
        return {attribute.py_attribute:attribute.get_attribute(self)
                for attribute in self.__attributes__
                if attribute.py_attribute not in exclude
        }

    ##############################################

    def to_xml(self, **kwargs):

        """Return an etree element"""

        # attributes = {attribute.xml_attribute:str(attribute.get_attribute(self)) for attribute in self.__attributes__}

        attributes = {}
        for attribute in self.__attributes__:
            value = attribute.get_attribute(self)
            if value is not None:
                attributes[attribute.xml_attribute] = attribute.to_xml(value)
        attributes.update(kwargs)

        return etree.Element(self.__tag__, **attributes)

    ##############################################

    def to_xml_string(self):
        """Return a XML string"""
        return etree.tostring(self.to_xml())

    ##############################################

    # def __getattribute__(self, name):
    #     object.__getattribute__(self, '_' + name)

####################################################################################################

class TextXmlObjectAdaptator(XmlObjectAdaptator):

    """Class to implement an object oriented adaptor for text XML elements."""

    ##############################################

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.text = kwargs.get('text', '')

    ##############################################

    def _init_from_xml(self, xml_element):

        super()._init_from_xml(xml_element)
        self.text = str(xml_element.text)

    ##############################################

    def to_xml(self, **kwargs):

        element = super().to_xml(**kwargs)
        element.text = self.text

        return element
