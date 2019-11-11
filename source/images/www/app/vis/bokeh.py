#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import networkx as nx

from bokeh.plotting import figure
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx
from bokeh.palettes import Spectral4


from .schemas import NODE_ATTRS, EDGE_ATTRS


def render(graph):
    '''
    '''
    tooltips = [
        ("", "@desc")
    ]

    plot = figure(
        title="Граф взаимодействия",
        x_range=Range1d(-3.1, 3.1),
        y_range=Range1d(-3.1, 3.1),
        tooltips=tooltips,
        toolbar_location="above"
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
        EdgeAttrs = EDGE_ATTRS[edge_type]
        # enabled = edge_enabled[node]
        # enabled = extra.get("enabled", True)
        enabled = True
        edge_width[(start_node, end_node)] = EdgeAttrs.width(enabled, extra)
        edge_color[(start_node, end_node)] = EdgeAttrs.color(enabled, extra)
        edge_alpha[(start_node, end_node)] = EdgeAttrs.alpha(enabled, extra)
    nx.set_edge_attributes(graph, edge_width, "edge_width")
    nx.set_edge_attributes(graph, edge_color, "edge_color")
    nx.set_edge_attributes(graph, edge_alpha, "edge_alpha")

    node_size = {}
    node_fill_color = {}
    node_line_color = {}
    node_alpha = {}
    node_enabled = nx.get_node_attributes(graph, 'enabled')
    for node, extra in graph.nodes(data=True):
        node_type = extra.get("type")
        if not node_type or node_type not in NODE_ATTRS:
            print(f"Unknown node type '{node_type}' for node '{node}'", flush=True)
            continue
        NodeAttrs = NODE_ATTRS[node_type]
        enabled = node_enabled[node]
        node_alpha[node] = NodeAttrs.alpha(enabled, extra)
        node_size[node] = NodeAttrs.size(enabled, extra)
        node_fill_color[node] = NodeAttrs.fill_color(enabled, extra)
        node_line_color[node] = NodeAttrs.line_color(enabled, extra)
    nx.set_node_attributes(graph, node_size, "node_size")
    nx.set_node_attributes(graph, node_fill_color, "node_fill_color")
    nx.set_node_attributes(graph, node_line_color, "node_line_color")
    nx.set_node_attributes(graph, node_alpha, "node_alpha")

    graph_renderer = from_networkx(graph, nx.spring_layout, scale=2, center=(0, 0))
    graph_renderer.node_renderer.glyph = Circle(
        size="node_size",
        fill_color="node_fill_color",
        line_color="node_line_color",
        fill_alpha="node_alpha",
        line_alpha="node_alpha"
    )
    graph_renderer.edge_renderer.glyph = MultiLine(
        line_color="edge_color",
        line_alpha="edge_alpha",
        line_width="edge_width")
    plot.renderers.append(graph_renderer)
    return plot
