#!/usr/bin/env python
# -*- coding: utf-8 -*-


def color_positive(value, color="red", default="black"):
    '''
    '''
    return f"color: {color if value > 0 else default}"


def color_negative(value, color="red", default="black"):
    '''
    '''
    return f"color: {color if value < 0 else default}"


def color_zero(value, color="red", default="black"):
    '''
    '''
    return f"color: {color if value == 0 else default}"


def highlight_more(value, threshold=0, color="yellow"):
    '''
    '''
    return f"background-color: {color}" if value > threshold else ''


def highlight_less(value, threshold=0, color="yellow"):
    '''
    '''
    return f"background-color: {color}" if value < threshold else ''
