#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .unit import load as load_units
from .staff import load as load_staff
from .skill import load as load_skills


def load_data(filename):
    '''
    '''
    load_units(filename)
    load_staff(filename)
    load_skills(filename)
