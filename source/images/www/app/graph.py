#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import streamlit as st

from smart_hr.data.unit import get_unit, units, parents
from smart_hr.data.staff import persons
from smart_hr.data.skill import skills, get_skills


def nodes(node_type=None) -> dict:
    ''' Generate nodes
    '''
    if not node_type or node_type == "unit":
        for unit_uid, unit in units(level=-1):
            data = dict(type="unit")
            data.update(unit.to_dict(), desc=unit.desc)
            yield unit_uid, data

    if not node_type or node_type == "staff":
        for person_uid, person in persons():
            person_skills = get_skills(person_uid)
            data = dict(type="staff")
            data.update(
                person.to_dict(),
                level=person_skills.mean(),
                desc=person.desc,
                skills=person_skills.to_dict()
            )
            yield person_uid, data

    if not node_type or node_type == "skill":
        for skill_name, skill_level in skills():
            data = dict(type="skill")
            data.update(
                level=skill_level,
                desc=f"{skill_name} (уровень {skill_level})"
            )
            yield skill_name, data


@st.cache
def load_graphs():
    '''
    '''
    graphs = {
        "staff-unit": nx.Graph(),
        "staff-skill": nx.Graph(),
        "skill-staff-unit": nx.Graph()
    }

    for node_uid, node in nodes():
        # # Признак доступности узла при фильтрации
        # node_enabled = True
        # if node_type == "staff":
        #     if person and person["Табельный номер"] != node.get("Табельный номер"):
        #         node_enabled = False
        node_type = node["type"]
        node.update(enabled=True)
        for graph_name, graph in graphs.items():
            node_types = graph_name.split("-")
            if node_type in node_types:
                graph.add_node(node_uid, **node)

        if node_type == "staff":
            # Подразделение
            unit = node["unit"]
            if unit:
                for graph_name in ("staff-unit", "skill-staff-unit"):
                    graphs[graph_name].add_edge(node_uid, unit, type='unit')
            # Компетенции
            for skill_name, skill_value in node.get("skills", dict()).items():
                assert skill_value in range(0, 10)
                if skill_value:
                    for graph_name in ("staff-skill", "skill-staff-unit"):
                        graphs[graph_name].add_edge(node_uid, skill_name, type='skill', value=skill_value)
        elif node_type == "unit":
            unit = node.get("fullname")
            parent = node.get("parent")
            if unit and parent:
                for graph_name in ("staff-unit", "skill-staff-unit"):
                    graphs[graph_name].add_edge(unit, parent, type='unit')
    return graphs


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
