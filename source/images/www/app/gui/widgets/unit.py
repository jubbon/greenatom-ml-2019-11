#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

from smart_hr.data.unit import get_employees


def info(window, units, locale=None):
    ''' Общая информация о подразделении
    '''
    assert units
    window.subheader("Общая информация")
    employees_ = list(get_employees(unit=units[-1]))
    window.markdown(f"Общее количество сотрудников: **{len(employees_)}**")
    # data = person.to_dict(locale)
    # df = pd.DataFrame(
    #     data.values(),
    #     index=data.keys(),
    #     columns=["", ])
    # window.dataframe(df)


def employees(window, units, locale=None):
    ''' Список сотрудников подразделения
    '''
    assert units
    window.subheader("Сотрудники")
