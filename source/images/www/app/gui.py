#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import pandas as pd
import streamlit as st

from data.unit import units
from data.staff import persons

from graph import load_graphs
from graph import filter_graph_for_person
from vis import render_graph


def filter_by_units(root_unit=""):
    '''
    '''
    unit_uids = list()
    for unit_uid, _ in units(root_unit):
        unit_uids.append(unit_uid)
    if not unit_uids:
        return list()
    selected_unit = st.sidebar.selectbox(
        "" if root_unit else "Выберите подразделение",
        ["", ] + unit_uids)
    selected_units = [selected_unit, ]
    if selected_unit:
        selected_units += filter_by_units(selected_unit)
    return selected_units


def fullname(person):
    '''
    '''
    return person.fullname if person else " "


def filter_by_persons(unit=None):
    '''
    '''
    person_names = list()
    for _, person in persons(unit):
        person_names.append(person)
    if not person_names:
        return {}
    return st.sidebar.selectbox(
        "Сотрудник",
        options=["", ] + sorted(person_names, key=lambda p: p.fullname),
        format_func=fullname)


def brief_card(window, person):
    '''
    '''
    assert person
    window.image(person.image_filename, use_column_width=True)
    window.markdown(
        f'''
        **ФИО:** {person.fullname}

        **Возраст:** {person.ages}

        **Должность:** {person.job}'''
    )


def info_card(window, person):
    '''
    '''
    assert person
    window.subheader("Общая информация")

    data = person.to_dict()
    df = pd.DataFrame(
        data.values(),
        index=data.keys(),
        columns=["", ])
    window.dataframe(df)


def skill_card(window, person):
    '''
    '''
    assert person
    window.subheader("Компетенции сотрудника")

    person_skills = {k: v for k, v in person.skills() if v}
    df_skills = pd.DataFrame(
        person_skills.values(),
        index=person_skills.keys(),
        columns=["Уровень", ])
    window.dataframe(df_skills)

    if window.button("Подобрать экспертов", key="find_experts"):
        window.text(f"Письмо с рекомендованными экспертами было успешно отправлено")
    else:
        print(f"Не выбрали помощь экспертов", flush=True)


def dismiss_card(window, person):
    '''
    '''
    assert person
    window.subheader("Увольнение")
    if window.button(
        "Рассчитать вероятность увольнения",
        key="predict_dismiss"):
        window.markdown(f"Вероятность увольнения в ближайшие 3 месяца составляет **27%**")


def graph_card(window, person):
    '''
    '''
    assert person
    window.subheader("Графы взаимодействия")

    graphs = load_graphs()
    filtered_graphs = dict()
    for graph_name, graph in graphs.items():
        print(f"Loaded graph '{graph_name}' with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges", flush=True)
        if person:
            graph = filter_graph_for_person(graph, person)
        filtered_graphs[graph_name] = graph

    for graph_name in ("skill-staff-unit", "staff-unit", "staff-skill"):
        window.write(render_graph(filtered_graphs[graph_name], engine="bokeh"))
