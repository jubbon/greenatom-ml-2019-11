#!/usr/bin/env python
# -*- coding: utf-8 -*-


import networkx as nx

from data.unit import units
from data.staff import persons
from data.skill import skills, get_skills


def load_nodes() -> dict:
    ''' Load grapf nodes
    '''
    nodes = dict()
    for unit_uid, unit in units(level=-1):
        nodes.setdefault(unit_uid, dict(type='unit')).update(unit)

    for person_uid, person in persons():
        person_skills = get_skills(person_uid)
        nodes.setdefault(person_uid, dict(type='staff')).update(
            person,
            skills=person_skills)

    for skill_name in skills():
        nodes.setdefault(skill_name, dict()).update(type="skill")
    return nodes


def load_graph(unit=None, person=None):
    '''
    '''
    G = nx.Graph()

    nodes = load_nodes()
    for node_id, node in nodes.items():
        node_type = node.get("type")

        # Признак доступности узла при фильтрации
        node_enabled = True
        if node_type == "staff":
            if person and person["Табельный номер"] != node.get("Табельный номер"):
                node_enabled = False
        attrs = dict(
            type=node_type,
            enabled=node_enabled
            )
        G.add_node(node_id, **attrs)

    for node_id, node in nodes.items():
        node_type = node.get("type")
        if node_type == "staff":
            # Подразделение
            unit = node.get("Подразделение")
            if unit:
                G.add_edge(node_id, unit, type='unit')
            # Компетенции
            for skill_name, skill_value in node.get("skills", dict()).items():
                if skill_value:
                    G.add_edge(node_id, skill_name, type='skill', value=1)
        elif node_type == "unit":
            unit = node.get("Тип") + ' ' + node.get("Номер")
            parent = node.get("Родительская структура")
            if unit and parent:
                G.add_edge(unit, parent, type='unit')
    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges", flush=True)
    return G
