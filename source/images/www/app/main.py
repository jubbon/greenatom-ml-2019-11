#!/usr/bin/env python
# -*- coding: utf-8 -*-


import streamlit as st

from graph import get_graph
from vis.plotly import graph_via_plotly
from vis.bokeh import graph_via_bokeh

from data import load_data
from gui import filter_by_units


def main():
    '''
    '''
    load_data('/data/hr.xls')

    selected_units = filter_by_units()
    st.text("/".join(selected_units))

    title = st.sidebar.text_input('Введите ФИО сотрудника', '')
    if title:
        st.write(f'Информация по сотруднику {title}:')
        st.write(f'Вероятность увольнения: 56%')

    blocks = [
        # graph_via_plotly(get_graph()),
        graph_via_bokeh(get_graph())
    ]
    # map(st.write, blocks)
    for block in blocks:
        st.write(block)
