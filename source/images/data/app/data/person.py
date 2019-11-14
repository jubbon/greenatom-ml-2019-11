#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from dataclasses import dataclass
from functools import partial
import random

from mimesis import Generic
from mimesis import Datetime
from mimesis import Person
from mimesis.random import Random
from mimesis.enums import Gender
from mimesis.builtins import RussiaSpecProvider


@dataclass
class FamilyRelations:
    # Семейный статус
    status: str
    # Количество несовершеннолетних детей
    children_count: int
    # Родился в данной местности
    local: bool


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
    status: int
    # Первый день на работе
    first_workingday: date
    # Дата последнего повышения
    promotion_workingday: date
    # Дата увольнения
    last_workingday: date
    # Количество командировок за последний год
    business_trip_count: int
    # Суммарное количество дней в командировках за последний год
    business_trip_days: int

    # Семейные отношения
    family: FamilyRelations


def random_date(start: date, end: date, locale: str) -> date:
    ''' Generate random date between start date and end date
    '''
    if end <= start:
        raise RuntimeError("Bad date range")
    datetime = Datetime(locale)
    while True:
        date = datetime.date(start=start.year, end=end.year)
        if date < start or date >= end:
            continue
        return date


def filter_by_last_name(persons):
    ''' Выполняет фильтрацию по фамилии
    '''
    for person in persons:
        if person.last_name.startswith("Ё"):
            continue
        yield person


def generator(positions: list, locale: str):
    '''
    '''
    # generic = Generic(locale)
    datetime = Datetime(locale)
    person = Person(locale)
    ru = RussiaSpecProvider()
    today = date.today()
    get_random_date = partial(random_date, locale=locale)
    while positions:
        gender = random.choice([
            Gender.MALE,
            Gender.FEMALE])
        position = positions.pop(random.randint(0, len(positions)-1))
        status = 1 if random.random() < 0.1 else 0
        birthday = datetime.date(start=1950, end=1998)

        first_workingday = get_random_date(
            start=birthday + timedelta(days=18*365),
            end=today - timedelta(days=2*365))
        promotion_workingday = get_random_date(
            start=first_workingday + timedelta(days=6*30),
            end=today - timedelta(days=6*30))
        last_workingday = get_random_date(
            start=promotion_workingday + timedelta(days=2*30),
            end=today - timedelta(days=2*30))
        assert first_workingday < promotion_workingday, f"{first_workingday} < {promotion_workingday}"
        assert last_workingday is None or promotion_workingday < last_workingday, f"{promotion_workingday} < {last_workingday}"

        business_trip_count = random.choice([0]*30+[1]*20+[2]*16+[3]*13+[4]*8+[5]*5+[6]*4+[7]*3+[8]*2+[9]*1+[10])
        business_trip_days = random.randint(business_trip_count, 7 * business_trip_count)

        family = FamilyRelations(
            status=random.choice([0]*30+[1]*10+[2]*1),
            children_count=random.choice([0]*2+[1]*10+[2]*7+[3]*2),
            local=random.choice([0]*1+[1]*2)
        )
        yield Human(
            uid=person.identifier(mask='#####'),
            last_name=person.last_name(gender=gender),
            first_name=person.name(gender=gender),
            patronymic=ru.patronymic(gender=gender),
            gender='муж' if gender == Gender.MALE else 'жен',
            birthday=birthday,
            department=position[0] + ' ' + position[1],
            position=position[2],
            status=status,
            first_workingday=first_workingday,
            promotion_workingday=promotion_workingday,
            last_workingday=last_workingday if status == 1 else None,
            business_trip_count=business_trip_count,
            business_trip_days=business_trip_days,
            family=family
        )
