#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import asyncio
from smart_hr.bus.models.employee import dismiss_probabilities


async def send_value(interval: int) -> None:
    '''
    '''
    i = 0
    while True:
        message = f"[{i}] Hello, I am alive"
        print(f"Send message: '{message}'", flush=True)
        ping.cast(value=message)
        i += 1
        await asyncio.sleep(interval)


def main():
    '''
    '''
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_value(15))
