#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

from smart_hr.data.unit import units as get_units
from smart_hr.data.unit import get_unit
from smart_hr.data.unit import get_employees


def info(window, units, locale=None):
    ''' Общая информация о подразделении
    '''
    assert units
    window.subheader("Общая информация")
    unit = get_unit(units[-1])
    employees_ = list(get_employees(unit=units[-1]))
    window.markdown(f"Общее количество сотрудников: **{len(employees_)}**")
    window.markdown(f"Руководитель: **{unit.head.fullname}**")

    # data = person.to_dict(locale)
    # df = pd.DataFrame(
    #     data.values(),
    #     index=data.keys(),
    #     columns=["", ])
    # window.dataframe(df)


def units(window, units, locale=None):
    ''' Список подразделениий
    '''
    assert units

    unit_uid = units[-1]
    if not unit_uid:
        return

    data = dict()
    for unit_uid, unit in get_units(unit_uid, level=0):
        head = unit.head
        employees_count = len(list(get_employees(unit_uid)))
        data[unit_uid] = {
            "Руководитель": head.fullname if head else "",
            "Сотрудников": employees_count,
        }
    if data:
        window.subheader(f"Подразделения ({len(data)})")
        df = pd.DataFrame(data.values(), index=data.keys())
        window.table(df)


def employees(window, units, locale=None):
    ''' Список сотрудников подразделения
    '''
    assert units
    window.subheader("Сотрудники")
