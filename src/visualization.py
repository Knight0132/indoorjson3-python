"""
File Name: visualization.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/4/18
"""

from indoorspace import IndoorSpace
from shapely import geometry as geo

import plotly.graph_objs as go
from plotly.offline import plot


def graph_visualize(indoorSpace: IndoorSpace):
    fig = go.Figure()

    for cell in indoorSpace.cells:
        cell_space = geo.Polygon(cell.space)
        cell_node = geo.Point(cell.node)
        x1, y1 = cell_space.exterior.xy
        x2, y2 = cell_node.xy

        fig.add_trace(
            go.Scatter(x=list(x1), y=list(y1), fill='toself', name='Space'))
        fig.add_trace(
            go.Scatter(x=list(x2),
                       y=list(y2),
                       mode='markers',
                       name='Cell',
                       text=str(cell.properties),
                       hoverinfo='text'))

    for connection in indoorSpace.connections:
        connection_bound = geo.LineString(connection.bound)
        connection_edge = geo.LineString(connection.edge)
        x1, y1 = connection_bound.xy
        x2, y2 = connection_edge.xy

        fig.add_trace(
            go.Scatter(x=list(x1), y=list(y1), mode='lines', name='Boundary'))
        fig.add_trace(
            go.Scatter(x=list(x2),
                       y=list(y2),
                       mode='lines',
                       name='Edge',
                       text=str(connection.properties),
                       hoverinfo='text'))

    fig.update_layout(showlegend=False)

    plot(fig, filename='graph.html')


def hypergraph_visualize(indoorSpace: IndoorSpace):
    fig = go.Figure()

    hypergraph = indoorSpace.get_hypergraph()

    for hyperEdge in hypergraph['hyperEdges']:
        cell = indoorSpace.get_cell_from_id(hyperEdge['id'])
        connection_dict = hyperEdge['inner_nodeset']
        rlines_group = geo.Polygon(cell.space)

        x1, y1 = rlines_group.exterior.xy

        for value in connection_dict.values():
            for connection_id in value:
                connection = indoorSpace.get_connection_from_id(connection_id)
                connection_point = connection.bound.centroid
                x2, y2 = connection_point.xy

                fig.add_trace(
                    go.Scatter(x=list(x2),
                               y=list(y2),
                               mode='markers',
                               name='Connection Point',
                               text=str(connection.properties),
                               hoverinfo='text'))

        if 'closure' in hyperEdge:
            rlines_closure = hyperEdge['closure']
            for rlines_pairs in rlines_closure:
                ins_connection_point = indoorSpace.get_connection_from_id(rlines_pairs[0]).bound.centroid
                outs_connection_point = indoorSpace.get_connection_from_id(rlines_pairs[1]).bound.centroid
                rline = geo.LineString([ins_connection_point, outs_connection_point])
                x, y = rline.xy
                fig.add_trace(
                    go.Scatter(x=list(x),
                               y=list(y),
                               mode='lines',
                               name='Rline',
                               text=str(rlines_pairs),
                               hoverinfo='text'))

        fig.add_trace(
            go.Scatter(x=list(x1),
                       y=list(y1),
                       fill='toself',
                       name='Rline Group',
                       text=str(cell.properties),
                       hoverinfo='text'))

    fig.update_layout(showlegend=False)

    plot(fig, filename='hypergraph.html')
