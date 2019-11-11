#!/usr/bin/env python
# -*- coding: utf-8 -*-


def render_graph(graph, engine: str, center=(0, 0)):
    '''
    '''
    assert graph

    if engine == "bokeh":
        from .bokeh import render
    elif engine == "plotly":
        from .plotly import render
    else:
        raise RuntimeError("Unknown render engine")
    return render(graph, center=center)
