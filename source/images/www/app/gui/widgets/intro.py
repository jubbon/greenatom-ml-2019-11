#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
from collections import OrderedDict

import pandas as pd

from app.tasks import analyze_text


def banner(window, image: str = "banner.jpg"):
    '''
    '''
    window.image(
        image=os.path.join(
            os.getenv("IMAGE_DIR", "."),
            image),
        use_column_width=True)


def nlp(window, locale=None):
    ''' Виджет для работы с NLP
    '''
    window.subheader(f"Обработка естественного языка")
    initial_text = '- Андрей, привет! Как дела? Что нового?\n- Завтра едем в Москву для презентации проекта. Ура!\n- Я ненавижу ездить в поездах РЖД, просто замучился!\n- Тогда полетим на самолете Аэрофлота'
    text = window.text_area('Введите текст для анализа', initial_text)
    if text:
        # TODO: делать запрос в DeepPavlov
        sentences = text.split('\n')
        res_ner, res_sen = analyze_text(sentences)
        print(f"Сущности: {res_ner}", flush=True)
        print(f"Тональность: {res_sen}", flush=True)
        for sentence_ner, sentence_sen in zip(res_ner, res_sen):
            assert sentence_ner[0] == sentence_sen[0]
            window.markdown(f"#### {sentence_ner[0]}")

            tonality = sentence_sen[1][0]
            if tonality == 'negative':
                window.error('Отрицательная тональность')
            elif tonality == 'speech':
                window.info('Разговорная речь')
            elif tonality == 'neutral':
                window.info('Нейтральная тональность')
            elif tonality == 'positive':
                window.success('Положительная тональность')
            else:
                window.warning(tonality)

            data = list()
            index = list()
            for number, word, entity_type in sentence_ner[1]:
                if 'LOC' in entity_type:
                    entity_type = "место"
                elif 'PER' in entity_type:
                    entity_type = "персона"
                elif 'ORG' in entity_type:
                    entity_type = "организация"
                data.append({"Слово": word, "Тип": entity_type})
                index.append(number)
            if data:
                df = pd.DataFrame(data, index=index)
                window.table(df)
