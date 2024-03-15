"""
File Name: indoorspace.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/14
"""

import json
import numpy as np
from cell import Cell
from connection import Connection
from layer import Layer
from rlines import Rlines
from typing import List, Dict


class IndoorSpace:

    def __init__(self):
        self._properties: Dict = {}
        self._cells: List[Cell] = []
        self._connections: List[Connection] = []
        self._layers: List[Layer] = []
        self._rlineses: List[Rlines] = []
        self._hypergraph: Dict = {}

    @property
    def properties(self) -> Dict:
        return self._properties

    @property
    def cells(self) -> List[Cell]:
        return self._cells

    @property
    def connections(self) -> List[Connection]:
        return self._connections

    @property
    def layers(self) -> List[Layer]:
        return self._layers

    @property
    def rlineses(self) -> List[Rlines]:
        return self._rlineses

    @property
    def hypergraph(self) -> Dict:
        return self._hypergraph

    def set_properties(self, properties: Dict):
        self._properties = properties

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
        for j, connection in enumerate(connections):
            source = self.get_cell_from_id(connection.source)
            target = self.get_cell_from_id(connection.target)
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

    def to_json(self) -> str:
        result = {}
        for key, value in self.__dict__.items():
            if key == '_hypergraph':
                continue
            elif key == '_properties':
                result[key.strip('_')] = value
            else:
                result[key.strip('_')] = [item.to_json() for item in value]
        return json.dumps(result, indent=4, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'IndoorSpace':
        json_data = json.loads(json_str)
        instance = cls()
        for key, value in json_data.items():
            if key == 'properties':
                setattr(instance, f"_{key}", value)
            elif key == 'rlineses':
                setattr(instance, f"_{key}", [eval(key.capitalize()[:-2]).from_json(item) for item in value])
            else:
                setattr(instance, f"_{key}", [eval(key.capitalize()[:-1]).from_json(item) for item in value])
        return instance
