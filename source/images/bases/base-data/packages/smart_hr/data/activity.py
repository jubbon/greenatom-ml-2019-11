#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict

import pandas as pd


data = {}
names_ = list()


@dataclass
class PersonActivities:
    person_uid: str
    activities: Dict[str, int]

    def to_dict(self, locale=None) -> dict:
        data = self.activities
        if locale:
            data = {
                self._meta.get(locale, {}).get(k, k): v
                for k, v
                in data.items()}
        return data


def load(filename):
    '''
    '''
    print(f"Loading activities from file '{filename}'", flush=True)
    df = pd.read_csv(
        filename,
        dtype={'uid': str}
    )
    for index, row in df.iterrows():
        activity = row.to_dict()
        person_uid = activity.pop('uid')
        activities = PersonActivities(
            person_uid=person_uid,
            activities={k: int(v) for k, v in activity.items()}
        )
        data[person_uid] = activities


def get_activities(person_uid: str) -> PersonActivities:
    ''' Return activities for person
    '''
    return data.get(person_uid)
