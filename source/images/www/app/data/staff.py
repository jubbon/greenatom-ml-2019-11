#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas as pd


data = {}


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
        person_uid = person['Табельный номер']
        data[person_uid] = person


def persons(unit=None):
    '''
    '''
    for person_uid, person in data.items():
        person_unit = person['Подразделение']
        if unit and unit != person_unit:
            continue
        yield person_uid, person
