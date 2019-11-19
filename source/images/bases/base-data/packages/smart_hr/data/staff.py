#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import date
from dataclasses import dataclass, asdict
from typing import ClassVar
from typing import Dict

import pandas as pd

from .activity import get_activities
from .skill import get_skills
from .dismissal import get_dismissal
from .unit import get_unit

data = {}


@dataclass
class Contacts:
    # Адрес электронной почты
    email: str


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
    promotion_workingday: date
    image_number: int

    # Вовлеченность в проекты
    projects: Dict[str, int]

    # Контактная информация
    contacts: Contacts

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

    @property
    def director(self):
        '''
        '''
        unit = get_unit(self.unit)
        return unit.head

    def feature_value(self, feature_name):
        '''
        '''
        skills = get_skills(self.uid).to_dict()
        activities = get_activities(self.uid)
        activities = activities.to_dict() if activities else {}

        if feature_name == "Ипотека":
            return "Наличие ипотеки", self.living.mortgage
        elif feature_name == "Дата последнего повышения":
            return "Дата последнего повышения", f"{self.promotion_workingday:%d.%m.%Y}"
        elif feature_name == "Должность":
            return "Должность", self.job
        elif feature_name == "count_early_from_work_1m":
            return "Ранний уход с работы за последний месяц", activities.get(feature_name, "")
        elif feature_name == "count_late_for_work_1m":
            return "Опоздание на работу за последний месяц", activities.get(feature_name, "")
        elif feature_name == "tech:programming:JavaScript":
            return "Уровень знаний JavaScript", skills.get("tech:programming:JavaScript", "")
        elif feature_name == "tech:programming:python":
            return "Уровень знаний Python", skills.get("tech:programming:python", "")
        elif feature_name == "count_day_off_3m":
            return "Отгулы за последние 3 месяца", activities.get(feature_name, "")
        elif feature_name == "Тип жилья":
            return "Тип жилья", self.living.dwelling_type
        elif feature_name == "other:presentation":
            return "Уровень владения презентационными навыками", skills.get(feature_name, "")
        elif feature_name == "finance":
            return "Уровень навыков финансовой деятельности", skills.get("finance", "")
        elif feature_name == "Руководитель":
            return "Руководитель", "Да" if self.is_head else "Нет"
        elif feature_name == "count_day_off_1m":
            return "Отгулы за последний месяц", activities.get(feature_name, "")
        elif feature_name == "count_workdays_weekend_1m":
            return "Работа в выходные дни за последний месяц", activities.get(feature_name, "")
        else:
            return ""

    def dismissal(self, feature_importance_count) -> float:
        dismissal = get_dismissal(self.uid)
        if dismissal is None:
            return None
        feature_importance_list = list()
        for fi in dismissal.feature_importance[:feature_importance_count]:
            feature_importance = fi.to_dict()
            feature_name = feature_importance['feature_name']
            desc, value = self.feature_value(feature_name)
            feature_importance.update(feature_name=desc, value=value)
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


def load_contacts(filename):
    '''
    '''
    data = dict()
    sheet_name = 'Контакты'
    print(f"Loading contacts from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name,
        dtype={'Табельный номер': str}
    )

    for index, row in df.iterrows():
        cnt = row.to_dict()
        uid = cnt['Табельный номер']
        data[uid] = Contacts(
            email=cnt["Адрес электронной почты"]
        )
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
    cs = load_contacts(filename)

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
            promotion_workingday=date.fromisoformat(person['Дата последнего повышения']),
            gender=person['Пол'],
            unit=person['Подразделение'],
            job=person['Должность'],
            is_head=person['Руководитель'] == 'Да',
            status=person['Статус'],
            image_number=int(uid) % 85 + 1,
            projects=projects[uid],
            contacts=cs[uid],
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


def experts(skill_name: str, expected_skill_value: int, unit=None):
    ''' Генерирует список экспертов - сотрудников с компетенциями, не ниже заданных
    '''
    for person_uid, person in persons(unit):
        for person_skill_name, person_skill_value in person.skills():
            if person_skill_name == skill_name:
                if person_skill_value >= expected_skill_value:
                    yield person, person_skill_value
                break
