#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_dismissal_probability(employee, skill, activity) -> float:
    '''
    '''
    probability = 0.1
    if skill.get("tech:programming:JavaScript", 0) > 5:
        probability *= 1.4
    if skill.get("tech:programming:python", 0) > 8:
        probability *= 1.2

    if activity.get("count_late_for_work_1m", 0) > 4:
        probability *= 1.1
    elif activity.get("count_late_for_work_1m", 0) > 8:
        probability *= 1.4

    if activity.get("count_early_from_work_1m", 0) > 8:
        probability *= 1.1
    elif activity.get("count_early_from_work_1m", 0) > 12:
        probability *= 1.3

    if activity.get("count_day_off_3m", 0) > 4:
        probability *= 1.4
    elif activity.get("count_day_off_3m", 0) > 8:
        probability *= 1.9

    return min(probability, 0.95)
