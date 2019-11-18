#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, timedelta


def get_dismissal_probability(employee, skill, activity) -> float:
    '''
    '''
    # Базовая вероятность
    probability = 0.1

    # Эксперт в языках программирования
    if skill.get("tech:programming:JavaScript", 0) > 7:
        probability *= 1.6
    if skill.get("tech:programming:python", 0) > 8:
        probability *= 1.4

    # Опоздания на работу в последний месяц
    if activity.get("count_late_for_work_1m", 0) > 4:
        probability *= 1.1
    elif activity.get("count_late_for_work_1m", 0) > 8:
        probability *= 1.4

    # Ранний уход с работы в последний месяц
    if activity.get("count_early_from_work_1m", 0) > 8:
        probability *= 1.1
    elif activity.get("count_early_from_work_1m", 0) > 12:
        probability *= 1.3

    # Много отгулов за последние 3 месяца
    if activity.get("count_day_off_3m", 0) > 4:
        probability *= 1.4
    elif activity.get("count_day_off_3m", 0) > 8:
        probability *= 1.9

    # Руководящая должность
    if employee.is_head:
        probability *= 0.2

    # Наличие ипотеки
    if employee.living.mortgage:
        probability *= 0.1

    # Длительные коммандировки
    if employee.business_trip_days > 80:
        probability *= 1.5

    # Долгое неповышение в должности
    if date.today() - employee.promotion_workingday > timedelta(days=3*365):
        probability *= 1.5

    return min(probability, 0.95)
