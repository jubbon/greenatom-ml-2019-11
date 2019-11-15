#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, asdict
from typing import Dict

import pandas as pd


data = {}


@dataclass
class Unit:
    unit_type: str
    name: str
    parent: str
    projects: Dict[str, int]

    @property
    def head(self):
        ''' Руководитель подразделения
        '''
        for employee in get_employees(None):
            if employee.is_head and employee.unit == self.fullname:
                return employee

    @property
    def fullname(self):
        return " ".join([self.unit_type, self.name])

    @property
    def desc(self) -> str:
        return f"{self.fullname}"

    def to_dict(self):
        data = asdict(self)
        data.update(fullname=self.fullname)
        return data



def load(filename):
    '''
    '''
    global data
    sheet_name = 'Оргструктура'
    print(f"Loading units from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name
    )
    for index, row in df.iterrows():
        unit = row.to_dict()
        unit_type = unit.pop("Тип")
        name = unit.pop("Номер")
        parent = unit.pop("Родительская структура").strip()
        projects = {k: int(v) for k, v in unit.items() if not k.startswith("Unnamed")}
        unit = Unit(
            unit_type=unit_type,
            name=name,
            parent=parent,
            projects=projects
        )
        data[unit.fullname] = unit


def get_unit(uid: str) -> Unit:
    '''
    '''
    assert uid
    return data[uid]


def units(root_uid=None, level=0):
    '''
    '''
    for unit_uid, unit in data.items():
        if not root_uid and unit.parent:
            continue
        if root_uid and root_uid != unit.parent:
            continue
        yield unit_uid, unit
        if level:
            yield from units(root_uid=unit_uid, level=level-1)


def leafs(root_uid=None):
    '''
    '''
    all_units = dict()
    for unit_uid, unit in data.items():
        all_units[unit_uid] = unit

    for unit_uid, unit in data.items():
        if not unit.parent:
            del all_units[unit_uid]
        elif unit.parent in all_units:
            del all_units[unit.parent]

    for unit_uid, unit in all_units.items():
        yield unit


def parents(unit):
    ''' Return all parents units
    '''
    if unit.parent:
        parent = get_unit(unit.parent)
        yield parent
        yield from parents(parent)


def get_employees(unit=None):
    '''
    '''
    from .staff import persons
    if unit:
        for _, employee in persons(unit):
            yield employee
    for unit_uid, _ in units(unit):
        yield from get_employees(unit=unit_uid)
