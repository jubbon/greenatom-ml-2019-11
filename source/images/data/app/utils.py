#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import errno


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
