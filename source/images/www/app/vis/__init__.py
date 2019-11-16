#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import streamlit as st

from .schemas import NODE_ATTRS, EDGE_ATTRS


@st.cache
def custom_graph(graph: nx.Graph):
    '''
    '''
    assert isinstance(graph, nx.Graph)
    graph = graph.copy()

    edge_attr = {}
    edge_color = {}
    edge_alpha = {}
    edge_width = {}
    for start_node, end_node, extra in graph.edges(data=True):
        edge_type = extra.get("type")
        EdgeAttrs = EDGE_ATTRS[edge_type]
        # enabled = edge_enabled[node]
        enabled = extra.get("enabled", True)
        edge_width[(start_node, end_node)] = EdgeAttrs.width(enabled, extra)
        edge_color[(start_node, end_node)] = EdgeAttrs.color(enabled, extra)
        edge_alpha[(start_node, end_node)] = EdgeAttrs.alpha(enabled, extra)
    if edge_width:
        nx.set_edge_attributes(graph, edge_width, "edge_width")
        edge_attr.update(line_width="edge_width")
    if edge_color:
        nx.set_edge_attributes(graph, edge_color, "edge_color")
        edge_attr.update(line_color="edge_color")
    if edge_alpha:
        nx.set_edge_attributes(graph, edge_alpha, "edge_alpha")
        edge_attr.update(line_alpha="edge_alpha")

    node_attr = {}
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
    if node_size:
        nx.set_node_attributes(graph, node_size, "node_size")
        node_attr.update(size="node_size")
    if node_fill_color:
        nx.set_node_attributes(graph, node_fill_color, "node_fill_color")
        node_attr.update(fill_color="node_fill_color")
    if node_line_color:
        nx.set_node_attributes(graph, node_line_color, "node_line_color")
        node_attr.update(line_color="node_line_color")
    if node_alpha:
        nx.set_node_attributes(graph, node_alpha, "node_alpha")
        node_attr.update(fill_alpha="node_alpha", line_alpha="node_alpha")

    return graph, node_attr, edge_attr


def render_graph(graph: nx.Graph, title: str, engine: str, layout_attr: {}):
    '''
    '''
    assert isinstance(graph, nx.Graph)

    if engine == "bokeh":
        from .bokeh import render
    elif engine == "plotly":
        from .plotly import render
    else:
        raise RuntimeError("Unknown render engine")

    attr = dict(layout_function=nx.spring_layout)
    attr.update(layout_attr)

    graph, node_attr, edge_attr = custom_graph(graph)
    return render(graph, title, attr, node_attr, edge_attr)
