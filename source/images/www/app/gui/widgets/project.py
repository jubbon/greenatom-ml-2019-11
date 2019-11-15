#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

from .stylers import *

# from smart_hr.data.unit import get_employees


def info(window, project, locale=None):
    ''' Общая информация о проекте
    '''
    assert project
    window.subheader("Общая информация")
    # employees_ = list(get_employees(unit=units[-1]))
    # window.markdown(f"Общее количество сотрудников: **{len(employees_)}**")
    # data = person.to_dict(locale)
    # df = pd.DataFrame(
    #     data.values(),
    #     index=data.keys(),
    #     columns=["", ])
    # window.dataframe(df)


def skills(window, project, locale=None):
    ''' Список компетенций для проекта
    '''
    assert project
    window.subheader("Компетенции")
    data = dict()
    for skill_name, skill_needs in project.skills.items():
        if skill_needs == 0:
            continue
        import random
        skill_now = random.randint(1, 10)
        data.setdefault(skill_name, dict()).update({
            "Запланировано": skill_needs,
            "Участвует в настоящее время": skill_now,
            "Потребность": max(0, skill_needs - skill_now)
        })

    df = pd.DataFrame(data.values(), index=data.keys())
    window.table(df.style.applymap(highlight_more, subset=["Потребность", ]))

    if window.button("Подобрать сотрудников", key="find_employees"):
        window.markdown(f"Рекомендуемые для проекта сотрудники: Куликов, Иванов, Петров")


def units(window, project, locale=None):
    ''' Список подразделений в проекте
    '''
    assert project
    window.subheader("Подразделения")


def employees(window, project, locale=None):
    ''' Список участников в проекте
    '''
    assert project
    window.subheader("Участники")