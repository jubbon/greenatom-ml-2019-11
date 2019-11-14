#!/usr/bin/env python
# -*- coding: utf-8 -*-

import faust

from ..app import app


class Employee(faust.Record):
    ''' Сотрудник
    '''
    # Уникальный идентификатор
    uid: str


predict_dismiss_topic = app.topic("predict_dismiss", value_type=Employee)

# dismiss_probabilities = app.Table('dismiss_probability_v2', default=float, help="Dismiss probability")
