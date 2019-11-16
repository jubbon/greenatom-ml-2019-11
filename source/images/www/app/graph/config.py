#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx


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