#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import ClassVar

import pandas as pd


data = {}


@dataclass
class FeatureImportance:
    filename: ClassVar = None
    updated_at: ClassVar = None
    feature_name: str
    importance: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Dismissal:
    filename: ClassVar = None
    feature_importance: ClassVar = None
    updated_at: ClassVar = None
    person_uid: str
    probability: float


def load(dismissal_filename=None, feature_importance_filename=None):
    '''
    '''
    load_dismissal(dismissal_filename)
    load_feature_importance(feature_importance_filename)


def load_dismissal(filename=None):
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
    return True


def load_feature_importance(filename=None):
    '''
    '''
    global data
    if filename is None:
        filename = FeatureImportance.filename
    if not filename:
        return

    print(f"Loading feature importance from file '{filename}'", flush=True)
    df = pd.read_csv(filename)

    feature_importance_list = list()
    for index, row in df.iterrows():
        fi = row.to_dict()
        feature_importance_list.append(FeatureImportance(
            feature_name=fi['Наименование колонки'],
            importance=fi['Важность']
        ))
    Dismissal.feature_importance = feature_importance_list
    FeatureImportance.filename = filename
    FeatureImportance.updated_at = datetime.now().timestamp()


def get_dismissal(person_uid: str) -> Dismissal:
    ''' Return dismissal for person
    '''
    assert person_uid
    if person_uid not in data:
        # Загрузка данных
        load()
    if (
        Dismissal.updated_at < os.stat(Dismissal.filename).st_mtime or
        FeatureImportance.updated_at < os.stat(FeatureImportance.filename).st_mtime):
        # Обновление данных
        load()
    return data[person_uid]
