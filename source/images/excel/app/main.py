#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import xlsxwriter

from data import persons
from data import skills
from data import departments


@click.command()
@click.argument('output', type=click.File('wb'))
def generate(output):
    ''' Generate Excel file with fake staff
    '''
    print(f"Generating file", flush=True)
    workbook = xlsxwriter.Workbook(output)

    # Штатное расписание
    positions = departments()

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

    worksheet_skills = workbook.add_worksheet("Компетенции")
    skill_columns = dict()
    for i, (staff, skill) in enumerate(
        zip(
            persons(positions, locale='ru'),
            skills(positions, locale='ru')
            ), 1):
        worksheet_staff.write(i, 0, staff.uid)
        worksheet_staff.write(i, 1, staff.last_name)
        worksheet_staff.write(i, 2, staff.first_name)
        worksheet_staff.write(i, 3, staff.patronymic)
        worksheet_staff.write(i, 4, staff.gender)
        worksheet_staff.write(i, 5, str(staff.birthday))
        worksheet_staff.write(i, 6, staff.department)
        worksheet_staff.write(i, 7, staff.position)

        worksheet_skills.write(i, 0, staff.uid)

        for skill_name, skill_value in skill.items():
            worksheet_skills.write(
                i,
                skill_columns.setdefault(skill_name, len(skill_columns)+1),
                skill_value)
    worksheet_skills.write(0, 0, "Табельный номер")
    for skill_name, column_number in skill_columns.items():
        worksheet_skills.write(0, column_number, skill_name)

    workbook.close()
    print(f"Created {i} entries", flush=True)