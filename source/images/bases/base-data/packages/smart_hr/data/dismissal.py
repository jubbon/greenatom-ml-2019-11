#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

import pandas as pd


data = {}


@dataclass
class Dismissal:
    filename: ClassVar = None
    updated_at: ClassVar = None
    person_uid: str
    probability: float


def load(filename=None):
    '''
    '''
    global data
    if filename is None:
        filename = Dismissal.filename
    if not filename:
        return
    print(f"Loading dismissal probability from file '{filename}'", flush=True)
    df = pd.read_csv(
        filename,
        dtype={'Табельный номер': str}
    )
    for index, row in df.iterrows():
        dp = row.to_dict()
        person_uid = dp.pop('Табельный номер')
        dismissal = Dismissal(
            person_uid=person_uid,
            probability=dp['Вероятность увольнения']
        )
        data[person_uid] = dismissal
    Dismissal.filename = filename
    Dismissal.updated_at = datetime.now().timestamp()


def get_dismissal_probability(person_uid: str) -> Dismissal:
    ''' Return dismissal probability for person
    '''
    assert person_uid
    if person_uid not in data:
        # Загрузка данных
        load()
    if Dismissal.updated_at < os.stat(Dismissal.filename).st_mtime:
        # Обновление данных
        load()
    return data[person_uid].probability
