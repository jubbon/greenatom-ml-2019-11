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

    data = {
        "Дата начала": f"{project.started_at:%d.%m.%Y}",
        "Дата завершения": f"{project.finished_at:%d.%m.%Y}",
        "Полная длительность": f"{project.duration_full.days} дн.",
        "Текущая длительность": f"{project.duration_now.days} дн.",
        "Осталось": f"{project.duration_full.days - project.duration_now.days} дн.",
        "Прогресс": f"{round(project.progress * 100)}%",
        "Важность": project.priority
    }
    df = pd.DataFrame(data.values(), columns=[""], index=data.keys())
    window.table(df)
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
    data = dict()
    for unit in project.units():
        head = unit.head

        employee_count = 0
        total_involvement = 0
        for employee in get_employees(unit.fullname):
            involvement = employee.projects[project.name]
            if involvement:
                total_involvement += involvement / 100.0
                employee_count += 1

        data[unit.fullname] = {
            "Руководитель": head.fullname if head else "",
            "Сотрудников в проекте": employee_count,
            "Суммарная вовлеченность": round(total_involvement, 1)
        }
    window.subheader(f"Подразделения ({len(data)})")
    if data:
        df = pd.DataFrame(data.values(), index=data.keys())
        window.table(df.sort_values(by=["Сотрудников в проекте"], ascending=[False, ]))


def employees(window, project, locale=None):
    ''' Список участников в проекте
    '''
    assert project
    window.subheader("Участники")
    data = dict()
    for employee, involvement in project.employees():
        data[employee.fullname] = {
            "Должность": employee.job,
            "Вовлеченность, %": involvement
        }
    df = pd.DataFrame(data.values(), index=data.keys())
    window.table(df.sort_values(by=["Вовлеченность, %"], ascending=[False, ]))
