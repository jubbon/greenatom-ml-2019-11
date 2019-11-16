#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import streamlit as st

from smart_hr.data.unit import get_unit, units, parents
from smart_hr.data.staff import persons
from smart_hr.data.skill import skills, get_skills
from smart_hr.data.project import projects


def entities(node_types: list, edge_types: list) -> dict:
    ''' Generate nodes and edges
    '''
    if not node_types or "unit" in node_types:
        for unit_uid, unit in units(level=-1):
            data = dict(type="unit")
            data.update(unit.to_dict(), desc=unit.desc)
            if "projects" in data:
                del data["projects"]
            yield "node", unit_uid, data

            if "unit-unit" in edge_types:
                if unit.parent:
                    data = dict(type="unit-unit")
                    yield "edge", (unit_uid, unit.parent), data

            if "unit-project" in edge_types:
                for project in unit.projects:
                    data = dict(type="unit-project")
                    yield "edge", (unit_uid, project), data

    if not node_types or "staff" in node_types:
        for person_uid, person in persons():
            person_skills = get_skills(person_uid)
            data = dict(type="staff")
            data.update(
                person.to_dict(),
                level=person_skills.mean(),
                desc=person.desc,
                # skills=person_skills.to_dict()
            )
            if 'projects' in data:
                del data['projects']
            yield "node", person_uid, data

            if 'staff-unit' in edge_types:
                data = dict(type="staff-unit")
                yield "edge", (person_uid, person.unit), data

            if 'staff-skill' in edge_types:
                for skill_name, value in person.skills():
                    if value > 0:
                        data = dict(type="staff-skill", value=value)
                        yield "edge", (person_uid, skill_name), data

            if 'staff-project' in edge_types:
                for project_name, involvement in person.projects.items():
                    if involvement > 0:
                        data = dict(type="staff-project")
                        yield "edge", (person_uid, project_name), data

    if not node_types or "skill" in node_types:
        for skill_name, skill_level in skills():
            data = dict(type="skill")
            data.update(
                level=skill_level,
                desc=f"{skill_name} (уровень {skill_level})"
            )
            yield "node", skill_name, data

    if not node_types or "project" in node_types:
        for project in projects():
            data = dict(type="project")
            data.update(
                desc=f"{project.name}"
            )
            yield "node", project.name, data

            if "project-skill" in edge_types:
                for skill_name, value in project.skills.items():
                    if value > 0:
                        data = dict(type="project-skill", value=value)
                        yield "edge", (person_uid, skill_name), data


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
        "edges": [
            "staff-unit",
            "unit-unit"
        ]
    },
    "staff-skill": {
        "title": "Сотрудник-компетенции",
        "init": nx.Graph,
        "nodes": [
            "staff",
            "skill"
        ],
        "edges": [
            "staff-skill"
        ]
    },
    "skill-staff-unit": {
        "title": "Сотрудник-компетенции-подразделение",
        "init": nx.Graph,
        "nodes": [
            "staff",
            "skill",
            "unit"
        ],
        "edges": [
            "staff-unit",
            "unit-unit",
            "staff-skill"
        ]
    },
    "project-staff": {
        "title": "Сотрудник-проект",
        "init": nx.Graph,
        "nodes": [
            "staff",
            "project",
        ],
        "edges": [
            "staff-project"
        ]
    }
}


def load_graph(uid: str, config: dict) -> nx.Graph:
    '''
    '''
    G = config.get('init', nx.Graph)()
    node_types = config.get("nodes")
    assert isinstance(node_types, list)
    edge_types = config.get("edges")
    assert isinstance(node_types, list)
    for entity_type, entity_uid, entity in entities(node_types, edge_types):
        entity.update(enabled=True)
        if entity_type == "node":
            G.add_node(entity_uid, **entity)
        elif entity_type == "edge":
            G.add_edge(*entity_uid, **entity)
        else:
            print("Unknown entity type '{entity_type}'", flush=True)
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
