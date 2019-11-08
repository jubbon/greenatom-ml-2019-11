#!/usr/bin/env python
# -*- coding: utf-8 -*-


import streamlit as st

from graph import load_graph
from vis import render_graph

from data import load_data
from gui import filter_by_units
from gui import filter_by_persons
from gui import person_card


def main():
    '''
    '''
    load_data('/data/hr.xls')

    selected_units = filter_by_units()
    active_person = filter_by_persons(selected_units[-1])
    person_card(active_person)
    graph = load_graph(selected_units[-1], active_person)

    blocks = [
        "/".join(selected_units),
        # render_graph(graph, engine="plotly"),
        render_graph(graph, engine="bokeh")
    ]
    for block in blocks:
        st.write(block)
