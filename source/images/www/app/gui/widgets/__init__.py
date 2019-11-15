#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .employee import *  # noqa
from .unit import *  # noqa
from .project import *  # noqa

from smart_hr.data.unit import units as get_units
from smart_hr.data.unit import get_employees
from smart_hr.data.staff import persons
from smart_hr.data.project import projects


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
