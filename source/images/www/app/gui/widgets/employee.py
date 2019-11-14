#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from graph import load_graphs
from graph import filter_graph_for_person
from vis import render_graph

from tasks import send_email


def brief(window, person):
    ''' Краткая информация о сотруднике
    '''
    assert person
    window.image(person.image_filename, use_column_width=True)
    window.markdown(
        f'''
        **ФИО:** {person.fullname}

        **Возраст:** {person.ages}

        **Должность:** {person.job}'''
    )


def info(window, person, locale=None):
    ''' Общая информация о сотруднике
    '''
    assert person
    window.subheader("Общая информация")

    data = person.to_dict(locale)
    df = pd.DataFrame(
        data.values(),
        index=data.keys(),
        columns=["", ])
    window.dataframe(df)


def family(window, person, locale=None):
    ''' Семейное положение
    '''
    assert person
    window.subheader("Семейное положение")

    data = person.family.to_dict(locale)
    df = pd.DataFrame(
        data.values(),
        index=data.keys(),
        columns=["", ])
    window.dataframe(df)


def skill(window, person):
    ''' Компетенции сотрудника
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
        to = "kulikov@sarov.info"
        subject = "[SmartHR] Рекомендованные эксперты"
        text = f"Рекомендованные эксперты для сотрудника {person.fullname}"
        res = send_email(to=to, subject=subject, text=text)
        if res:
            window.text(f"Письмо с рекомендованными экспертами было успешно отправлено на адрес '{to}'")
    else:
        print(f"Не выбрали помощь экспертов", flush=True)


def dismiss(window, person):
    ''' Увольнение
    '''
    assert person
    window.subheader("Увольнение")
    if window.button(
        "Рассчитать вероятность увольнения",
        key="predict_dismiss"):
        window.markdown(f"Вероятность увольнения в ближайшие 3 месяца составляет **27%**")


def graph(window, person):
    ''' Графы социального взаимодействия
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
