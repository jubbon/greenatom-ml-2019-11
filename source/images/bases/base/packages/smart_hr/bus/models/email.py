#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import faust

from ..app import app


class EMail(faust.Record):
    ''' Сообщение отправляемое по электронной почте
    '''
    # Получатель
    to: str
    # Заголовок сообщения
    subject: str
    # Текст сообщения
    text: str


topic = app.topic("email", value_type=EMail)
