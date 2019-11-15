#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import streamlit as st

from smart_hr.data import load_data

from gui import widgets


def main():
    '''
    '''
    locale = os.getenv("LOCALE")
    data_dir = os.getenv("DATA_DIR", ".")
    excel_filename = os.path.join(data_dir, "hr.xls")
    load_data(excel_filename)

    units, project, employee = widgets.filters(st.sidebar)
    if employee:
        # Выбран сотрудник
        st.title("Информация о сотруднике")
        st.header(employee.fullname)
        widgets.employee.brief(st.sidebar, employee)
        widgets.employee.info(st, employee, locale=locale)
        widgets.employee.family(st, employee, locale=locale)
        widgets.employee.skill(st, employee)
        widgets.employee.dismiss(st, employee)
        widgets.employee.graph(st, employee)
    elif units:
        # Выбрано подразделение
        st.title("Информация о подразделении")
        st.header("/".join(units).title())
        widgets.unit.info(st, units, locale=locale)
        widgets.unit.employees(st, units, locale=locale)
