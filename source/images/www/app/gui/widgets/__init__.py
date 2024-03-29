#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .employee import *  # noqa
from .unit import *  # noqa
from .project import *  # noqa
from .intro import *  # noqa

from smart_hr.data.unit import units as get_units
from smart_hr.data.unit import get_employees
from smart_hr.data.staff import persons
from smart_hr.data.project import projects

from graph import load_graphs
from graph import render_graph
from graph.filters.unit import filter_graph as filter_graph_for_unit
from graph.filters.project import filter_graph as filter_graph_for_project
from graph.filters.employee import filter_graph as filter_graph_for_employee


def graph(window, available_graphs: list, unit=None, project=None, employee=None, engine="bokeh"):
    ''' Графы социального взаимодействия
    '''
    window.subheader("Графы взаимодействия")

    graph_titles = window.multiselect(
        label="",
        options=list(title for _, title in available_graphs),
        default=None)

    graph_names = list(
        name
        for name, title
        in available_graphs
        if title in graph_titles)

    for graph_uid, graph_title, graph in load_graphs(graph_names):
        print(f"Loaded graph '{graph_uid}' with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges", flush=True)
        if employee:
            print(f"Filtering graph for {employee}", flush=True)
            graph = filter_graph_for_employee(graph, employee)
        elif project:
            print(f"Filtering graph for project '{project}'", flush=True)
            graph = filter_graph_for_project(graph, project)
        elif unit:
            print(f"Filtering graph for unit '{unit}'", flush=True)
            graph = filter_graph_for_unit(graph, unit)

        # k = window.slider('k:', 0.001, 1.0, step=0.001, key=f"{graph_uid}_k")
        layout_attr = dict(
            k=None,
            scale=100,
            center=(0, 0))
        window.write(
            render_graph(
                graph,
                title=graph_title,
                engine=engine,
                layout_attr=layout_attr))


def filters(window):
    '''
    '''
    def filter_by_units(window, root_unit=""):
        '''
        '''
        unit_uids = list()
        for unit_uid, _ in get_units(root_unit):
            unit_uids.append(unit_uid)
        if not unit_uids:
            return list()
        selected_unit = window.selectbox(
            "" if root_unit else "Подразделение:",
            ["", ] + unit_uids)
        selected_units = []
        if selected_unit:
            selected_units = [selected_unit, ] + filter_by_units(window, selected_unit)
        return selected_units

    def fullname(employee):
        '''
        '''
        return employee.fullname if employee else " "

    def filter_by_employees(window, unit=None):
        '''
        '''
        employee_names = list(get_employees(unit))
        return window.selectbox(
            "Сотрудник:",
            options=["", ] + sorted(employee_names, key=lambda p: p.fullname),
            format_func=fullname)

    def projectname(project):
        '''
        '''
        return project.name if project else " "

    def filter_by_projects(window, unit=None):
        '''
        '''
        filtered_projects = list(projects(unit))
        return window.selectbox(
            "Проект:",
            options=["", ] + sorted(filtered_projects, key=lambda p: p.name),
            format_func=projectname)

    units = filter_by_units(window)
    unit = units[-1] if units else None
    project = filter_by_projects(window, unit)
    employee = filter_by_employees(window, unit)
    return units, project, employee
