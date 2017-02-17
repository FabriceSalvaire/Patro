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

####################################################################################################

from itertools import tee

####################################################################################################

def pairwise(iterable):

    """ Return a generator which generate a pair wise list from an iterable.
    s -> (s[0],s[1]), (s[1],s[2]), ... (s[N-1],s[N])
    """

    prev = iterable[0]
    for x in iterable[1:]:
        yield prev, x
        prev = x

####################################################################################################

def multiwise(iterable, n=2):

    """ Return a generator which generate a multi wise list from an iterable.
    s -> (s[0],s[1],s[2],...), (s[1],s[2],s[3],...), ... (...,s[N-2],s[N-1],s[N])

    Examples::

      a = (1,2,3,4,5)

      list(multiwise(a, n=1))
      # [(1,), (2,), (3,), (4,), (5,)]

      list(multiwise(a, n=2))
      # [(1, 2), (2, 3), (3, 4), (4, 5)]

      list(multiwise(a, n=3))
      # [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

      # list(multiwise(a, n=4))
      # [(1, 2, 3, 4), (2, 3, 4, 5)]

      list(multiwise(a, n=5))
      # [(1, 2, 3, 4, 5)]

      list(multiwise(a, n=6))
      # []

      list(multiwise(a, n=0))
      # []

    """

    iterators = tee(iterable, n) # return n iterators on iterable
    # increment the iterators according to their positions
    for i, iterator in enumerate(iterators):
        for j in range(i):
            next(iterator, None)
    # return the aggregate
    return zip(*iterators)

####################################################################################################

def multiwise_interval(iterable_size, n=2):

    if n:
        upper_index = iterable_size -1
        offset = n -1
        upper_start_index = upper_index -offset
        if upper_start_index:
            return [slice(start_index, start_index +n) for start_index in range(upper_start_index +1)]
        elif upper_start_index == 0:
            return [slice(0, iterable_size),]

    return ()

####################################################################################################

def closed_pairwise(iterable):

    """ Return a generator which generate a closed pair wise list from an iterable.
    s -> (s[0],s[1]), (s[1],s[2]), ... (s[N], s[0])
    """

    closed_iterable = list(iterable) + [iterable[0]]

    # Fixme: duplicated code
    prev = closed_iterable[0]
    for x in closed_iterable[1:]:
        yield prev, x
        prev = x

####################################################################################################

class PairWiseManipulator(object):

    """ This class is a template to manipulate an iterable with a pair wise iterator concept.

    The method :meth:`do` must be implemented in super-class.
    """

    ##############################################

    def __init__(self):

         self._iterable = None

    ##############################################

    def _index_max(self):

        """ Return the index max of the list.
        """

        return len(self._iterable) -1

    ##############################################

    def next(self):

        """ Increment the index position.
        """

        self._index += 1

    ##############################################

    def end(self):

        """ Test if the index position is at the end of the list.
        """

        return self._index == self._index_max()

    ##############################################

    def pair(self):

        """ Return the pair from the current index position.
        """

        return self._iterable[self._index:self._index+2]

    ##############################################

    def del_item(self):

        """ Delete the item at the current index position.
        """

        del self._iterable[self._index]

    ##############################################

    def del_next_item(self):

        """ Delete the item at the next index position.
        """

        del self._iterable[self._index +1]

    ##############################################

    def apply(self, iterable):

        """ Iterate over the iterable and call the method :meth:`do` at each iteration until the
        last position is reached.  The index position is incremented if the method return
        :obj:`True`.
        """

        self._iterable = iterable

        self._index = 0
        while True:
            if self.do():
                self.next()
            if self.end():
                break

    ##############################################

    def do(self):

        """ Method called by method :meth:`apply` to manipulate the list. Must return a boolean.
        """

        raise NotImplementedError

####################################################################################################

def accumulate(iterable):

    """ Accumulate the values of an iterable to a new array. """

    accumulator = 0
    array = []
    for x in iterable:
        accumulator += x
        array.append(accumulator)

    return array
