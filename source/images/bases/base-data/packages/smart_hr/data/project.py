#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from dataclasses import dataclass, asdict
from typing import OrderedDict
from math import isnan

import pandas as pd

from .unit import leafs
from .staff import persons


data = {}


@dataclass()
class Project:
    # Наименование проекта
    name: str
    # Дата старта проекта
    started_at: date
    # Дата завершения проекта
    finished_at: date
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
        ''' Сотрудники, участвующие в проекте
        '''
        for _, employee in persons():
            involvement = employee.projects.get(self.name, 0)
            if involvement > 0:
                yield employee, involvement

    def duration(self, dt: date) -> timedelta:
        ''' Длительность проекта до заданной даты
        '''
        assert dt
        assert dt > self.started_at
        return dt - self.started_at

    @property
    def duration_full(self):
        '''
        '''
        return self.duration(self.finished_at)

    @property
    def duration_now(self):
        '''
        '''
        return self.duration(date.today())

    @property
    def progress(self):
        '''
        '''
        return self.duration_now / self.duration_full

    def to_dict(self, locale=None) -> dict:
        data = asdict(self)
        # data.update(self.skills)
        # if locale:
        #     data = {
        #         self._meta.get(locale, {}).get(k, k): v
        #         for k, v
        #         in data.items()}
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
        started_at = project.pop("Дата начала")
        finished_at = project.pop("Дата завершения")
        project = Project(
            name=project_name,
            started_at=date.fromisoformat(started_at),
            finished_at=date.fromisoformat(finished_at),
            skills=OrderedDict({k: int(v) for k, v in project.items() if not isnan(v)})
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
