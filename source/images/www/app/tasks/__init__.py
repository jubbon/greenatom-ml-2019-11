#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import subprocess

from bus.models.email import EMail


def _send(app, topic, value):
    ''' Send value to topic
    '''
    assert app
    assert topic
    assert value
    res = subprocess.run([
        "faust",
        "-A",
        app,
        "send",
        topic,
        json.dumps(value.dumps(), ensure_ascii=False)
    ], capture_output=True)
    print(res, flush=True)
    return res.returncode == 0


def send_email(to, subject, text):
    ''' Send email
    '''
    assert to
    assert subject
    assert text
    email = EMail(to=to, subject=subject, text=text)
    return _send("bus.models.email", "email", email)
