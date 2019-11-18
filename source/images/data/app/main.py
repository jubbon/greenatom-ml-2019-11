#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
import xlsxwriter
import random

from data import persons, filter_by_last_name
from data import skills as get_skills
from data import activities as get_activities
from data.skills import names as skill_names
from data import departments
from data.project import projects as all_projects
from utils import make_sure_directory_exists

from dismissal import get_dismissal_probability


def generate_data(locale: str):
    '''
    '''
    # Проекты
    projects_count = random.randint(15, 25)
    projects = list(all_projects(count=projects_count, locale="ru"))

    # Штатное расписание
    units, positions, _ = departments(projects)

    employees = dict()
    skills = dict()
    activities = dict()
    dismissal = dict()

    for employee, skill, activity in zip(
        persons(
            units,
            positions,
            projects,
            locale=locale,
            filters=[filter_by_last_name, ]),
        get_skills(positions, locale=locale),
        get_activities(positions, periods=('1m', '2m', '3m'), locale=locale)):

        # Расчет вероятности увольнения
        dismissal_probability = get_dismissal_probability(employee, skill, activity)
        assert 0.0 <= dismissal_probability < 1.0
        if random.random() < dismissal_probability:
            # Сотрудник уже уволен
            employee.dismiss()

        employees[employee.uid] = employee
        skills[employee.uid] = skill
        activities[employee.uid] = activity
        dismissal[employee.uid] = {
            "Табельный номер": employee.uid,
            "Вероятность увольнения": round(dismissal_probability, 3)
            }

    return projects, units, employees, skills, activities, dismissal


def save_excel(filename: str, projects: list, units: list, employees: dict, skills: dict, locale: str):
    ''' Save Excel file with fake data
    '''
    print(f"Saving file '{filename}'", flush=True)

    workbook = xlsxwriter.Workbook(
        make_sure_directory_exists(filename))

    # Подразделения
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
    worksheet_projects.write(0, 1, "Дата начала")
    worksheet_projects.write(0, 2, "Дата завершения")
    worksheet_projects.write(0, 3, "Важность")
    for n, skill_name in enumerate(skill_names(), 1):
        worksheet_projects.write(0, n + 5, skill_name)
    for i, project in enumerate(projects, 1):
        worksheet_projects.write(i, 0, project.name)
        worksheet_projects.write(i, 1, str(project.started_at))
        worksheet_projects.write(i, 2, str(project.finished_at))
        worksheet_projects.write(i, 3, project.priority_str(locale))
        for n, skill_name in enumerate(skill_names(), 1):
            worksheet_projects.write(i, n + 5, project.skills.get(skill_name, 0))

    # Сотрудники
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
    for i, (employee_uid, employee) in enumerate(employees.items(), 1):
        assert employee.last_name[0] != "Ё", employee.last_name
        worksheet_staff.write(i, 0, employee_uid)
        worksheet_staff.write(i, 1, employee.last_name)
        worksheet_staff.write(i, 2, employee.first_name)
        worksheet_staff.write(i, 3, employee.patronymic)
        worksheet_staff.write(i, 4, employee.gender)
        worksheet_staff.write(i, 5, str(employee.birthday))
        worksheet_staff.write(i, 6, employee.department)
        worksheet_staff.write(i, 7, employee.position)
        worksheet_staff.write(i, 8, "Да" if employee.is_head else "Нет")
        worksheet_staff.write(i, 9, employee.status)
        worksheet_staff.write(i, 10, str(employee.first_workingday))
        worksheet_staff.write(i, 11, str(employee.promotion_workingday))
        worksheet_staff.write(i, 12, "" if employee.last_workingday is None else str(employee.last_workingday))
        worksheet_staff.write(i, 13, employee.business_trip_count)
        worksheet_staff.write(i, 14, employee.business_trip_days)

    # Вовлеченность в проекты
    worksheet_involvement = workbook.add_worksheet("Вовлеченность")
    worksheet_involvement.write(0, 0, "Табельный номер")
    for n, project in enumerate(projects):
        worksheet_involvement.write(0, 1 + n, project.name)
    for i, (employee_uid, employee) in enumerate(employees.items(), 1):
        worksheet_involvement.write(i, 0, employee.uid)
        for n, project in enumerate(projects):
            project_name = project.name
            worksheet_involvement.write(i, 1 + n, employee.involvement.get(project_name, 0))

    # Контакты
    worksheet_contacts = workbook.add_worksheet("Контакты")
    worksheet_contacts.write(0, 0, "Табельный номер")
    worksheet_contacts.write(0, 1, "Адрес электронной почты")
    for i, (employee_uid, employee) in enumerate(employees.items(), 1):
        worksheet_contacts.write(i, 0, employee_uid)
        worksheet_contacts.write(i, 1, employee.contacts.email)

    # Семейное положение
    worksheet_family = workbook.add_worksheet("Семейное положение")
    worksheet_family.write(0, 0, "Табельный номер")
    worksheet_family.write(0, 1, "Статус")
    worksheet_family.write(0, 2, "Количество детей")
    worksheet_family.write(0, 3, "Местный специалист")
    for i, (employee_uid, employee) in enumerate(employees.items(), 1):
        worksheet_family.write(i, 0, employee_uid)
        worksheet_family.write(i, 1, employee.family.status)
        worksheet_family.write(i, 2, employee.family.children_count)
        worksheet_family.write(i, 3, employee.family.local)

    # Бытовые условия
    worksheet_living = workbook.add_worksheet("Бытовые условия")
    worksheet_living.write(0, 0, "Табельный номер")
    worksheet_living.write(0, 1, "Тип жилья")
    worksheet_living.write(0, 2, "Удаленность от места работы")
    worksheet_living.write(0, 3, "Ипотека")
    worksheet_living.write(0, 4, "Наличие дачи")
    for i, (employee_uid, employee) in enumerate(employees.items(), 1):
        worksheet_living.write(i, 0, employee_uid)
        worksheet_living.write(i, 1, employee.living.dwelling_type)
        worksheet_living.write(i, 2, employee.living.distance)
        worksheet_living.write(i, 3, "Да" if employee.living.mortgage else "Нет")
        worksheet_living.write(i, 4, "Да" if employee.living.country_house else "Нет")

    # Компетенции
    worksheet_skills = workbook.add_worksheet("Компетенции")
    worksheet_skills.write(0, 0, "Табельный номер")
    for n, skill_name in enumerate(skill_names(), 1):
        worksheet_skills.write(0, n, skill_name)
    for i, (employee_uid, skills) in enumerate(skills.items(), 1):
        worksheet_skills.write(i, 0, employee_uid)
        for n, skill_name in enumerate(skill_names(), 1):
            worksheet_skills.write(i, n, skills.get(skill_name, 0))

    workbook.close()


