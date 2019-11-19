#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from mailer import Mailer, Message

from smart_hr.bus.app import app
from smart_hr.bus.models.email import topic


@app.agent(topic)
async def handler(messages):
    async for message in messages:
        to = os.getenv("SMTP_REDIRECT_TO", message.to)
        print(f"Send email '{message.text}' to '{to}'", flush=True)
        try:
            msg = Message()
            msg.From = "SmartHR Notify Service <SmartHR@inbox.ru>"
            msg.To = to
            msg.Subject = "Список сотрудников-экспертов"
            msg.Html = message.text

            sender = Mailer('smtp.mail.ru', port=465, use_ssl=True, usr='SmartHR@inbox.ru', pwd='greenatomhackathon')
            sender.send(msg)
        except Exception as err:
            print(f"[ERROR]: {err}", flush=True)
        yield "OK"


def main():
    app.main()
