#!/usr/bin/env python
# -*- coding: utf-8 -*-


import streamlit as st

from graph import load_graph
from vis import render_graph

from data import load_data
from gui import filter_by_units
from gui import filter_by_persons


def main():
    '''
    '''
    load_data('/data/hr.xls')

    selected_units = filter_by_units()
    selected_person = filter_by_persons(selected_units[-1])

    # if title:
    #     st.write(f'Информация по сотруднику {title}:')
    #     st.write(f'Вероятность увольнения: 56%')

    graph = load_graph(selected_units[-1], selected_person)
    blocks = [
        "/".join(selected_units),
        selected_person,
        # render_graph(graph, engine="plotly"),
        render_graph(graph, engine="bokeh")
    ]
    for block in blocks:
        st.write(block)
