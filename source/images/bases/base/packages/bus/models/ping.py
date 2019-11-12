#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..app import app


topic = app.topic("ping", value_type=str)


@app.agent(topic)
async def handler(messages):
    async for message in messages:
        print(message, flush=True)
        yield "OK"
