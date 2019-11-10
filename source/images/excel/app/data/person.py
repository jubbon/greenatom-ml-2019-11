#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
import random
from dataclasses import dataclass

from mimesis import Generic
from mimesis import Datetime
from mimesis import Person
from mimesis.random import Random
from mimesis.enums import Gender
from mimesis.builtins import RussiaSpecProvider


@dataclass
class Human:
    uid: str
    last_name: str
    first_name: str
    patronymic: str
    gender: str
    birthday: date
    department: str
    position: str
    # Текущий статус (0-работает, 1-уволен)
    status: int = 0


def generator(positions: list, locale: str):
    '''
    '''
    # generic = Generic(locale)
    datetime = Datetime(locale)
    person = Person(locale)
    ru = RussiaSpecProvider()
    while positions:
        gender = random.choice([
            Gender.MALE,
            Gender.FEMALE])
        position = positions.pop(random.randint(0, len(positions)-1))
        status = 1 if random.random() < 0.1 else 0
        yield Human(
            uid=person.identifier(mask='#####'),
            last_name=person.last_name(gender=gender),
            first_name=person.name(gender=gender),
            patronymic=ru.patronymic(gender=gender),
            gender='муж' if gender == Gender.MALE else 'жен',
            birthday=datetime.date(start=1950, end=2000),
            department=position[0] + ' ' + position[1],
            position=position[2],
            status=status
        )
