#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import streamlit as st


from gui import widgets
from data import load_data


def main():
    '''
    '''
    locale = os.getenv("LOCALE")
    engine = os.getenv("VIS_ENGINE", "bokeh")
    data_dir = os.getenv("DATA_DIR", ".")
    load_data(data_dir)

    widgets.intro.banner(st)
    units, project, employee = widgets.filters(st.sidebar)
    graph_names = ["skill-staff-unit", "staff-unit", "staff-skill", "project-staff"]
    if employee:
        # Выбран сотрудник
        st.title("Информация о сотруднике")
        st.header(employee.fullname)
        widgets.employee.brief(st.sidebar, employee)
        widgets.employee.info(st, employee, locale=locale)
        widgets.employee.family_and_living(st, employee, locale=locale)
        widgets.employee.skill(st, employee)
        widgets.employee.dismiss(st, employee)
        widgets.graph(st, graph_names, employee=employee, engine=engine)
    elif project:
        # Выбран проект
        st.title("Информация о проекте")
        st.header(project.name)
        widgets.project.info(st, project, locale=locale)
        widgets.project.skills(st, project, locale=locale)
        widgets.project.units(st, project, locale=locale)
        widgets.project.employees(st, project, locale=locale)
        widgets.graph(st, graph_names, project=project, engine=engine)
    elif units:
        # Выбрано подразделение
        st.title("Информация о подразделении")
        st.header("/".join(units).title())
        widgets.unit.info(st, units, locale=locale)
        widgets.unit.employees(st, units, locale=locale)
        widgets.graph(st, graph_names, unit=unit[-1], engine=engine)
    else:
        # Начальная страница
        widgets.graph(st, graph_names, engine=engine)
        widgets.intro.nlp(st, locale=locale)
