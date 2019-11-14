#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import faust

app = faust.App(
    "SmartHR",
    broker=os.getenv("BROKER_URL", "kafka://localhost"),
)
