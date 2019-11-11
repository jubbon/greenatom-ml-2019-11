#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import xlsxwriter

from data import persons, filter_by_last_name
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
    units, positions = departments()
    worksheet_units = workbook.add_worksheet("Оргструктура")
    worksheet_units.write(0, 0, "Тип")
    worksheet_units.write(0, 1, "Номер")
    worksheet_units.write(0, 2, "Родительская структура")
    for i, unit in enumerate(units, 1):
        worksheet_units.write(i, 0, unit[0])
        worksheet_units.write(i, 1, unit[1])
        worksheet_units.write(i, 2, unit[2] + ' ' + unit[3])

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
    worksheet_staff.write(0, 8, "Статус")
    worksheet_staff.write(0, 9, "Дата выхода на работу")
    worksheet_staff.write(0, 10, "Дата последнего повышения")
    worksheet_staff.write(0, 11, "Дата увольнения")
    worksheet_staff.write(0, 12, "Количество командировок за год")
    worksheet_staff.write(0, 13, "Дней в командировках за год")

    worksheet_skills = workbook.add_worksheet("Компетенции")
    skill_columns = dict()
    for i, (staff, skill) in enumerate(
        zip(
            filter_by_last_name(
                persons(positions, locale='ru')),
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
        worksheet_staff.write(i, 8, staff.status)
        worksheet_staff.write(i, 9, str(staff.first_workingday))
        worksheet_staff.write(i, 10, str(staff.promotion_workingday))
        worksheet_staff.write(i, 11, "" if staff.last_workingday is None else str(staff.last_workingday))
        worksheet_staff.write(i, 12, staff.business_trip_count)
        worksheet_staff.write(i, 13, staff.business_trip_days)

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
