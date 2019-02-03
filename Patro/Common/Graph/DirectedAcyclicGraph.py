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

"""This module implements a directed acyclic graph.

"""

####################################################################################################

# import logging

####################################################################################################

class DirectedAcyclicGraphNode:

    """Class to define a node of a DAG."""

    ##############################################

    def __init__(self, node_id, data=None):

        self._node_id = node_id
        self._data = data

        self._ancestors = set()
        self._descendants = set()

    ##############################################

    def __repr__(self):
        return '{} {}'.format(self.__class__.__name__, self._node_id)

    ##############################################

    @property
    def node_id(self):
        return self._node_id

    @property
    def data(self):
        return self._data

    @property
    def ancestor(self):
        return self._ancestor

    @property
    def descendants(self):
        return self._descendants

    ##############################################

    @property
    def is_root(self):
        return not self._ancestors

    ##############################################

    @property
    def is_leaf(self):
        return not self._descendants

    ##############################################

    def disconnect_ancestor(self, node):
        self._ancestors.remove(node)
        node.descendants.remove(self)

    ##############################################

    def connect_ancestor(self, node):
        self._ancestors.add(node)
        node._descendants.add(self)

    ##############################################

    def breadth_first_search(self):

        # Fixme: Name ?

        queue = [self]
        visited = set((self,))
        while queue:
            node = queue.pop(0)
            yield node
            for descendant in node._descendants:
                if descendant not in visited:
                    queue.append(descendant)
                    visited.add(descendant)

####################################################################################################

class DirectedAcyclicGraph:

    """Class to implement a DAG."""

    ##############################################

    def __init__(self):
        self._nodes = {}

    ##############################################

    def __iter__(self):
        return iter(self._nodes.values())

    ##############################################

    def __getitem__(self, node_id):
        return self._nodes[node_id]

    ##############################################

    def add_node(self, node_id, **kwargs):

        if node_id not in self._nodes:
            node = DirectedAcyclicGraphNode(node_id, **kwargs)
            self._nodes[node_id] = node
            return node
        else:
            raise NameError("Node {} is already registered".format(node_id))

    ##############################################

    def add_edge(self, ancestor, descendant):
        descendant.connect_ancestor(ancestor)

    ##############################################

    def roots(self):
        return [node for node in self if node.is_root]

    ##############################################

    def leafs(self):
        return [node for node in self if node.is_leaf]

    ##############################################

    def topological_sort(self):

        sorted_list = [] # reversed
        unmarked_nodes = set(self._nodes.values())
        marked_nodes = set()
        temporary_marked_nodes = set()

        def visit(node):
            if node in temporary_marked_nodes:
                raise NameError('Not a DAG')
            if node not in marked_nodes:
                temporary_marked_nodes.add(node)
                for descendant in node._descendants:
                    visit(descendant)
                marked_nodes.add(node)
                temporary_marked_nodes.remove(node)
                sorted_list.append(node)

        while unmarked_nodes:
            node = unmarked_nodes.pop()
            visit(node)

        sorted_list.reverse()

        return sorted_list
