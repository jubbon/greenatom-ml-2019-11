#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import date
from dataclasses import dataclass, asdict
import random

import pandas as pd

from .skill import get_skills


data = {}


@dataclass
class Person:
    uid: str
    lastname: str
    firstname: str
    patronymic: str
    birthday: date
    gender: str
    unit: str
    job: str
    status: int
    image_number: int

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

    @property
    def is_dismissed(self) -> bool:
        return self.status == 1

    @property
    def image_filename(self) -> str:
        filename = os.path.join(
            os.getenv("IMAGE_DIR", "."),
            "male" if self.gender == "муж" else "female",
            "{:03}.jpeg".format(self.image_number))
        return filename

    def skills(self):
        '''
        '''
        person_skills = get_skills(self.uid).to_dict()
        for skill_name, skill_value in person_skills.items():
            yield skill_name, skill_value

    def to_dict(self):
        data = asdict(self)
        data.update(
            fullname=self.fullname,
            ages=self.ages,
            is_dismissed=self.is_dismissed
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
            gender=person['Пол'],
            unit=person['Подразделение'],
            job=person['Должность'],
            status=person['Статус'],
            image_number=random.randint(1, 22)
        )


def persons(unit=None):
    '''
    '''
    for person_uid, person in data.items():
        if unit and unit != person.unit:
            continue
        yield person_uid, person
