#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import faust

from ..app import app


class Message(faust.Record):
    ''' Сообщение Skype for Business (ex Lync)
    '''
    # Уникальный идентификатор сообщения
    uid: str
    # Отправитель
    sender: str
    # Получатель
    recipient: str
    # Дата и время отправки сообщения
    sended_at: datetime
    # Дата и время получения сообщения
    received_at: datetime
    # Текст сообщения
    text: str
    # Идентификатор сообщения,на которое сообщение отвечает
    replay_for: str = None


topic = app.topic("lync", value_type=Message)


@app.agent(topic)
async def handler(messages):
    async for message in messages:
        print(f"lync: {message.text}", flush=True)
