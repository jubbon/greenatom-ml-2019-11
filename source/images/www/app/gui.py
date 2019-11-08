#!/usr/bin/env python
# -*- coding: utf-8 -*-


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


def filter_by_persons(unit=None):
    '''
    '''
    person_names = list()
    for unit_uid, person in persons(unit):
        person_names.append(person["fullname"])
    if not person_names:
        return ""
    return st.sidebar.selectbox("Сотрудник", ["", ] + sorted(person_names))
