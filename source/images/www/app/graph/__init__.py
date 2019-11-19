#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import streamlit as st
import copy

from smart_hr.data.unit import units
from smart_hr.data.staff import persons
from smart_hr.data.skill import skills, get_skills
from smart_hr.data.project import projects

from .config import GRAPHS
from .vis import render_graph # noqa


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
            email = data.get("contacts", {}).get("email", "")
            data.update(contacts=email)
            yield "node", person_uid, data

            if 'staff-unit' in edge_types:
                data = dict(type="staff-unit")
                yield "edge", (person_uid, person.unit), data

            if 'staff-staff' in edge_types:
                data = dict(type="staff-staff")
                director = person.director
                if director:
                    yield "edge", (person_uid, director.uid), data

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


@st.cache
def load_graph(uid: str, config: dict) -> nx.Graph:
    '''
    '''
    print(f"Generating graph '{uid}'", flush=True)
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
        graph = load_graph(uid, config)
        yield uid, config.get("title", uid), copy.deepcopy(graph)


def available_graphs():
    '''
    '''
    return [(name, params.get("title", name)) for name, params in GRAPHS.items()]
