#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from catboost import Pool, CatBoostClassifier
from catboost.utils import eval_metric
import math
import random
import os
import sys
import numpy as np
from datetime import datetime
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import pickle

pd.set_option('mode.chained_assignment', None)

trainFilePath = os.path.join(os.getenv('DATA_DIR', '.'), 'train')
demoFilePath = os.path.join(os.getenv('DATA_DIR', '.'), 'demo')
modelsDirPath = os.getenv('MODELS_DIR', '.')

'''
    Рекурсивный поиск файла в подкаталогах каталога
    catalog - корень, где искать
    f - имя файла

    Возвращает список всех найденных файлов
'''
def find_files(catalog, f):
    print('Запущен поиск файлов в каталоге: {}'.format(catalog), flush=True)
    find_files = []
    for root, dirs, files in os.walk(catalog):
        find_files += [os.path.join(root, name) for name in files if name == f]
    print('Завершен поиск файлов. Обнаружено {} файла(ов)'.format(str(len(find_files))), flush=True)
    return find_files

'''
    Подготовка входных данных
    pathlist - список файлов

    Возвращает обучающую выборку, метки принадлежности к классу
'''
def prepareInputData (pathlist):
    dataFrame = pd.DataFrame()

    # проверка существования подготовленных данных
    if os.path.exists( trainFilePath + '/dataframe.csv'):
        print('Обнаружены ранее подготовленные данные', flush=True)
        dataFrame = pd.read_csv( trainFilePath + '/dataframe.csv')
        dataFrame.drop(['Unnamed: 0' ], axis=1, inplace = True)
    else:
        for path in pathlist:
            print('Обработка файла: {}'.format(path), flush=True)
            persons = pd.read_excel(path, sheet_name='Персонал', dtype={'Дата увольнения':str}, na_rep ='')
            # удаление значений nan
            persons = persons.fillna('')
            # удаление столбцов
            persons.drop(['Фамилия', 'Имя', 'Отчество', 'Дата увольнения' ], axis=1, inplace = True)
            # конвертация значений в строки
            for index in range (len(persons['Дата рождения'].values)):
                persons.at[index, 'Дата рождения'] =  float((datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')-datetime.strptime(persons.at[index, 'Дата рождения'] , '%Y-%m-%d')).days/365)

            for index in range (len(persons['Дата выхода на работу'].values)):
                persons.at[index, 'Дата выхода на работу'] =  int((datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')-datetime.strptime(persons.at[index, 'Дата выхода на работу'] , '%Y-%m-%d')).days)

            for index in range (len(persons['Дата последнего повышения'].values)):
                persons.at[index, 'Дата последнего повышения'] =  int((datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')-datetime.strptime(persons.at[index, 'Дата последнего повышения'] , '%Y-%m-%d')).days)

            persons = persons.astype({"Дата рождения": float, "Дата выхода на работу": int, "Дата последнего повышения": int})

            # Обработка других листов файла
            ExcelList = ['Бытовые условия', 'Компетенции', 'Семейное положение']
            for index in ExcelList:
                tmp = pd.read_excel(path, sheet_name=index, na_rep ='')
                tmp = tmp.fillna('')
                persons = pd.merge(persons, tmp, left_on='Табельный номер', right_on='Табельный номер')

            # Чтение активности сотрудников
            head, tail = os.path.split(path)
            act = head + '/activities.csv'
            if os.path.exists( act ):
                print('Обработка файла: {}'.format(act), flush=True)
                activities = pd.read_csv(act, sep=',')
                activities = activities.fillna('')
                persons = pd.merge(persons, activities, left_on='Табельный номер', right_on='uid')
                persons.drop(['uid' ], axis=1, inplace = True)

            # Накопление данных
            dataFrame = pd.concat([dataFrame, persons],sort=False)
        # Обнуление полей nan, после слияния таблиц
        dataFrame = dataFrame.fillna(0)

        print('Сохранение файла со считанными данными', flush=True)
        dataFrame.to_csv( trainFilePath + '/dataframe.csv')

    dataFrame.sort_index(axis=1, inplace=True)
    # Разделение данных 80% - обучение 20% - валидация
    train, test = train_test_split(dataFrame, test_size=0.2)

    # Столбец, который необходимо прогнозировать
    train_label = train['Статус_x'].values.tolist()
    test_label = test['Статус_x'].values.tolist()

    # Удаление ненужных столбцов
    train.drop(['Табельный номер', 'Статус_x'], axis=1, inplace = True)
    test.drop(['Табельный номер', 'Статус_x'], axis=1, inplace = True)
    dataFrame.drop(['Табельный номер', 'Статус_x'], axis=1, inplace = True)

    datalist80 = train.values.tolist()
    datalist20 = test.values.tolist()

    dataFrame.rename(columns={"Статус_y": "Статус"}, errors="raise")

    # Список колонок
    columnNames = dataFrame.columns.tolist()
    #print(dataFrame.columns.tolist(), flush=True)
    #print (dataFrame.dtypes, flush=True)

    # Определение категориальных фитч
    categorical_features_indices = np.where((dataFrame.dtypes != np.int32) & (dataFrame.dtypes != np.float64) & (dataFrame.dtypes != np.int64))[0]

    return train_label, datalist80, test_label, datalist20, columnNames, categorical_features_indices

'''
    Сохранение обученной модели
    model - классификатор
    fname - наименование файла
    pool - считанные данные
'''
def saveData (model, fname, pool):
    model.save_model(fname, format="cbm", pool=pool)

def main():
    ''' Обучает модель
    '''

    try:
        print(f"Начинается обучение модели", flush=True)
        print('Запущен процесс подготовки данных', flush=True)
        train_label, datalist80, test_label, datalist20, columnNames, categorical_features_indices = \
        prepareInputData (find_files(trainFilePath, 'hr.xls'))

        print('Подготовка данных завершена', flush=True)
        print('Количество категориальных фитч: {}'.format(str(len(categorical_features_indices))), flush=True)
        print('Создание dataset для обучения', flush=True)
        train_dataset = Pool(data=datalist80,
                            label=train_label,
                            cat_features=categorical_features_indices)

        print('Создание dataset для валидации', flush=True)
        test_dataset = Pool(data=datalist20,
                            label=test_label,
                            cat_features=categorical_features_indices)

        print('Инициализация классфикатора', flush=True)
        model = CatBoostClassifier(
                                learning_rate=0.05,
                                loss_function='Logloss',
                                use_best_model=True,
                                eval_metric='AUC',
                                depth=5,
                                iterations=100,
                                random_seed=42
                                )

        #custom_metric='Accuracy',
        #eval_metric='Accuracy',

        print('Запуск обучения модели', flush=True)
        model.fit(train_dataset, eval_set=test_dataset)
        print('Обучение модели завершено', flush=True)

        print('Cохранение обученной модели', flush=True)
        saveData(model, modelsDirPath + '/dismissal.cbm', train_dataset)

        print('Точность валидации модели: {:.4}'.format(accuracy_score(test_label, model.predict(datalist20))), flush=True)

        preds_proba = model.predict_proba(datalist20)
        print ( 'ROC AUC Score: {}'.format( roc_auc_score(test_label, preds_proba[:, 1] )), flush=True)

        #print ( model.eval_metrics(train_dataset, metrics=['Precision', 'Logloss', 'AUC', 'Recall', 'Accuracy']), flush=True)

        print('Подготовка списка важности признаков', flush=True)
        feature_importances = model.get_feature_importance(train_dataset)
        feature_names = columnNames
        with open(demoFilePath + '/feature_importance.csv', mode='w') as csv_file:
            csv_file.write('Наименование колонки,Важность\n')
            for score, name in sorted(zip(feature_importances, feature_names), reverse=True):
                csv_file.write(name + ',' + str(score) + '\n')
            csv_file.close()

        with open(demoFilePath + '/columnNames', 'wb') as fp:
            pickle.dump(columnNames, fp)

        print(f"Обучение модели завершено", flush=True)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
