#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

from mimesis.random import Random


DEPARTMENTS_HIERARCHY = [
    {
        "title": "отделение",
        "mask": "##",
        "count": [2, 4],
        "jobs": {
            "head": "начальник отделения"
        },
        "nested": [
            {
                "title": "отдел",
                "mask": "##",
                "count": [3, 10],
                "jobs": {
                    "head": "начальник отдела"
                },
                "nested": [
                    {
                        "title": "лаборатория",
                        "mask": "/1",
                        "count": [1, 3],
                        "jobs": {
                            "head": "начальник лаборатории",
                            "others": [
                                {
                                    "title": "инженер-программист",
                                    "count": [3, 16]
                                },
                                {
                                    "title": "младший научный сотрудник",
                                    "count": [3, 10]
                                },
                                {
                                    "title": "научный сотрудник",
                                    "count": [2, 8]
                                },
                                {
                                    "title": "старший научный сотрудник",
                                    "count": [1, 5]
                                },
                                {
                                    "title": "ведущий научный сотрудник",
                                    "count": [0, 2]
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
]


def handle(root: dict, deps: list, projs: list):
    '''
    '''
    units = list()
    positions = list()
    projects = set()
    if deps:
        random = Random()
        for dep in deps:
            assert isinstance(dep, dict)
            title = dep["title"]
            mask = dep.get("mask", "1")
            count = dep.get("count", (0, 0))
            for i in range(1, randint(*count)+1):
                # Название департамента
                if "1" in mask:
                    name = mask.replace("1", str(i))
                else:
                    name = random.custom_code(mask)
                if root and root.get("name"):
                    name = root.get("name") + name
                data = {
                    "title": title,
                    "name": name
                }
                jobs = dep.get("jobs")
                if jobs:
                    position = jobs.get("head")
                    if position:
                        positions.append((title, name, position))
                    for job in jobs.get("others", list()):
                        position = job["title"]
                        count = job.get("count", (0, 0))
                        for _ in range(randint(*count)):
                            positions.append((title, name, position))
                # Обработка вложенных департаментов
                child_units, child_positions, child_projects = handle(data, dep.get("nested", list()), projs)

                projects_ = set()
                if not child_units:
                    # Проекты в подразделении
                    projects_count = random.randint(1, 2)
                    while len(projects_) < projects_count:
                        projects_.add(random.choice(projs))
                else:
                    projects_.update(child_projects)
                units.append((
                    title,
                    name,
                    root.get("title", ""),
                    root.get("name", ""),
                    list(projects_)))

                units.extend(child_units)
                positions.extend(child_positions)
                projects.update(projects_)

    return units, positions, list(projects)


def departments(projs):
    '''
    '''
    return handle({}, DEPARTMENTS_HIERARCHY, projs)
