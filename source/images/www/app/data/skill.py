#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas as pd


data = {}
names_ = list()

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
        person_uid = skill['Табельный номер']
        data[person_uid] = skill
    for skill_name in df.columns.to_list():
        if skill_name == 'Табельный номер':
            continue
        names_.append(skill_name)


def get_skills(person_uid: str) -> dict:
    ''' Return skills for person
    '''
    return data.get(person_uid, {})


def skills():
    '''
    '''
    for skill_name in names_:
        yield skill_name
