#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import errno
from datetime import date

from mimesis import Datetime


def make_sure_directory_exists(filename):
    '''
    Создает каталог для заданного файла, если он не существует
    '''
    path = os.path.dirname(os.path.abspath(filename))
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return os.path.abspath(filename)


def random_date(start: date, end: date, locale: str) -> date:
    ''' Generate random date between start date and end date
    '''
    if end <= start:
        raise RuntimeError("Bad date range")
    datetime = Datetime(locale)
    while True:
        date = datetime.date(start=start.year, end=end.year)
        if date < start or date >= end:
            continue
        return date
