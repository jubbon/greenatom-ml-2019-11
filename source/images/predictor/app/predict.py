#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from catboost import Pool, CatBoostClassifier
import math
import random
import os
import sys
import numpy as np
from datetime import datetime
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle

pd.set_option('mode.chained_assignment', None)

demoFilePath = os.path.join(os.getenv('DATA_DIR', '.'), 'demo')
trainFilePath = os.path.join(os.getenv('DATA_DIR', '.'), 'train')

'''
    Загрузка обученной модели
    fname - наименование файла

    Возвращает классификатор
'''
def loadData (fname):
    model = CatBoostClassifier()
    model.load_model(fname, format='cbm')

    return model


def main():
    ''' Применяет модель для предсказания
    '''
    try:
        print('Чтение демонстрационных данных', flush=True)
        demo_persons = pd.read_excel(demoFilePath + '/hr.xls', sheet_name='Персонал', dtype={'Дата увольнения':str}, na_rep ='')
        # удаление значений nan
        demo_persons = demo_persons.fillna('')
        # табельные номера
        TabelNumbers = demo_persons['Табельный номер'].values.tolist()
        # удаление столбцов
        demo_persons.drop(['Фамилия', 'Имя', 'Отчество', 'Статус', 'Дата увольнения' ], axis=1, inplace = True)
        # конвертация значений в строки
        for index in range (len(demo_persons['Дата рождения'].values)):
            demo_persons.at[index, 'Дата рождения'] =  float((datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d') - datetime.strptime(demo_persons.at[index, 'Дата рождения'] , '%Y-%m-%d')).days/365)

        for index in range (len(demo_persons['Дата выхода на работу'].values)):
            demo_persons.at[index, 'Дата выхода на работу'] =  int((datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d') - datetime.strptime(demo_persons.at[index, 'Дата выхода на работу'] , '%Y-%m-%d')).days)

        for index in range (len(demo_persons['Дата последнего повышения'].values)):
            demo_persons.at[index, 'Дата последнего повышения'] =  int((datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d') - datetime.strptime(demo_persons.at[index, 'Дата последнего повышения'] , '%Y-%m-%d')).days)

        demo_persons = demo_persons.astype({"Дата рождения": float, "Дата выхода на работу": int, "Дата последнего повышения": int})

        ExcelList = ['Вовлеченность', 'Бытовые условия', 'Компетенции', 'Семейное положение']
        for index in ExcelList:
            tmp = pd.read_excel(demoFilePath + '/hr.xls', sheet_name=index, na_rep ='')
            tmp = tmp.fillna('')
            demo_persons = pd.merge(demo_persons, tmp, left_on='Табельный номер', right_on='Табельный номер')

        demo_persons.drop(['Табельный номер' ], axis=1, inplace = True)

        columnNames = list ()
        with open (demoFilePath + '/columnNames', 'rb') as fp:
            columnNames = pickle.load(fp)

        # Обнуление несуществующих колонок
        for cname in columnNames:
            if cname in demo_persons.columns:
                pass
            else:
                if not cname.find('Статус'):
                    pass
                else:
                    demo_persons[cname] = 0

        demo_persons = demo_persons.fillna(0)

        demo_persons.sort_index(axis=1, inplace=True)
        demo_data = demo_persons.values.tolist()
        #print(len(demo_persons.columns.tolist()), flush=True)
        categorical_features_indices = np.where((demo_persons.dtypes != np.int32) & (demo_persons.dtypes != np.float64) & (demo_persons.dtypes != np.int64))[0]
        demo_dataset = Pool(data=demo_data, label = demo_persons['Статус'].values.tolist(), cat_features=categorical_features_indices)

        print('Инициализация модели', flush=True)
        model = loadData (demoFilePath + '/model.cbm')
        print('Прогнозирование', flush=True)
        preds_class = model.predict(demo_dataset)
        preds_proba = model.predict_proba(demo_dataset)

        #print('Точность прогнозирования модели: {:.4}'.format(accuracy_score(demo_persons['Статус'].values.tolist(), model.predict(demo_dataset))), flush=True)

        print('Сохранение результатов прогнозирования', flush=True)
        with open(demoFilePath + '/dismissal.csv', mode='w') as csv_file:
            csv_file.write('Табельный номер,Вероятность увольнения\n')
            for tabel, probability in zip(TabelNumbers, preds_proba):
                csv_file.write(str(tabel) + ',' + str(float('{:.3f}'.format(probability[1]))) + '\n')
            csv_file.close()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
