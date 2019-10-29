#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import faust

app = faust.App(
    'hello-world-1',
    broker='kafka://kafka:9092',
)
ping_topic = app.topic('ping', value_type=str)


@app.agent(ping_topic)
async def ping(messages):
    async for message in messages:
        print(message, flush=True)
    return messages
