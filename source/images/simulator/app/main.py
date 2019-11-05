#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


import simpy

from agents import Clock, Staff


class Environment(simpy.Environment):
    '''
    '''
    debug = False

    def __init__(self, **kwargs):
        super(Environment, self).__init__(**kwargs)

        self._clock = Clock(self, timeout=600)

        # Персонал
        self._staff = list()

    @property
    def status(self):
        '''
        '''
        return "OK"

    def add_staff(self, **kwargs):
        '''
        '''
        self._staff.append(Staff(self, kwargs))


def simulate(start_time, finish_time):
    '''
    '''
    assert start_time
    assert finish_time
    env = Environment(initial_time=start_time)
    env.add_staff(
        first_name="Дмитрий"
    )
    env.run(until=finish_time)
    return env


def main():
    '''
    '''
    start_time = datetime(2019, 8, 1).timestamp()
    finish_time = datetime(2019, 8, 2).timestamp()
    # finish_time = datetime(2019, 11, 1).timestamp()

    env = simulate(
        start_time=start_time,
        finish_time=finish_time
    )
    print(env, flush=True)
