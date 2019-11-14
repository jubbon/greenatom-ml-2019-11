#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import streamlit as st

from smart_hr.data import load_data

from gui import filter_by_units
from gui import filter_by_persons
from gui import widgets


def main():
    '''
    '''
    locale = os.getenv("LOCALE")
    data_dir = os.getenv("DATA_DIR", ".")
    excel_filename = os.path.join(data_dir, "hr.xls")
    load_data(excel_filename)

    selected_units = filter_by_units()
    active_person = filter_by_persons(selected_units[-1])

    if active_person:
        # Выбран сотрудник
        st.title(active_person.fullname)
        widgets.employee.brief(st.sidebar, active_person)
        widgets.employee.info(st, active_person, locale=locale)
        widgets.employee.family(st, active_person, locale=locale)
        widgets.employee.skill(st, active_person)
        widgets.employee.dismiss(st, active_person)
        widgets.employee.graph(st, active_person)
    elif selected_units:
        # Выбрано подразделение
        st.title("/".join(selected_units))
