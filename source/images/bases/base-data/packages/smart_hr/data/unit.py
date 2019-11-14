#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, asdict

import pandas as pd


data = {}


@dataclass
class Unit:
    unit_type: str
    name: str
    parent: str

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
        unit = Unit(
            unit_type=unit["Тип"],
            name=unit["Номер"],
            parent=unit["Родительская структура"].strip()
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


def parents(unit):
    ''' Return all parents units
    '''
    if unit.parent:
        parent = get_unit(unit.parent)
        yield parent
        yield from parents(parent)
