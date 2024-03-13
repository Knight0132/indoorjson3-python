"""
File Name: test_deserialization.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/3/13
"""

import json
import sys
import os

sys.path.append(os.path.abspath('../src'))

from serialization import Graph

with open('example.json', 'r', encoding='utf-8') as f:
    graph_dict = json.load(f)

graph = Graph().from_json(graph_dict)
hypergraph = graph.get_hypergraph()

with open('test_hypergraph.json', 'w', encoding='utf-8') as f:
    json.dump(hypergraph, f, indent=4)
