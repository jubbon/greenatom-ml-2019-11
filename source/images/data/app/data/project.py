#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from dataclasses import dataclass
from functools import partial
from typing import OrderedDict
import random

from mimesis import Science

from app.utils import random_date

from .skills import generator as get_skills


@dataclass()
class Project:
    # Наименование проекта
    name: str
    # Старт проекта
    started_at: date
    # Завершение проекта
    finished_at: date
    # Важность проекта
    # 0 - обычный
    # 1 - высокий приоритет
    # 2 - крайне важный
    priority: int
    # Необходимые компетенции
    skills: OrderedDict[str, int]

    def priority_str(self, locale: str) -> str:
        '''
        '''
        if self.priority == 0:
            return "обычный"
        elif self.priority == 1:
            return "высокий приоритет"
        elif self.priority == 2:
            return "крайне важный"

    def __hash__(self):
        return hash(self.name)


def projects(count: int, locale: str):
    '''
    '''
    science = Science(locale)
    project_names = set()
    while len(project_names) < count:
        project_names.add(science.chemical_element())
    assert len(project_names) == count

    today = date.today()
    get_random_date = partial(random_date, locale=locale)
    for name in project_names:
        started_at = get_random_date(
            start=today - timedelta(days=10*365),
            end=today).replace(day=1)
        finished_at = get_random_date(
            start=today,
            end=today + timedelta(days=3*365)).replace(day=1) - timedelta(days=1)
        priority = random.choice([0]*20+[1]*5+[2]*1)
        for skills in get_skills([1, ], locale=locale):
            yield Project(
                name=name,
                started_at=started_at,
                finished_at=finished_at,
                priority=priority,
                skills=skills,
            )
            break
