#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import streamlit as st

from graph import load_graphs
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
    graphs = load_graphs()
    filtered_graphs = dict()
    for graph_name, graph in graphs.items():
        print(f"Loaded graph '{graph_name}' with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges", flush=True)
        if active_person:
            graph = filter_graph_for_person(graph, active_person)
        filtered_graphs[graph_name] = graph

    blocks = [
        "/".join(selected_units),
        render_graph(filtered_graphs["skill-staff-unit"], engine="bokeh"),
        render_graph(filtered_graphs["staff-unit"], engine="bokeh"),
        render_graph(filtered_graphs["staff-skill"], engine="bokeh"),
    ]
    for block in blocks:
        st.write(block)
