#!/usr/bin/env python
# -*- coding: utf-8 -*-


import networkx as nx

from data.unit import get_unit, units, parents
from data.staff import persons
from data.skill import skills, get_skills


def load_nodes() -> dict:
    ''' Load grapf nodes
    '''
    nodes = dict()
    for unit_uid, unit in units(level=-1):
        nodes.setdefault(unit_uid, dict(type='unit')).update(
            unit.to_dict(),
            desc=unit.desc)

    for person_uid, person in persons():
        person_skills = get_skills(person_uid)
        nodes.setdefault(person_uid, dict(type='staff')).update(
            person.to_dict(),
            desc=person.desc,
            skills=person_skills.to_dict())

    for skill_name in skills():
        nodes.setdefault(skill_name, dict(type='skill')).update(
            desc=skill_name)
    return nodes


def load_graph(unit=None, person=None):
    '''
    '''
    G = nx.Graph()

    nodes = load_nodes()
    for node_id, node in nodes.items():
        node_type = node.get("type")

        # # Признак доступности узла при фильтрации
        # node_enabled = True
        # if node_type == "staff":
        #     if person and person["Табельный номер"] != node.get("Табельный номер"):
        #         node_enabled = False
        attrs = node
        attrs.update(type=node_type, enabled=True)
        G.add_node(node_id, **attrs)

    for node_id, node in nodes.items():
        node_type = node.get("type")
        if node_type == "staff":
            # Подразделение
            unit = node["unit"]
            if unit:
                G.add_edge(node_id, unit, type='unit')
            # Компетенции
            for skill_name, skill_value in node.get("skills", dict()).items():
                if skill_value:
                    G.add_edge(node_id, skill_name, type='skill', value=1)
        elif node_type == "unit":
            unit = node.get("fullname")
            parent = node.get("parent")
            if unit and parent:
                G.add_edge(unit, parent, type='unit')
    return G


def filter_graph_for_person(graph, person):
    '''
    '''
    assert person
    enabled_units = None
    if person:
        unit = get_unit(person.unit)
        parent_units = list(parents(unit))
        enabled_units = list([unit["unit_uid"], ]) + [unit["unit_uid"] for unit in parent_units]

    node_enabled = dict()
    node_extras = nx.get_node_attributes(graph, 'extra')
    for node_uid, extra in node_extras.items():
        node_type = extra["type"]
        if node_type == "unit":
            unit_uid = extra["unit_uid"]
            if enabled_units and unit_uid not in enabled_units:
                node_enabled[node_uid] = False
            else:
                node_enabled[node_uid] = True
    nx.set_node_attributes(graph, node_enabled, name="enabled")

    return graph
