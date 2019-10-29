#!/usr/bin/env python
# -*- coding: utf-8 -*-


import networkx as nx


def get_graph():
    ''' Return fake graph
    '''
    return nx.random_geometric_graph(250, 0.125)
