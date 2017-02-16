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

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Evaluator:

    _logger = _module_logger.getChild('Evaluator')

    ##############################################

    def __init__(self, measurements):

        self._measurements = measurements

        self._cache  = {}

    ##############################################

    @property
    def measurements(self):
        return self._measurements

    @property
    def cache(self):
        return self._cache

    ##############################################

    def _update_cache(self, named_expression):

        self._cache[named_expression.name] = named_expression.value


####################################################################################################

class Expression:

    _logger = _module_logger.getChild('Expression')

    ##############################################

    def __init__(self, expression, evaluator=None):

        self._expression = expression
        self._evaluator = evaluator

        self._ast = None
        self._code = None
        self._value = None

    ##############################################

    @property
    def expression(self):
        return self._expression

    ##############################################

    def __str__(self):
        return self._expression

    ##############################################

    def is_float(self):

        try:
            float(self._expression)
            return True
        except ValueError:
            return False

    ##############################################

    def find_name(self, start=0):

        expression = self._expression
        start = expression.find('@', start)
        if start is -1:
            return None, None
        index = start + 1
        while index < len(expression):
            c = expression[index]
            if 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c in '_':
                index += 1
            else:
                break
        return expression[start:index], index + 1

    ##############################################

    def compile(self):

        expression = self._expression

        # Python don't accept identifier starting with @
        # https://docs.python.org/3.5/reference/lexical_analysis.html#identifiers
        if '@' in expression:
            custom_measurements = []
            start = 0
            while True:
                name, start = self.find_name(start)
                if name is None:
                    break
                else:
                    custom_measurements.append(name)
            for measurement in custom_measurements:
                expression = self.expression.replace(measurement, self._evaluator.measurements[measurement].name)

        # Fixme: What is the (supported) grammar ?
        # http://beltoforion.de/article.php?a=muparser
        # http://beltoforion.de/article.php?a=muparserx
        self._ast = ast.parse(expression, mode='eval')
        self._code = compile(self._ast, '<string>', mode='eval')

    ##############################################

    def eval(self):

        self.compile()
        try:
            self._value = eval(self._code, self._evaluator.cache)
        except NameError:
            self._value = None
        self._logger.info('Eval {} = {}'.format(self._expression, self._value))

    ##############################################

    @property
    def value(self):

        if self._code is None:
            self.eval()
        return self._value

####################################################################################################

class NamedExpression(Expression):

    ##############################################

    def __init__(self, name, expression, evaluator=None):

        Expression.__init__(self, expression, evaluator)
        self._name = name

    ##############################################

    @property
    def name(self):
        return self._name
