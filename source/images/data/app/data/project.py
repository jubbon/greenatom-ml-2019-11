#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import OrderedDict

from mimesis import Science

from .skills import generator as get_skills


PROJECTS = [
    {
        "name": "Омега",
        "skills": {
            "tech:programming:python": 5,
            "tech:programming:C": 2,
            "tech:devops": 1
        }
    },
    {
        "name": "Дзета",
        "skills": {
            "tech:programming:JavaScript": 8,
            "tech:programming:python": 1,
            "tech:devops": 3
        }
    },
    {
        "name": "Гамма",
        "skills": {
            "tech:programming:С": 10,
            "tech:programming:python": 1,
            "tech:devops": 3
        }
    },
    {
        "name": "Логос",
        "skills": {
            "other:presentation": 3,
            "finance": 5
        }
    }
]


@dataclass()
class Project:
    # Наименование проекта
    name: str
    # Необходимые компетенции
    skills: OrderedDict[str, int]

    def __hash__(self):
        return hash(self.name)


def projects(count: int, locale: str):
    '''
    '''
    science = Science(locale)
    for _ in range(count):
        for skills in get_skills([1, ], locale=locale):
            yield Project(
                name=science.chemical_element(),
                skills=skills
            )
            break
