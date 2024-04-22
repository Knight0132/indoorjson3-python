"""
File Name: visualization.py

Copyright (c) 2023 - 2024 IndoorJson

Author: Ziwei Xiang <knightzz1016@gmail.com>
Create Date: 2024/4/18
"""

import plotly.graph_objs as go
from plotly.offline import plot
from shapely import geometry as geo
from shapely.wkt import loads

from indoorspace import IndoorSpace


def graph_visualize(indoorSpace: IndoorSpace, filename: str = 'graph.html'):
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

    plot(fig, filename=filename)


def hypergraph_visualize(indoorSpace: IndoorSpace, filename: str = 'hypergraph.html'):
    fig = go.Figure()

    hypergraph = indoorSpace.get_hypergraph()

    for hyperEdge in hypergraph['hyperEdges']:
        cell = indoorSpace.get_cell_from_id(hyperEdge['id'])
        ins = hyperEdge['inner_nodeset']['ins']
        outs = hyperEdge['inner_nodeset']['outs']
        rlines = []
        rlines_group = geo.Polygon(cell.space)

        x_rlinesGroup, y_rlinesGroup = rlines_group.exterior.xy

        fig.add_trace(
            go.Scatter(x=list(x_rlinesGroup),
                       y=list(y_rlinesGroup),
                       fill='toself',
                       fillcolor='#C1DDDB',
                       line=dict(color='#81B3A9', width=2),
                       name='Rline Group',
                       text=str(cell.properties),
                       hoverinfo='text'))

        for ins_id in ins:
            insConnectionPoint = indoorSpace.get_connection_from_id(
                ins_id).bound.centroid

            for outs_id in outs:
                outsConnectionPoint = indoorSpace.get_connection_from_id(
                    outs_id).bound.centroid
                rline = geo.LineString(
                    [insConnectionPoint, outsConnectionPoint])
                rlines.append(rline)

        if 'closure' in hyperEdge:
            rlines_closure = hyperEdge['closure']
            for rlines_pairs in rlines_closure:
                insConnectionPoint = indoorSpace.get_connection_from_id(
                    rlines_pairs[0]).bound.centroid
                outsConnectionPoint = indoorSpace.get_connection_from_id(
                    rlines_pairs[1]).bound.centroid
                rline_closure = geo.LineString(
                    [insConnectionPoint, outsConnectionPoint])

                for rline in rlines:
                    if rline == rline_closure:
                        rlines.remove(rline)
                        break

        for rline in rlines:
            x_rline, y_rline = rline.xy
            fig.add_trace(
                go.Scatter(x=list(x_rline),
                           y=list(y_rline),
                           mode='lines',
                           line=dict(color='#81B3A9'),
                           name='Rline'))

    for hyperNode in hypergraph['hyperNodes']:
        connectionPoint = loads(hyperNode['bound'])
        x_hyperNode, y_hyperNode = geo.LineString(connectionPoint).centroid.xy

        fig.add_trace(
            go.Scatter(x=list(x_hyperNode),
                       y=list(y_hyperNode),
                       mode='markers',
                       marker=dict(size=10, color='#81B3A9'),
                       name='Connection Point',
                       text=str(hyperNode['properties']),
                       hoverinfo='text'))

    fig.update_layout(showlegend=False)

    plot(fig, filename=filename)
