#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import streamlit as st

from graph import load_graph
from graph import filter_graph_for_person
from vis import render_graph

from data import load_data
from gui import filter_by_units
from gui import filter_by_persons
from gui import person_card


def main():
    '''
    '''
    data_dir = os.getenv("DATA_DIR", ".")
    excel_filename = os.path.join(data_dir, "hr.xls")
    load_data(excel_filename)

    selected_units = filter_by_units()
    active_person = filter_by_persons(selected_units[-1])
    person_card(active_person)
    graph = load_graph()
    print(f"Loaded graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges", flush=True)
    if active_person:
        graph = filter_graph_for_person(graph, active_person)
    blocks = [
        "/".join(selected_units),
        # render_graph(graph, engine="plotly"),
        render_graph(graph, engine="bokeh"),
    ]
    for block in blocks:
        st.write(block)
