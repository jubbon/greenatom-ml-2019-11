#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import networkx as nx


def load_staff(filename):
    '''
    '''
    sheet_name = 'Персонал'
    print(f"Loading staff from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name,
        dtype={'Табельный номер': str}
    )
    return df


def load_skills(filename):
    '''
    '''
    sheet_name = 'Компетенции'
    print(f"Loading skills from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name,
        dtype={'Табельный номер': str}
    )
    return df


def load_units(filename):
    '''
    '''
    sheet_name = 'Оргструктура'
    print(f"Loading units from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name
    )
    return df


def load_nodes(filename):
    '''
    '''
    nodes = dict()
    df_units = load_units(filename)
    for index, row in df_units.iterrows():
        unit = row.to_dict()
        unit_name = unit["Тип"] + ' ' + unit["Номер"]
        nodes.setdefault(unit_name, dict(type='unit')).update(row.to_dict())

    df_staff = load_staff(filename)
    for index, row in df_staff.iterrows():
        staff_uid = row['Табельный номер']
        nodes.setdefault(staff_uid, dict(type='staff')).update(row.to_dict())

    df_skills = load_skills(filename)
    for index, row in df_skills.iterrows():
        skills = row.to_dict()
        staff_uid = skills.pop('Табельный номер')
        nodes.setdefault(staff_uid, dict(type='staff')).update(skills=skills)

    for skill_name in df_skills.columns.to_list():
        if skill_name == 'Табельный номер':
            continue
        nodes.setdefault(skill_name, dict()).update(type="skill")
    return nodes


def load_graph(filename):
    '''
    '''
    G = nx.Graph()

    nodes = load_nodes(filename)
    # print(nodes, flush=True)
    for node_id, node in nodes.items():
        node_type = node.get("type")
        attrs = dict(type=node_type)
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
    return G
