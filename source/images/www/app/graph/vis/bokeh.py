#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx

from bokeh.plotting import figure
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx


def render(graph: nx.Graph, title: str, attr: dict, node_attr: dict, edge_attr: dict):
    '''
    '''
    assert isinstance(graph, nx.Graph)
    print(f"Render graph '{title}' (nodes: {graph.number_of_nodes()}, edges: {graph.number_of_edges()}, attr: {attr}", flush=True)

    tooltips = [
        ("", "@desc")
    ]

    scale = attr.get("scale", 1) * 1.1
    plot = figure(
        title=title,
        width=800,
        x_range=Range1d(-scale, scale),
        y_range=Range1d(-scale, scale),
        tooltips=tooltips,
        toolbar_location="above"
        )
    plot.xgrid.visible = False
    plot.ygrid.visible = False
    plot.xaxis.visible = False
    plot.yaxis.visible = False

    renderer = from_networkx(graph, **attr)
    if node_attr:
        renderer.node_renderer.glyph = Circle(**node_attr)
    if edge_attr:
        renderer.edge_renderer.glyph = MultiLine(**edge_attr)
    plot.renderers.append(renderer)
    return plot
