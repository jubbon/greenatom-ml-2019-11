#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from collections import OrderedDict


SKILLS = [
    "tech:programming:python",
    "tech:programming:C",
    "tech:programming:JavaScript",
    "tech:devops",
    "other:presentation",
    "finance"
]

SKILL_VALUES = {
    0: 150,
    1: 9,
    2: 8,
    3: 7,
    4: 6,
    5: 5,
    6: 4,
    7: 3,
    8: 2,
    9: 1
}


def generator(positions: list, locale: str):
    '''
    '''
    skill_values = []
    for skill_level, skill_prob in SKILL_VALUES.items():
        skill_values.extend([skill_level, ] * skill_prob)
    for position in positions:
        while True:
            skills = OrderedDict({skill: random.choice(skill_values) for skill in SKILLS})
            if any(map(lambda skill: skills[skill], skills)):
                yield skills
                break

def names():
    '''
    '''
    return SKILLS
