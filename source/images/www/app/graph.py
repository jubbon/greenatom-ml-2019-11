#!/usr/bin/env python
# -*- coding: utf-8 -*-


import networkx as nx

from data import load_graph


def get_graph():
    ''' Return fake graph
    '''
    graph = load_graph("/data/hr.xls")
    print(f"Loaded graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges", flush=True)
    return graph
    # return nx.random_geometric_graph(2500, 0.0125)
