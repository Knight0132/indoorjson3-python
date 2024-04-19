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
            go.Scatter(x=list(x1),
                       y=list(y1),
                       fill='toself',
                       fillcolor='#C1DDDB',
                       line=dict(color='#81B3A9', width=2),
                       name='Space'))
        fig.add_trace(
            go.Scatter(x=list(x2),
                       y=list(y2),
                       mode='markers',
                       marker=dict(size=10, color='#81B3A9'),
                       name='Cell',
                       text=str(cell.properties),
                       hoverinfo='text'))

    for connection in indoorSpace.connections:
        connection_bound = geo.LineString(connection.bound)
        connection_edge = geo.LineString(connection.edge)
        x1, y1 = connection_bound.xy
        x2, y2 = connection_edge.xy

        fig.add_trace(
            go.Scatter(x=list(x1),
                       y=list(y1),
                       mode='lines',
                       line=dict(color='#81B3A9', width=2),
                       name='Boundary',
                       text=str(connection.properties),
                       hoverinfo='text'))
        fig.add_trace(
            go.Scatter(x=list(x2),
                       y=list(y2),
                       mode='lines',
                       line=dict(color='#81B3A9', width=2),
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
        ins = hyperEdge['inner_nodeset']['ins']
        outs = hyperEdge['inner_nodeset']['outs']
        rlines = []
        rlines_group = geo.Polygon(cell.space)

        x1, y1 = rlines_group.exterior.xy

        fig.add_trace(
            go.Scatter(x=list(x1),
                       y=list(y1),
                       fill='toself',
                       fillcolor='#C1DDDB',
                       line=dict(color='#81B3A9', width=2),
                       name='Rline Group',
                       text=str(cell.properties),
                       hoverinfo='text'))

        for ins_id in ins:
            ins_connection_point = indoorSpace.get_connection_from_id(
                ins_id).bound.centroid
            x2, y2 = ins_connection_point.xy

            for outs_id in outs:
                outs_connection_point = indoorSpace.get_connection_from_id(
                    outs_id).bound.centroid
                rline = geo.LineString(
                    [ins_connection_point, outs_connection_point])
                rlines.append(rline)

                x3, y3 = outs_connection_point.xy

                fig.add_trace(
                    go.Scatter(x=list(x3),
                               y=list(y3),
                               mode='markers',
                               marker=dict(size=10, color='#81B3A9'),
                               name='Connection Point',
                               text=str(
                                   indoorSpace.get_connection_from_id(
                                       outs_id).properties),
                               hoverinfo='text'))

            fig.add_trace(
                go.Scatter(
                    x=list(x2),
                    y=list(y2),
                    mode='markers',
                    marker=dict(size=10, color='#81B3A9'),
                    name='Connection Point',
                    text=str(
                        indoorSpace.get_connection_from_id(ins_id).properties),
                    hoverinfo='text'))

        if 'closure' in hyperEdge:
            rlines_closure = hyperEdge['closure']
            for rlines_pairs in rlines_closure:
                ins_connection_point = indoorSpace.get_connection_from_id(
                    rlines_pairs[0]).bound.centroid
                outs_connection_point = indoorSpace.get_connection_from_id(
                    rlines_pairs[1]).bound.centroid
                rline_closure = geo.LineString(
                    [ins_connection_point, outs_connection_point])

                for rline in rlines:
                    if rline == rline_closure:
                        rlines.remove(rline)
                        break

        for rline in rlines:
            x, y = rline.xy
            fig.add_trace(
                go.Scatter(x=list(x),
                           y=list(y),
                           mode='lines',
                           line=dict(color='#81B3A9'),
                           name='Rline'))

    fig.update_layout(showlegend=False)

    plot(fig, filename='hypergraph.html')
