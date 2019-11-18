#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import date
from dataclasses import dataclass, asdict
from typing import ClassVar
from typing import Dict

import pandas as pd

from .skill import get_skills
from .dismissal import get_dismissal


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
class LivingConditions:
    _meta: ClassVar = {
        "ru": {
            "dwelling_type": "Тип жилья",
            "distance": "Удаленность от места работы",
            "mortgage": "Ипотека",
            "country_house": "Наличие дачи"
        }
    }
    # Тип жилья (общежитие, комната, квартира, дом)
    dwelling_type: str
    # Удаленность от места работы
    distance: int
    # Ипотека
    mortgage: str
    # Наличие дачи
    country_house: str

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
    is_head: bool
    status: int
    image_number: int

    # Вовлеченность в проекты
    projects: Dict[str, int]

    # Семейное положение
    family: FamilyRelations

    # Бытовые условия
    living: LivingConditions

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

    def feature_value(self, feature_name):
        '''
        '''
        # TODO
        return ""

    def dismissal(self, feature_importance_count) -> float:
        dismissal = get_dismissal(self.uid)
        feature_importance_list = list()
        for fi in dismissal.feature_importance[:feature_importance_count]:
            feature_importance = fi.to_dict()
            feature_name = feature_importance['feature_name']
            feature_importance.update(value=self.feature_value(feature_name))
            feature_importance_list.append(feature_importance)
        return dismissal.probability, feature_importance_list

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
        data.pop("living")
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
            children_count=int(fr["Количество детей"]),
            local=fr["Местный специалист"]
        )
    return data


def load_living_conditions(filename: str) -> dict:
    '''
    '''
    data = dict()
    sheet_name = 'Бытовые условия'
    print(f"Loading living conditions from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name,
        dtype={'Табельный номер': str}
    )

    for index, row in df.iterrows():
        lc = row.to_dict()
        uid = lc['Табельный номер']
        data[uid] = LivingConditions(
            dwelling_type=lc["Тип жилья"],
            distance=int(lc["Удаленность от места работы"]),
            mortgage=lc["Ипотека"],
            country_house=lc["Наличие дачи"]
        )
    return data


def load_projects(filename):
    '''
    '''
    data = dict()
    sheet_name = 'Вовлеченность'
    print(f"Loading involvement from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name,
        dtype={'Табельный номер': str}
    )

    for index, row in df.iterrows():
        involvement = row.to_dict()
        uid = involvement.pop('Табельный номер')
        projects = {k: int(v) for k, v in involvement.items() if not k.startswith("Unnamed")}
        data[uid] = projects
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
    lcs = load_living_conditions(filename)
    projects = load_projects(filename)

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
            is_head=person['Руководитель'] == 'Да',
            status=person['Статус'],
            image_number=int(uid) % 22 + 1,
            projects=projects[uid],
            family=frs[uid],
            living=lcs[uid]
        )


def persons(unit=None):
    '''
    '''
    for person_uid, person in data.items():
        if unit and unit != person.unit:
            continue
        yield person_uid, person
