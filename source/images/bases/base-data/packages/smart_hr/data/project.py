#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import OrderedDict

import pandas as pd

from .unit import leafs
from .staff import persons


data = {}


@dataclass()
class Project:
    # Наименование проекта
    name: str
    # Необходимые компетенции
    skills: OrderedDict[str, int]

    def __hash__(self):
        return hash(self.name)

    def units(self):
        '''
        '''
        for unit in leafs():
            if unit.projects.get(self.name, 0) == 1:
                yield unit

    def employees(self):
        ''' Сотрудник, участвующие в проекте
        '''
        for _, employee in persons():
            involvement = employee.projects.get(self.name, 0)
            if involvement > 0:
                yield employee, involvement

    def to_dict(self, locale=None) -> dict:
        data = self.skills
        if locale:
            data = {
                self._meta.get(locale, {}).get(k, k): v
                for k, v
                in data.items()}
        return data


def load(filename):
    '''
    '''
    sheet_name = 'Проекты'
    print(f"Loading projects from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name
    )
    for index, row in df.iterrows():
        project = row.to_dict()
        project_name = project.pop("Название")
        project = Project(
            name=project_name,
            skills=OrderedDict({k: int(v) for k, v in project.items()})
        )
        data[project_name] = project


def get_skills(project_name: str):
    ''' Return skills for person
    '''
    return data[project_name]


def projects(unit=None):
    '''
    '''
    for _, project in data.items():
        # if unit and root_uid != unit.parent:
        #     continue
        # yield unit_uid, unit
        yield project
