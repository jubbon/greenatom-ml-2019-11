#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


def nlp(window, locale=None):
    ''' Виджет для работы с NLP
    '''
    window.subheader(f"Обработка естественного языка")
    text = window.text_area('Введите текст для анализа', '')
    if text:
        # TODO: делать запрос в DeepPavlov
        tonality = random.choice([-1, 0, 1])
        if tonality < 0:
            window.error(f'Текст несет отрицательную тональность')
        elif tonality == 0:
            window.info(f'Текст несет нейтральную тональность')
        elif tonality > 0:
            window.success(f'Текст несет положительную тональность')
