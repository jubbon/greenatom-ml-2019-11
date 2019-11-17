#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
import subprocess

from smart_hr.bus.models.email import EMail


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
    return _send("smart_hr.bus.models.email", "email", email)


def analyze_text(sentences: list) -> dict:
    ''' Analyze text with DeepPavlov
    '''
    assert sentences
    data = dict(x=list(sentences))

    res_ner = list()
    try:
        nlp_url_ner = os.getenv("NLP_URL_NER", "http://localhost:5000/model")
        r = requests.post(nlp_url_ner, data=json.dumps(data))
        result = json.loads(r.text)
        for i, sentence in enumerate(result):
            entities = list()
            for n, (token, token_kind) in enumerate(zip(*sentence), 1):
                if token_kind == "O":
                    continue
                entities.append((n, token, token_kind))
            res_ner.append((sentences[i], entities))
    except Exception as err:
        print(f"[ERROR] {err}", flush=True)

    res_sen = list()
    try:
        nlp_url_sen = os.getenv("NLP_URL_SEN", "http://localhost:5000/model")
        r = requests.post(nlp_url_sen, data=json.dumps(data))
        result = json.loads(r.text)
        print(result, flush=True)
        for i, sentence in enumerate(result):
            res_sen.append((sentences[i], sentence))
    except Exception as err:
        print(f"[ERROR] {err}", flush=True)

    return res_ner, res_sen
