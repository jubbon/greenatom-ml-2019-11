#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from dataclasses import dataclass, asdict
from typing import Dict
from typing import ClassVar

import numpy as np
import pandas as pd


data = {}
names_ = list()
counter_ = Counter()


@dataclass
class PersonSkills:
    _meta: ClassVar = {
        "ru": {
            "finance": "Финансы",
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
    person_uid: str
    skills: Dict[str, int]

    def mean(self) -> float:
        '''
        '''
        return round(np.mean(list(self.skills.values())), 1)

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
    sheet_name = 'Компетенции'
    print(f"Loading skills from sheet '{sheet_name}'", flush=True)
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name,
        dtype={'Табельный номер': str}
    )
    for index, row in df.iterrows():
        skill = row.to_dict()
        person_uid = skill.pop('Табельный номер')
        skills = PersonSkills(
            person_uid=person_uid,
            skills={k: int(v) for k, v in skill.items()}
        )
        counter_.update(skill)
        data[person_uid] = skills

    for skill_name in df.columns.to_list():
        if skill_name == 'Табельный номер':
            continue
        names_.append(skill_name)


def get_skills(person_uid: str) -> PersonSkills:
    ''' Return skills for person
    '''
    return data[person_uid]


def skills():
    '''
    '''
    for skill_name in names_:
        skill_level = round(counter_[skill_name] / len(data), 1)
        yield skill_name, skill_level
