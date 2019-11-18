#!/usr/bin/env python
# -*- coding: utf-8 -*-


from smart_hr.data.staff import experts as get_experts


def sortByExpert(obj):
    '''
    '''
    expert, skill_value = obj
    return -skill_value


def find_experts(employee, count=10) -> list:
    ''' Найти экспертов для заданного сотрудника
    '''
    for skill_name, skill_value in employee.skills():
        if skill_value == 0:
            continue
        experts = list(get_experts(skill_name, skill_value, unit=None))
        experts.sort(key=sortByExpert)
        total = 0
        for expert, skill_value in experts:
            if expert == employee:
                # Игнорируем самого себя
                continue
            total += 1
            if total > count:
                break
            yield skill_name, skill_value, expert
