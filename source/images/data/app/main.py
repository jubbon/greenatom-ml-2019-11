#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
import xlsxwriter
import random

from data import persons, filter_by_last_name
from data import skills
from data.skills import names as skill_names
from data import departments
from data.project import projects as all_projects
from utils import make_sure_directory_exists


def generate_excel(filename: str, locale: str):
    ''' Generate Excel file with fake staff
    '''
    print(f"Generating file '{filename}'", flush=True)

    workbook = xlsxwriter.Workbook(
        make_sure_directory_exists(filename))

    # Проекты
    projects_count = random.randint(15, 25)
    projects = list(all_projects(count=projects_count, locale="ru"))

    # Штатное расписание
    units, positions, _ = departments(projects)

    worksheet_units = workbook.add_worksheet("Оргструктура")
    worksheet_units.write(0, 0, "Тип")
    worksheet_units.write(0, 1, "Номер")
    worksheet_units.write(0, 2, "Родительская структура")
    for n, project in enumerate(projects):
        worksheet_units.write(0, 5 + n, project.name)

    for i, unit in enumerate(units, 1):
        worksheet_units.write(i, 0, unit[0])
        worksheet_units.write(i, 1, unit[1])
        worksheet_units.write(i, 2, unit[2] + ' ' + unit[3])
        for n, project in enumerate(projects):
            worksheet_units.write(i, 5 + n, "1" if project in unit[4] else "0")

    # Проекты
    worksheet_projects = workbook.add_worksheet("Проекты")
    worksheet_projects.write(0, 0, "Название")
    for n, skill_name in enumerate(skill_names(), 1):
        worksheet_projects.write(0, n, skill_name)
    for i, project in enumerate(projects, 1):
        worksheet_projects.write(i, 0, project.name)
        for n, skill_name in enumerate(skill_names(), 1):
            worksheet_projects.write(i, n, project.skills.get(skill_name, 0))

    # Персонал
    worksheet_staff = workbook.add_worksheet("Персонал")
    worksheet_staff.write(0, 0, "Табельный номер")
    worksheet_staff.write(0, 1, "Фамилия")
    worksheet_staff.write(0, 2, "Имя")
    worksheet_staff.write(0, 3, "Отчество")
    worksheet_staff.write(0, 4, "Пол")
    worksheet_staff.write(0, 5, "Дата рождения")
    worksheet_staff.write(0, 6, "Подразделение")
    worksheet_staff.write(0, 7, "Должность")
    worksheet_staff.write(0, 8, "Руководитель")
    worksheet_staff.write(0, 9, "Статус")
    worksheet_staff.write(0, 10, "Дата выхода на работу")
    worksheet_staff.write(0, 11, "Дата последнего повышения")
    worksheet_staff.write(0, 12, "Дата увольнения")
    worksheet_staff.write(0, 13, "Количество командировок за год")
    worksheet_staff.write(0, 14, "Дней в командировках за год")

    # Вовлеченность в проекты
    worksheet_involvement = workbook.add_worksheet("Вовлеченность")
    worksheet_involvement.write(0, 0, "Табельный номер")
    for n, project in enumerate(projects):
        worksheet_involvement.write(0, 1 + n, project.name)

    worksheet_family = workbook.add_worksheet("Семейное положение")
    worksheet_family.write(0, 0, "Табельный номер")
    worksheet_family.write(0, 1, "Статус")
    worksheet_family.write(0, 2, "Количество детей")
    worksheet_family.write(0, 3, "Местный специалист")

    worksheet_skills = workbook.add_worksheet("Компетенции")
    skill_columns = dict()
    for i, (staff, skill) in enumerate(
        zip(
            (
            persons(
                units,
                positions,
                projects,
                locale=locale,
                filters=[filter_by_last_name,])),
            skills(positions, locale=locale)
            ), 1):

        assert staff.last_name[0] != "Ё", staff.last_name
        worksheet_staff.write(i, 0, staff.uid)
        worksheet_staff.write(i, 1, staff.last_name)
        worksheet_staff.write(i, 2, staff.first_name)
        worksheet_staff.write(i, 3, staff.patronymic)
        worksheet_staff.write(i, 4, staff.gender)
        worksheet_staff.write(i, 5, str(staff.birthday))
        worksheet_staff.write(i, 6, staff.department)
        worksheet_staff.write(i, 7, staff.position)
        worksheet_staff.write(i, 8, "Да" if staff.is_head else "Нет")
        worksheet_staff.write(i, 9, staff.status)
        worksheet_staff.write(i, 10, str(staff.first_workingday))
        worksheet_staff.write(i, 11, str(staff.promotion_workingday))
        worksheet_staff.write(i, 12, "" if staff.last_workingday is None else str(staff.last_workingday))
        worksheet_staff.write(i, 13, staff.business_trip_count)
        worksheet_staff.write(i, 14, staff.business_trip_days)

        worksheet_involvement.write(i, 0, staff.uid)
        for n, project in enumerate(projects):
            project_name = project.name
            worksheet_involvement.write(i, 1 + n, staff.involvement.get(project_name, 0))

        worksheet_skills.write(i, 0, staff.uid)
        for skill_name, skill_value in skill.items():
            worksheet_skills.write(
                i,
                skill_columns.setdefault(skill_name, len(skill_columns)+1),
                skill_value)

        worksheet_family.write(i, 0, staff.uid)
        worksheet_family.write(i, 1, staff.family.status)
        worksheet_family.write(i, 2, staff.family.children_count)
        worksheet_family.write(i, 3, staff.family.local)

    assert i == len(positions), f"{i} != {len(positions)}"

    worksheet_skills.write(0, 0, "Табельный номер")
    for skill_name, column_number in skill_columns.items():
        worksheet_skills.write(0, column_number, skill_name)

    workbook.close()
    print(f"Created {i} entries", flush=True)


@click.command()
@click.option('--locale', type=str, default='ru')
@click.argument('output', type=str)
@click.argument('count', type=int, default=1)
def generate(output: str, count: int, locale: str):
    ''' Generate Excel file with fake staff
    '''
    playbooks = list()
    if output == "train":
        for i in range(count):
            playbooks.append(os.path.join("train", f"{i:02}"))
    else:
        playbooks.append(output)
    for playbook in playbooks:
        output_filename = os.path.join(
            os.getenv("DATA_DIR", "."),
            playbook,
            "hr.xls")
        generate_excel(output_filename, locale)
