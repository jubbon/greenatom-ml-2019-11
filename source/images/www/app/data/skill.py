#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, asdict
from typing import Dict

import numpy as np
import pandas as pd


data = {}
names_ = list()


@dataclass
class PersonSkills:
    person_uid: str
    skills: Dict[str, int]

    def mean(self) -> float:
        '''
        '''
        return round(np.mean(list(self.skills.values())), 1)

    def to_dict(self) -> dict:
        return self.skills


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
            skills=skill
        )
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
        yield skill_name
