#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bus.app import app
from bus import models  # noqa


def main():
    '''
    '''
    from db import init_db
    init_db("hr", "events")

    app.main()
