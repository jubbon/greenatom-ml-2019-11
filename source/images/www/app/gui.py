#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import pandas as pd
import streamlit as st

from data.unit import units
from data.staff import persons


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


def person_card(person):
    '''
    '''
    if person:
        st.sidebar.image(person.image_filename, use_column_width=True)
        st.sidebar.markdown(
            f'''
            **ФИО:** {person.fullname}

            **Возраст:** {person.ages}

            **Должность:** {person.job}'''
        )


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
        window.text(f"Письмо с рекомендованными экспертами было отправлено", flush=True)
    else:
        print(f"Не выбрали помощь экспертов", flush=True)
