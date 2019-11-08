#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


data = {}


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
        unit_uid = unit["Тип"] + ' ' + unit["Номер"]
        data[unit_uid] = unit


def units(root_uid=None, level=0):
    '''
    '''
    for unit_uid, unit in data.items():
        parent_unit = unit["Родительская структура"].strip()
        if not root_uid and parent_unit:
            continue
        if root_uid and root_uid != parent_unit:
            continue
        yield unit_uid, unit
        if level:
            yield from units(root_uid=unit_uid, level=level-1)
