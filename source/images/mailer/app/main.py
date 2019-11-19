#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from smart_hr.bus.app import app
from smart_hr.bus.models.email import topic


@app.agent(topic)
async def handler(messages):
    async for message in messages:
        to = os.getenv("SMTP_REDIRECT_TO", message.to)
        print(f"Send email '{message.text}' to '{to}'", flush=True)
        try:
            pass
        except Exception as err:
            print(f"[ERROR]: {err}", flush=True)
        yield "OK"


def main():
    app.main()
