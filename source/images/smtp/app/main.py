#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from email.message import EmailMessage
from smtplib import SMTP_SSL

from smart_hr.bus.app import app
from smart_hr.bus.models.email import topic


@app.agent(topic)
async def handler(messages):
    async for message in messages:
        print(f"Send email '{message.text}' to '{message.to}'", flush=True)
        try:
            emsg = EmailMessage()
            emsg.set_content(message.text)
            emsg['From'] = os.getenv("SMTP_USERNAME")
            emsg['To'] = message.to
            emsg['Subject'] = message.subject

            smtp_server = os.getenv("SMTP_SERVER")
            s = SMTP_SSL(smtp_server)

            username = os.getenv("SMTP_USERNAME")
            password = os.getenv("SMTP_PASSWORD")
            s.login(username, password)
            try:
                s.send_message(emsg)
            finally:
                s.quit()
        except Exception as err:
            print(f"[ERROR]: {err}", flush=True)
        yield "OK"


def main():
    app.main()
