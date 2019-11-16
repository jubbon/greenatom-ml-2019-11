#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import streamlit as st

from smart_hr.data.unit import get_unit, units, parents
from smart_hr.data.staff import persons
from smart_hr.data.skill import skills, get_skills


def nodes(node_types: list) -> dict:
    ''' Generate nodes
    '''
    if not node_types or "unit" in node_types:
        for unit_uid, unit in units(level=-1):
            data = dict(type="unit")
            data.update(unit.to_dict(), desc=unit.desc)
            if 'projects' in data:
                del data['projects']
            yield unit_uid, data

    if not node_types or "staff" in node_types:
        for person_uid, person in persons():
            person_skills = get_skills(person_uid)
            data = dict(type="staff")
            data.update(
                person.to_dict(),
                level=person_skills.mean(),
                desc=person.desc,
                skills=person_skills.to_dict()
            )
            if 'projects' in data:
                del data['projects']
            yield person_uid, data

    if not node_types or "skill" in node_types:
        for skill_name, skill_level in skills():
            data = dict(type="skill")
            data.update(
                level=skill_level,
                desc=f"{skill_name} (уровень {skill_level})"
            )
            yield skill_name, data


GRAPHS = {
    "test": {
        "title": "Демо",
        "init": nx.karate_club_graph,
    },
    "staff-unit": {
        "title": "Сотрудник-подразделение",
        "init": nx.Graph,
        "nodes": [
            "staff",
            "unit"
        ],
        "edges": []
    },
    "staff-skill": {
        "title": "Сотрудник-компетенции",
        "init": nx.Graph,
        "nodes": [
            "staff",
            "skill"
        ],
        "edges": []
    },
    "skill-staff-unit": {
        "title": "Сотрудник-компетенции-подразделение",
        "init": nx.Graph,
        "nodes": [
            "staff",
            "skill",
            "unit"
        ],
        "edges": []
    }
}


def load_graph(uid: str, config: dict) -> nx.Graph:
    '''
    '''
    G = config.get('init', nx.Graph)()
    node_types = config.get("nodes")
    assert isinstance(node_types, list)
    for node_uid, node in nodes(node_types):
        node_type = node["type"]
        node.update(enabled=True)
        G.add_node(node_uid, **node)

        if node_type == "staff":
            # Подразделение
            unit = node["unit"]
            if unit and uid in ("staff-unit", "skill-staff-unit"):
                G.add_edge(node_uid, unit, type='unit')
            # Компетенции
            skills = node.pop("skills", dict())
            for skill_name, skill_value in skills.items():
                assert skill_value in range(0, 10)
                if skill_value and uid in ("staff-skill", "skill-staff-unit"):
                    G.add_edge(node_uid, skill_name, type='skill', value=skill_value)
        elif node_type == "unit":
            unit = node.get("fullname")
            parent = node.get("parent")
            if unit and parent and uid in ("staff-unit", "skill-staff-unit"):
                G.add_edge(unit, parent, type='unit')
    return G


def load_graphs(uids: list):
    '''
    '''
    for uid in uids:
        if uid not in GRAPHS:
            print(f"Graph with uid '{uid}' not found", flush=True)
            continue
        config = GRAPHS[uid]
        yield uid, config.get("title", uid), load_graph(uid, config)


def filter_graph_for_person(graph, person):
    '''
    '''
    assert person
    enabled_units = None
    if person:
        unit = get_unit(person.unit)
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
    nx.set_node_attributes(graph, node_enabled, name="enabled")
    return graph
