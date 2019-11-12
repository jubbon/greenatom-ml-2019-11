#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click


@click.command()
def train():
    ''' Train model
    '''
    print("Training model", flush=True)
