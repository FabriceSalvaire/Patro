####################################################################################################
#
# X - x
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

####################################################################################################

import ast
import logging

from lxml import etree

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

# <?xml version='1.0' encoding='UTF-8'?>
# <vit>
#     <!--Measurements created with Valentina (http://www.valentina-project.org/).-->
#     <version>0.3.3</version>
#     <read-only>false</read-only>
#     <notes/>
#     <unit>cm</unit>
#     <pm_system>998</pm_system>
#     <personal>
#         <family-name>..</family-name>
#         <given-name>...</given-name>
#         <birth-date>...</birth-date>
#         <gender>...</gender>
#         <email/>
#     </personal>
#     <body-measurements>
#         <m value="46" name="height_knee"/>
#     </body-measurements>
# </vit>

####################################################################################################

class Measurements:

    ##############################################

    def __init__(self):

        self._items = []
        self._item_dict = {}
        self._globals = {}

    ##############################################

    @property
    def globals(self):
        return self._globals

    ##############################################

    def __iter__(self):
        return iter(self._items)

    ##############################################

    def __getitem__(self, name):
        return self._item_dict[name]

    ##############################################

    def add(self, *args, **kgwars):

        measurement = Measurement(self, *args, **kgwars)
        self._items.append(measurement)
        self._item_dict[measurement.name] = measurement
        if measurement.is_custom():
            self._item_dict[measurement.pythonised_name] = measurement

    ##############################################

    def _update_globals(self, measurement):

        self._globals[measurement.pythonised_name] = measurement.eval()

    ##############################################

    def eval(self):

        # Fixme: compute a graph from the ast to evaluate
        for item in self:
            item.eval()

    ##############################################

    def dump(self):

        for item in self:
            print(item.pythonised_name, '=', item.value)
            print('  =', item.eval())

####################################################################################################

class Measurement:

    ##############################################

    def __init__(self, measurements, name, value, full_name='', description=''):

        self._measurements = measurements
        self._name = name
        self._value = value
        self._full_name = full_name
        self._description = description

        self._ast = None
        self._code = None
        self._float = None # Fixme: or int

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def pythonised_name(self):
        if self.is_custom():
            return '__custom__' + self._name[1:]
        else:
            return self._name

    @property
    def value(self):
        return self._value

    @property
    def full_name(self):
        return self._full_name

    @property
    def description(self):
        return self._description

    ##############################################

    def is_float(self):

        try:
            float(self._value)
            return True
        except ValueError:
            return False

    ##############################################

    def is_custom(self):
        return self._name.startswith('@')

    ##############################################

    def find_name(self, start=0):

        value = self._value
        start = value.find('@', start)
        if start is -1:
            return None, None
        index = start + 1
        while index < len(value):
            c = value[index]
            if 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c in '_':
                index += 1
            else:
                break
        return value[start:index], index + 1

    ##############################################

    def compile(self):

        value = self._value

        # Python don't accept identifier starting with @
        # https://docs.python.org/3.5/reference/lexical_analysis.html#identifiers
        if '@' in value:
            custom_measurements = []
            start = 0
            while True:
                name, start = self.find_name(start)
                if name is None:
                    break
                else:
                    custom_measurements.append(name)
            for custom_measurement in custom_measurements:
                value = self.value.replace(custom_measurement, self._measurements[custom_measurement].pythonised_name)

        # Fixme: What is the (supported) grammar ?
        # http://beltoforion.de/article.php?a=muparser
        # http://beltoforion.de/article.php?a=muparserx
        self._ast = ast.parse(value, mode='eval')
        self._code = compile(self._ast, '<string>', mode='eval')

    ##############################################

    def eval(self):

        if self._code is None:
            self.compile()
            try:
                self._float = eval(self._code, self._measurements.globals)
            except NameError:
                self._float = None
            self._measurements._update_globals(self)
        return self._float

####################################################################################################

class VitParser:

    ##############################################

    def parse(self, val_path):

        with open(val_path, 'rb') as f:
            source = f.read()

        tree = etree.fromstring(source)

        measurements = Measurements()

        elements = self._get_xpath_element(tree, 'body-measurements')
        for element in elements:
             if element.tag == 'm':
                 attrs = element.attrib
                 measurements.add(attrs['name'], attrs['value'],
                                  attrs.get('full_name', ''),
                                  attrs.get('description', ''))
             else:
                 raise NotImplementedError

        return measurements

    ##############################################

    def _get_xpath_element(self, root, path):

        return root.xpath(path)[0]
