#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

from tasks import send_email
from tasks.expert import find_experts


def brief(window, person):
    ''' Краткая информация о сотруднике
    '''
    assert person
    window.image(person.image_filename, use_column_width=True)
    window.markdown(
        f'''
        **ФИО:** {person.fullname}

        **Возраст:** {person.ages}

        **Должность:** {person.job}'''
    )


def info(window, person, locale=None):
    ''' Общая информация о сотруднике
    '''
    assert person
    window.subheader("Общая информация")

    data = person.to_dict(locale)
    for feature in ("is_head", "status", "image_number", "projects", "contacts", "ФИО", "is_dismissed", "promotion_workingday"):
        if feature in data:
            del data[feature]
    df = pd.DataFrame(
        data.values(),
        index=data.keys(),
        columns=["", ])
    window.table(df)


def family_and_living(window, person, locale=None):
    ''' Семейное положение и бытовые условия
    '''
    assert person
    window.subheader("Семейное положение и бытовые условия")

    data = dict()
    data.update(person.family.to_dict(locale))
    data.update(person.living.to_dict(locale))
    df = pd.DataFrame(
        data.values(),
        index=data.keys(),
        columns=["", ])
    window.table(df)


def skill(window, person):
    ''' Компетенции сотрудника
    '''
    assert person
    window.subheader("Компетенции сотрудника")

    person_skills = {k: v for k, v in person.skills() if v}
    df_skills = pd.DataFrame(
        person_skills.values(),
        index=person_skills.keys(),
        columns=["Уровень", ])
    window.table(df_skills)

    def get_experts(person):
        experts = dict()
        for skill_name, skill_value, expert in find_experts(person):
            experts.setdefault(skill_name, list()).append({
                "Эксперт": expert.fullname,
                "Подразделение": expert.unit,
                "Электронная почта": expert.contacts.email,
                "Уровень компетенции": skill_value
            })
        return experts

    send_to = window.text_input("Рекомендации отправить по электронной почте", f"{person.contacts.email}", key="email")
    find_experts_button = window.button("Подобрать экспертов", key="find_experts")
    if find_experts_button:
        report = f"Рекомендованные эксперты для сотрудника {person.fullname}"
        for skill_name, experts_ in get_experts(person).items():
            window.text(f"Эксперты по {skill_name}")
            df_experts = pd.DataFrame(experts_)
            window.table(df_experts)
            report += "\n"
            report += f"Эксперты по {skill_name}"
            report += df_experts.to_html()

        if send_to:
            subject = "[SmartHR] Рекомендованные эксперты"
            print(report, flush=True)
            if send_email(to=send_to, subject=subject, text=report):
                window.success(f"Письмо с рекомендованными экспертами было отправлено на электронную почту '{send_to}'")


def dismiss(window, person):
    ''' Увольнение
    '''
    assert person
    window.subheader("Увольнение")
    if window.button("Рассчитать вероятность увольнения", key="predict_dismiss"):
        dismissal = person.dismissal(feature_importance_count=8)
        if dismissal:
            probability, feature_importance = dismissal
            window.markdown(
                f"Вероятность увольнения составляет **{round(probability*100)}%**")
            if feature_importance:
                df = pd.DataFrame(feature_importance).set_index('feature_name')
                df.rename(columns={
                    'importance': 'Важность',
                    'value': 'Значение'
                    }, inplace=True)
                window.table(df)
        else:
            window.error("Служба предсказаний временно недоступна")
