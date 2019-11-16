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
    for _ in range(count):
        for skills in get_skills([1, ], locale=locale):
            yield Project(
                name=science.chemical_element(),
                skills=skills
            )
            break
