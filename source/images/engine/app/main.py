#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smart_hr.bus.app import app
from smart_hr.bus.models.ping import topic


@app.agent(topic)
async def handler(messages):
    async for message in messages:
        print(message, flush=True)
        yield "OK"


def main():
    '''
    '''
    from db import init_db
    init_db("hr", "events")

    app.main()