def save_csv(filename: str, data: dict, locale: str):
    ''' Save CSV file with fake data
    '''
    import csv
    print(f"Saving file '{filename}'", flush=True)

    with open(filename, mode='wt', encoding="utf-8") as f:
        fieldnames = ["uid", ] + list(list(data.values())[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Проверка на пустой файл
        if os.lseek(f.fileno(), 0, os.SEEK_CUR) == 0:
            writer.writeheader()

        for uid, entry in data.items():
            entry.update(uid=uid)
            writer.writerow(entry)


@click.command()
@click.option('--locale', type=str, default='ru')
@click.option('--activity', type=bool, is_flag=True, default=False)
@click.option('--dismissal', type=bool, is_flag=True, default=False)
@click.argument('output', type=str)
@click.argument('count', type=int, default=1)
def generate(output: str, count: int, locale: str, activity: bool, dismissal: bool):
    ''' Generate Excel file with fake staff
    '''
    playbooks = list()
    if output == "train":
        for i in range(count):
            playbooks.append(os.path.join("train", f"{i:02}"))
    else:
        playbooks.append(output)
    for playbook in playbooks:
        output_dir = os.path.join(os.getenv("DATA_DIR", "."), playbook)

        projects, units, employees, skills, activities, dismissals = generate_data(locale)

        output_filename_xls = os.path.join(output_dir, "hr.xls")
        save_excel(output_filename_xls, projects, units, employees, skills, locale)

        if activity:
            output_filename_csv = os.path.join(output_dir, "activities.csv")
            save_csv(output_filename_csv, activities, locale)

        if dismissal:
            output_filename_csv = os.path.join(output_dir, "dismissal.csv")
            save_csv(output_filename_csv, dismissals, locale)
