#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


class Clock():
    '''
    '''
    def __init__(self, env, timeout):
        self.env = env
        self.timeout = timeout
        self.action = env.process(self.run())

    def run(self):
        '''
        '''
        while True:
            now = datetime.fromtimestamp(self.env.now)
            print(f"[{now:%d.%m %H:%M}] {self.env.status}", flush=True)
            yield self.env.timeout(self.timeout)
