#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import plotly.graph_objects as go


def render(graph, title, center=(0, 0)):
    '''
    '''
    assert graph

    traces = list()

    def vis_nodes(graph, pos):
        ''' Visualize nodes
        '''
        node_x = []
        node_y = []
        node_color = []
        for n, node in enumerate(graph.nodes()):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_color.append("red" if n % 2 else "green")

        return go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=node_color,
                size=10,
                # colorbar=dict(
                #     thickness=15,
                #     title='Node Connections',
                #     xanchor='left',
                #     titleside='right'),
                line_width=2)
            )

    def vis_edges(graph, pos):
        ''' Visualize edges
        '''
        edge_x = []
        edge_y = []
        edge_color = []

        for n, edge in enumerate(graph.edges()):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)
            # edge_color.append("black" if n % 3 else "gray")
        return go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color="gray"),
            hoverinfo='none',
            mode='lines'
        )

    pos = nx.spring_layout(graph)
    traces.append(vis_edges(graph, pos))
    traces.append(vis_nodes(graph, pos))
    return traces