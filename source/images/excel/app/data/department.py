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


def handle(root: dict, deps: list):
    '''
    '''
    result = list()
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
                        result.append((title, name, position))
                    for job in jobs.get("others", list()):
                        position = job["title"]
                        count = job.get("count", (0, 0))
                        for _ in range(randint(*count)):
                            result.append((title, name, position))
                # Обработка вложенных департаментов
                result.extend(handle(data, dep.get("nested", list())))
    return result


def departments():
    '''
    '''
    return handle(None, DEPARTMENTS_HIERARCHY)
