#!/usr/bin/env python
# -*- coding: utf-8 -*-


import streamlit as st

from data.unit import units


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
