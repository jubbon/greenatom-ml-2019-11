#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx


GRAPHS = {
    # "test": {
    #     "title": "Демо",
    #     "init": nx.karate_club_graph,
    # },
    "staff-unit": {
        "title": "Оргструктура компании",
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
        "title": "Компетенции сотрудников",
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
        "title": "Компетенции cотрудников и подразделений",
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
        "title": "Участие сотрудников в проектах компании",
        "init": nx.Graph,
        "nodes": [
            "staff",
            "project",
        ],
        "edges": [
            "staff-project"
        ]
    },
    "staff-staff": {
        "title": "Социальные взаимосвязи сотрудников",
        "init": nx.Graph,
        "nodes": [
            "staff",
        ],
        "edges": [
            "staff-staff"
        ]
    }
}
