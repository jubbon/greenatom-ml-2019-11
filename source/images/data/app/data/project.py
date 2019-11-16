#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import OrderedDict

from mimesis import Science

from .skills import generator as get_skills


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
    project_names = set()
    while len(project_names) < count:
        project_names.add(science.chemical_element())
    assert len(project_names) == count
    for name in project_names:
        for skills in get_skills([1, ], locale=locale):
            yield Project(
                name=name,
                skills=skills
            )
            break
