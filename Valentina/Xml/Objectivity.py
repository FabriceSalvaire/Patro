####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
# Copyright (C) 2017 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

# cf. also http://lxml.de/objectify.html

####################################################################################################

import logging
from collections import OrderedDict

from lxml import etree

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Attribute:

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

    def from_xml(self, value):
        raise NotImplementedError

    ##############################################

    def set_property(self, cls):

        py_cls_attribute = self.py_cls_attribute
        setattr(cls,
                self.py_attribute,
                property(lambda self: getattr(self, py_cls_attribute),
                         lambda self, value: setattr(self, py_cls_attribute, value),
                ))

    ##############################################

    def get_attribute(self, instance):

        return getattr(instance, self.py_cls_attribute)

    ##############################################

    def set_attribute(self, instance, value):

        setattr(instance, self.py_cls_attribute, value)

####################################################################################################

class BoolAttribute(Attribute):

    ##############################################

    def from_xml(self, value):
        if value == "true" or value == "1":
            return True
        elif value == "false" or value == "0":
            return False
        else:
            raise ValueError("Incorrect boolean value {}".format(value))

####################################################################################################

class IntAttribute(Attribute):

    ##############################################

    def from_xml(self, value):
        return int(value)

####################################################################################################

class FloatAttribute(Attribute):

    ##############################################

    def from_xml(self, value):
        return float(value)

####################################################################################################

class StringAttribute(Attribute):

    ##############################################

    def from_xml(self, value):
        return str(value)

####################################################################################################

class XmlObjectAdaptatorMetaClass(type):

    _logger = _module_logger.getChild('XmlObjectAdaptatorMetaClass')

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        # cls._logger.info(str((cls, class_name, super_classes, class_attribute_dict)))
        type.__init__(cls, class_name, super_classes, class_attribute_dict)
        super_attributes = cls.register_from_super_class(super_classes)
        cls.__attributes__ = super_attributes + list(cls.__attributes__)
        for attribute in cls.__attributes__:
            # cls._logger.info('Register {}'.format(attribute))
            attribute.set_property(cls)

    ##############################################

    def register_from_super_class(cls, super_classes):

        super_attributes = []
        for super_class in super_classes:
            # __mro__ = [cls, ..., object]
            super_attributes += cls.register_from_super_class(super_class.__mro__[1:-1]) # super_class.__subclasses__()
            if hasattr(super_class, '__attributes__'):
                super_attributes += list(super_class.__attributes__)
        return super_attributes

####################################################################################################

class XmlObjectAdaptator(metaclass = XmlObjectAdaptatorMetaClass):

    __tag__ = None
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
            if py_attribute in kwargs:
                value = attribute.from_xml(kwargs[py_attribute])
            else:
                value = attribute.default
            attribute.set_attribute(self, value)

    ##############################################

    @classmethod
    def get_dict(cls, instance, exclude=()):

        return {attribute.py_attribute:getattr(instance, attribute.py_attribute)
                for attribute in cls.__attributes__
                if attribute.py_attribute not in exclude
        }

    ##############################################

    def to_dict(self, exclude=()):

        return {attribute.py_attribute:attribute.get_attribute(self)
                for attribute in self.__attributes__
                if attribute.py_attribute not in exclude
        }

    ##############################################

    def to_xml(self, **kwargs):

        attributes = {attribute.xml_attribute:str(attribute.get_attribute(self)) for attribute in self.__attributes__}
        attributes.update(kwargs)
        return etree.Element(self.__tag__, **attributes)

    ##############################################

    def to_xml_string(self):

        return etree.tostring(self.to_xml())

    ##############################################

    # def __getattribute__(self, name):
    #     object.__getattribute__(self, '_' + name)
