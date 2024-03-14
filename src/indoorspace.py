"""
File Name: indoorspace.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/14
"""

import numpy as np
from cell import Cell
from connection import Connection
from layer import Layer
from rlines import Rlines


class IndoorSpace:

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

    def get_hypergraph_incidence_matrix(self):
        return self.get_incident_matrix().T

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
            inner_edge_id = {'ins': [], 'outs': []}
            for i in range(incident_matrix_transpose.shape[0]):
                if incident_matrix_transpose[i, j] != 0:
                    if incident_matrix_transpose[i, j] == -1:
                        inner_edge_ins_id = connections[i].id
                        inner_edge_id['ins'].append(inner_edge_ins_id)
                    elif incident_matrix_transpose[i, j] == 1:
                        inner_edge_outs_id = connections[i].id
                        inner_edge_id['outs'].append(inner_edge_outs_id)
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
            'rlineses': [rlines.to_json() for rlines in self._rlineses]
        }

    @staticmethod
    def from_json(json_data):
        indoorSpace = IndoorSpace()

        setattr(indoorSpace, '_properties', json_data['properties'])

        class_map = {
            '_cells': Cell,
            '_connections': Connection,
            '_layers': Layer,
            '_rlineses': Rlines
        }

        for attr, cls in class_map.items():
            items = json_data[attr.lstrip('_')]
            setattr(indoorSpace, attr, [cls.from_json(item) for item in items])

        return indoorSpace
