#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import networkx as nx

from bokeh.plotting import figure
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx
from bokeh.palettes import Spectral4


def render(graph):
    '''
    '''
    plot = figure(
        title="Граф взаимодействия",
        x_range=Range1d(-3.1, 3.1),
        y_range=Range1d(-3.1, 3.1)
        )
    plot.xgrid.visible = False
    plot.ygrid.visible = False
    plot.xaxis.visible = False
    plot.yaxis.visible = False

    edge_color = {}
    edge_alpha = {}
    edge_width = {}
    for start_node, end_node, extra in graph.edges(data=True):
        edge_type = extra.get("type")
        color = "black"
        if edge_type == "skill":
            color = "gray"
        elif edge_type == "unit":
            color = "blue"
        edge_color[(start_node, end_node)] = color

        alpha = 1
        if edge_type == "skill":
            alpha = extra.get("value", 0) / 10.
        elif edge_type == "unit":
            alpha = 0.7
        edge_alpha[(start_node, end_node)] = alpha

        width = 1
        edge_width[(start_node, end_node)] = width
    nx.set_edge_attributes(graph, edge_color, "edge_color")
    nx.set_edge_attributes(graph, edge_alpha, "edge_alpha")
    nx.set_edge_attributes(graph, edge_width, "edge_width")

    node_size = {}
    node_color = {}
    for node, extra in graph.nodes(data=True):
        node_type = extra.get("type")
        color = "black"
        size = 10
        if node_type == "skill":
            color = "red"
            size = 20
        elif node_type == "unit":
            color = "blue"
            size = 14
        node_size[node] = size
        node_color[node] = color
    nx.set_node_attributes(graph, node_size, "node_size")
    nx.set_node_attributes(graph, node_color, "node_color")

    graph_renderer = from_networkx(graph, nx.spring_layout, scale=2, center=(0, 0))
    graph_renderer.node_renderer.glyph = Circle(
        size="node_size",
        fill_color="node_color"
    )
    graph_renderer.edge_renderer.glyph = MultiLine(
        line_color="edge_color",
        line_alpha="edge_alpha",
        line_width="edge_width")
    plot.renderers.append(graph_renderer)
    return plot
