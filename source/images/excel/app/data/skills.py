#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from collections import OrderedDict


SKILLS = [
    "tech:programming:python",
    "tech:programming:C",
    "tech:programming:JavaScript",
    "finance"
]


def generator(positions: list, locale: str):
    '''
    '''
    for position in positions:
        yield OrderedDict({skill: random.randint(0, 10) for skill in SKILLS})
