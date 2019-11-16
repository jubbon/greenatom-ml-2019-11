#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from collections import OrderedDict


ACTIVITIES = [
    # Количество опозданий на работу
    "count_late_for_work",
    # Количество ранних уходов с работы
    "count_early_from_work",
    # Количество отгулов
    "count_day_off",
]


def generator(positions: list, periods: list, locale: str):
    '''
    '''
    for position in positions:
        activities = OrderedDict()
        for activity in ACTIVITIES:
            prev_value = 0
            for period in periods:
                activity_name = f"{activity}_{period}"
                value = random.randint(
                    prev_value,
                    prev_value + random.randint(1, 3) * 10)
                activities[activity_name] = value
                prev_value = value
        yield activities


def names():
    '''
    '''
    return ACTIVITIES
