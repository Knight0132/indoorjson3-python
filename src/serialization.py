"""
File Name: serialization.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/13
"""

import numpy as np
from shapely.wkt import loads


class Graph:

    def __init__(self):
        self._properties = []
        self._cells = []
        self._connections = []
        self._layers = []
        self._rlineses = []
        self._hypergraph = {}

    @property
    def properties(self):
        return self._properties

    @property
    def cells(self):
        return self._cells

    @property
    def connections(self):
        return self._connections

    @property
    def layers(self):
        return self._layers

    @property
    def rlineses(self):
        return self._rlineses

    @property
    def hypergraph(self):
        return self._hypergraph

    class Cell:

        def __init__(self, cell_id, properties, space, node):
            self.__id = cell_id
            self._properties = properties
            self.__space = space
            self.__node = node

        @property
        def id(self):
            return self.__id

        @property
        def properties(self):
            return self._properties

        @property
        def space(self):
            return self.__space

        @property
        def node(self):
            return self.__node

        @classmethod
        def from_json(cls, json_data):
            return cls(json_data['$id'], json_data['properties'],
                       loads(json_data['space']), loads(json_data['node']))

        def to_json(self):
            return {
                '$id': self.__id,
                'properties': self._properties,
                'space': self.__space.wkt,
                'node': self.__node.wkt
            }

    class Connection:

        def __init__(self, connections_id, properties, source, target, bound,
                     edge):
            self.__id = connections_id
            self._properties = properties
            self.__source = source
            self.__target = target
            self.__bound = bound
            self.__edge = edge

        @property
        def id(self):
            return self.__id

        @property
        def properties(self):
            return self._properties

        @property
        def source(self):
            return self.__source

        @property
        def target(self):
            return self.__target

        @property
        def bound(self):
            return self.__bound

        @property
        def edge(self):
            return self.__edge

        @classmethod
        def from_json(cls, json_data):
            return cls(json_data['$id'], json_data['properties'],
                       json_data['fr'], json_data['to'],
                       loads(json_data['bound']), loads(json_data['edge']))

        def to_json(self):
            return {
                '$id': self.__id,
                'properties': self._properties,
                'source': self.__source,
                'target': self.__target,
                'bound': self.__bound.wkt,
                'edge': self.__edge.wkt
            }

    class Layer:
        def __init__(self, layer_id, cells):
            self.__id = layer_id
            self.__cells = cells

        @property
        def id(self):
            return self.__id

        @property
        def cells(self):
            return self.__cells

        @classmethod
        def from_json(cls, json_data):
            return cls(json_data['$id'], json_data['cells'])

        def to_json(self):
            return {
                '$id': self.__id,
                'cells': self.__cells
            }

    class Rlines:
        def __init__(self, rlines_id, cells, ins, outs, closure):
            self.__id = rlines_id
            self.__cells = cells
            self.__ins = ins
            self.__outs = outs
            self.__closure = closure

        @property
        def id(self):
            return self.__id

        @property
        def cells(self):
            return self.__cells

        @property
        def ins(self):
            return self.__ins

        @property
        def outs(self):
            return self.__outs

        @property
        def closure(self):
            return self.__closure

        @classmethod
        def from_json(cls, json_data):
            return cls(json_data['$id'], json_data['cells'], json_data['ins'], json_data['outs'], json_data['closure'])

        def to_json(self):
            return {
                '$id': self.__id,
                'cells': self.__cells,
                'ins': self.__ins,
                'outs': self.__outs,
                'closure': self.__closure
            }

    def set_properties(self, properties: dict):
        self._properties.append(properties)

    def add_cell(self, cell: Cell):
        if cell.id not in [c.id for c in self._cells]:
            self._cells.append(cell)
        else:
            raise ValueError('Cell id already exists')

    def add_connection(self, connection: Connection):
        if connection.id not in [c.id for c in self._connections]:
            if connection.source in [
                    c.id for c in self._cells
            ] and connection.target in [c.id for c in self._cells]:
                self._connections.append(connection)
            elif connection.source not in [
                    c.id for c in self._cells
            ] and connection.target in [c.id for c in self._cells]:
                raise ValueError('Source cell does not exist')
            elif connection.source in [
                    c.id for c in self._cells
            ] and connection.target not in [c.id for c in self._cells]:
                raise ValueError('Target cell does not exist')
            else:
                raise ValueError('Source and target cell do not exist')
        else:
            raise ValueError('Connection id already exists')

    def set_layers(self, layers: Layer):
        self._layers.append(layers)

    def set_rlineses(self, rlineses: Rlines):
        self._rlineses.append(rlineses)

    def get_incident_matrix(self):
        cells = self.cells
        connections = self.connections
        incident_matrix = np.zeros((len(cells), len(connections)), dtype=int)
        for j, connections in enumerate(connections):
            source = self.get_cell_from_id(connections.source)
            target = self.get_cell_from_id(connections.target)
            source_index = cells.index(source)
            target_index = cells.index(target)
            incident_matrix[source_index, j] = 1
            incident_matrix[target_index, j] = -1
        return incident_matrix

    def get_hypergraph(self):
        cells = self.cells
        connections = self.connections
        hypergraph = self._hypergraph
        hypergraph['hyperNodes'] = []
        hypergraph['hyperEdges'] = []
        incident_matrix = self.get_incident_matrix()
        incident_matrix_transpose = incident_matrix.T

        for hyperNode in connections:
            hypergraph['hyperNodes'].append(hyperNode.to_json())

        for j in range(incident_matrix_transpose.shape[1]):
            hyperEdge = {}
            inner_edge_id = {"ins": [], "outs": []}
            for i in range(incident_matrix_transpose.shape[0]):
                if incident_matrix_transpose[i, j] != 0:
                    if incident_matrix_transpose[i, j] == -1:
                        inner_edge_ins_id = connections[i].id
                        inner_edge_id["ins"].append(inner_edge_ins_id)
                    elif incident_matrix_transpose[i, j] == 1:
                        inner_edge_outs_id = connections[i].id
                        inner_edge_id["outs"].append(inner_edge_outs_id)
                    else:
                        raise ValueError('Incident matrix error')
            hyperEdge['id'] = cells[j].id
            hyperEdge['properties'] = cells[j].properties
            hyperEdge['space'] = cells[j].space.wkt
            hyperEdge['node'] = cells[j].node.wkt
            hyperEdge['inner_nodeset'] = inner_edge_id
            hypergraph['hyperEdges'].append(hyperEdge)

        self.set_hypergraph(hypergraph)

        return hypergraph

    def set_hypergraph(self, hypergraph):
        self._hypergraph = hypergraph

    def get_cell_from_id(self, cell_id):
        for cell in self.cells:
            if cell.id == cell_id:
                return cell
        return None

    def get_connection_from_id(self, connection_id):
        for connection in self.connections:
            if connection.id == connection_id:
                return connection
        return None

    def to_json(self):
        return {
            'properties': self._properties,
            'cells': [cell.to_json() for cell in self._cells],
            'connections': [
                connection.to_json() for connection in self._connections
            ],
            'layers': [layer.to_json() for layer in self._layers],
            'rlineses': [rlineses.to_json() for rlineses in self._rlineses]
        }

    @staticmethod
    def from_json(json_data):
        graph = Graph()
        graph._properties = json_data['properties']
        graph._cells = [
            Graph.Cell.from_json(cell) for cell in json_data['cells']
        ]
        graph._connections = [
            Graph.Connection.from_json(connection)
            for connection in json_data['connections']
        ]
        graph._layers = json_data['layers']
        graph._rlineses = json_data['rlineses']
        return graph
