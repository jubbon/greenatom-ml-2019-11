#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import date
from dataclasses import dataclass, asdict
from typing import ClassVar

import pandas as pd

from .skill import get_skills


data = {}


@dataclass
class FamilyRelations:
    _meta: ClassVar = {
        "ru": {
            "status": "Текущий статус",
            "children_count": "Количество детей",
            "local": "Уроженец данной местности",
        }
    }
    # Семейный статус
    status: str
    # Количество несовершеннолетних детей
    children_count: int
    # Уроженец данной местности
    local: bool

    def to_dict(self, locale=None):
        data = asdict(self)
        if locale:
            data = {
                self._meta.get(locale, {}).get(k, k): v
                for k, v
                in data.items()}
        return data


@dataclass
class Person:
    _meta: ClassVar = {
        "ru": {
            "uid": "Табельный номер",
            "lastname": "Фамилия",
            "firstname": "Имя",
            "patronymic": "Отчество",
            "birthday": "Дата рождения",
            "gender": "Пол",
            "unit": "Подразделение",
            "job": "Должность",
            "fullname": "ФИО",
            "ages": "Полных лет"
        }
    }
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

    # Семейное положение
    family: FamilyRelations

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

    def to_dict(self, locale=None):
        data = asdict(self)
        data.pop("family")
        data.update(
            fullname=self.fullname,
            ages=self.ages,
            is_dismissed=self.is_dismissed
        )
        if locale:
            data = {
                self._meta.get(locale, {}).get(k, k): v
                for k, v
                in data.items()}
        return data


def load_family_relations(filename):
    '''
    '''
    data = dict()
    sheet_name = 'Семейное положение'
    print(f"Loading family relations from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name,
        dtype={'Табельный номер': str}
    )

    for index, row in df.iterrows():
        fr = row.to_dict()
        uid = fr['Табельный номер']
        data[uid] = FamilyRelations(
            status=fr["Статус"],
            children_count=fr["Количество детей"],
            local=fr["Местный специалист"]
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

    frs = load_family_relations(filename)

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
            image_number=int(uid) % 22 + 1,
            family=frs[uid]
        )


def persons(unit=None):
    '''
    '''
    for person_uid, person in data.items():
        if unit and unit != person.unit:
            continue
        yield person_uid, person
