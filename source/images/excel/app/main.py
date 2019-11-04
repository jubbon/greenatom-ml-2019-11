#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import xlsxwriter

from data import persons
from data import departments


@click.command()
@click.argument('output', type=click.File('wb'))
def generate(output):
    ''' Generate Excel file with fake personal
    '''
    print(f"Generating file", flush=True)
    workbook = xlsxwriter.Workbook(output)

    # Штатное расписание
    positions = departments()

    # Персонал
    worksheet = workbook.add_worksheet("Персонал")
    worksheet.write(0, 0, "Табельный номер")
    worksheet.write(0, 1, "Фамилия")
    worksheet.write(0, 2, "Имя")
    worksheet.write(0, 3, "Отчество")
    worksheet.write(0, 4, "Пол")
    worksheet.write(0, 5, "Дата рождения")
    worksheet.write(0, 6, "Подразделение")
    worksheet.write(0, 7, "Должность")
    for i, human in enumerate(persons(positions, locale='ru'), 1):
        worksheet.write(i, 0, human.uid)
        worksheet.write(i, 1, human.last_name)
        worksheet.write(i, 2, human.first_name)
        worksheet.write(i, 3, human.patronymic)
        worksheet.write(i, 4, human.gender)
        worksheet.write(i, 5, str(human.birthday))
        worksheet.write(i, 6, human.department)
        worksheet.write(i, 7, human.position)
    workbook.close()
    print(f"Created {i} entries", flush=True)
