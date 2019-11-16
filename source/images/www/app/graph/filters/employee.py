#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx

from smart_hr.data.unit import get_unit, parents


def filter_graph(graph: nx.Graph, employee) -> nx.Graph:
    '''
    '''
    assert graph
    assert employee
    enabled_units = None
    if employee:
        unit = get_unit(employee.unit)
        parent_units = list(parents(unit))
        enabled_units = list([unit.fullname, ]) + [unit.fullname for unit in parent_units]

    node_enabled = dict()
    node_fullname = nx.get_node_attributes(graph, 'fullname')
    node_types = nx.get_node_attributes(graph, 'type')
    for node_uid, fullname in node_fullname.items():
        node_type = node_types[node_uid]
        if node_type == "unit":
            if enabled_units and fullname not in enabled_units:
                node_enabled[node_uid] = False
        elif node_type == "staff":
            node_enabled[node_uid] = False
    nx.set_node_attributes(graph, node_enabled, name="enabled")
    return graph
