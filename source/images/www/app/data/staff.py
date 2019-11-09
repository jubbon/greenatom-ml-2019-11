#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
from dataclasses import dataclass, asdict

import pandas as pd


data = {}


@dataclass
class Person:
    uid: str
    lastname: str
    firstname: str
    patronymic: str
    birthday: date
    unit: str
    job: str

    @property
    def fullname(self) -> str:
        ''' ФИО
        '''
        return " ".join([self.lastname, self.firstname, self.patronymic])

    @property
    def ages(self) -> int:
        ''' Полных лет
        '''
        delta = date.today() - self.birthday
        return delta.days // 365

    @property
    def desc(self) -> str:
        return f"{self.fullname} ({self.ages} лет)"

    def to_dict(self):
        data = asdict(self)
        data.update(
            fullname=self.fullname,
            ages=self.ages
        )
        return data


def load(filename):
    '''
    '''
    global data
    sheet_name = 'Персонал'
    print(f"Loading staff from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name,
        dtype={'Табельный номер': str}
    )
    for index, row in df.iterrows():
        person = row.to_dict()
        uid = person['Табельный номер']
        data[uid] = Person(
            uid=uid,
            lastname=person['Фамилия'],
            firstname=person['Имя'],
            patronymic=person['Отчество'],
            birthday=date.fromisoformat(person['Дата рождения']),
            unit=person['Подразделение'],
            job=person['Должность']
        )


def persons(unit=None):
    '''
    '''
    for person_uid, person in data.items():
        if unit and unit != person.unit:
            continue
        yield person_uid, person
