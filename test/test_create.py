"""
File Name: test_create.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/14
"""

import json
from shapely.wkt import loads
import sys
import os

sys.path.append(os.path.abspath('../src'))

from serialization import Graph

graph = Graph()

properties = {
    "name": "indoorjson3-python",
    "labels": ["indoorgml", "GIS"],
    "language": ["English", "中文", "한국어"],
    "author": {"name": "Ziwei Xiang", "email": "knightzz1016@gmail.com"}
}

cells = []

c1_id = "c1"
c1_properties = {"roomNumber": "1101"}
c1_space = loads("POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))")
c1_node = loads("POINT (0.5 0.5)")
cell1 = graph.Cell(c1_id, c1_properties, c1_space, c1_node)
cells.append(cell1)

c2_id = "c2"
c2_properties = {"roomNumber": "1102"}
c2_space = loads("POLYGON ((1 0, 2 0, 2 1, 1 1, 1 0))")
c2_node = loads("POINT (1.5 0.5)")
cell2 = graph.Cell(c2_id, c2_properties, c2_space, c2_node)
cells.append(cell2)

c3_id = "c3"
c3_properties = {"roomNumber": "1103"}
c3_space = loads("POLYGON ((0 1, 1 1, 1 2, 0 2, 0 1))")
c3_node = loads("POINT (0.5 1.5)")
cell3 = graph.Cell(c3_id, c3_properties, c3_space, c3_node)
cells.append(cell3)

for cell in cells:
    graph.add_cell(cell)

connections = []

con1_id = "conn1-2"
con1_properties = {"type": "door", "开放时间": "全天", "오픈 시간": "하루 종일"}
con1_fr = c1_id
con1_to = c2_id
con1_bound = loads("LINESTRING (1 0, 1 1)")
con1_edge = loads("LINESTRING (0.5 0.5, 1.5 0.5)")
connection1 = graph.Connection(con1_id, con1_properties, con1_fr, con1_to, con1_bound, con1_edge)
connections.append(connection1)

con2_id = "conn3-1"
con2_properties = {"type": "window"}
con2_fr = c3_id
con2_to = c1_id
con2_bound = loads("LINESTRING (1 0, 1 1)")
con2_edge = loads("LINESTRING (0.5 0.5, 1.5 0.5)")
connection2 = graph.Connection(con2_id, con2_properties, con2_fr, con2_to, con2_bound, con2_edge)
connections.append(connection2)

for connection in connections:
    graph.add_connection(connection)

layer_id = "layer"
layer_cells = [cell.id for cell in cells]
layer = graph.Layer(layer_id, layer_cells)
graph.set_layers(layer)

hypergraph = graph.get_hypergraph()
for hyperEdge in hypergraph['hyperEdges']:
    i = 0
    if hyperEdge["inner_nodeset"]["ins"] and hyperEdge["inner_nodeset"]["outs"]:
        i += 1
        rlines_id = str("rlines") + str(i)
        rlines_cell = hyperEdge["id"]
        rlines_ins = hyperEdge["inner_nodeset"]["ins"]
        rlines_outs = hyperEdge["inner_nodeset"]["outs"]
        rlines_closure = []
        rlines = graph.Rlines(rlines_id, rlines_cell, rlines_ins, rlines_outs, rlines_closure)
        graph.set_rlineses(rlines)

with open('test_created.json', 'w', encoding='utf-8') as f:
    json.dump(graph.to_json(), f, indent=4)
