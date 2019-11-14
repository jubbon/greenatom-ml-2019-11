#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from datetime import datetime
from uuid import uuid4

from smart_hr.bus.models.lync import handler, Message


async def fetch_messages(every: int) -> None:
    '''
    '''
    while True:
        message = Message(
            uid=str(uuid4()),
            sender="Dmitry",
            recipient="Aidar",
            sended_at=datetime(2019, 10, 13, 12, 34, 56),
            received_at=datetime(2019, 10, 13, 14, 24, 18),
            text="Привет! Есть вопрос по проекту Омега")
        print(f"Send message '{message.uid}'", flush=True)
        handler.cast(value=message)
        await asyncio.sleep(every)


def main():
    '''
    '''
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_messages(every=5))
