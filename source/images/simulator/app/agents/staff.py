#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import numpy


class Staff():
    '''
    '''
    def __init__(self, env, data):
        '''
        '''
        assert isinstance(data, dict)
        self.env = env
        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")

        # Присутствие на работе
        self._on_work = dict()

        self.action = env.process(self.run())

    @property
    def dayoffset(self):
        '''
        '''
        return int(self.env.now) % 86400

    def run(self):
        '''
        '''
        while True:
            now = datetime.fromtimestamp(self.env.now)
            today = "{:%Y%m%d}".format(now)
            on_work = self._on_work.setdefault(today, dict())
            if "started_at" not in on_work and self.dayoffset > numpy.random.normal(8*3600, 10*60):
                    print(f"[{self.dayoffset}] Hello! I am {self.first_name}, in work", flush=True)
                    on_work["started_at"] = now
            if "started_at" in on_work and "finished_at" not in on_work and self.dayoffset > numpy.random.normal(17*3600 + 12*60, 15*60):
                    print(f"[{self.dayoffset}] Hello! I am {self.first_name}, went out from work", flush=True)
                    on_work["finished_at"] = now
            yield self.env.timeout(60)
