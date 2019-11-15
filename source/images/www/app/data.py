#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import streamlit as st

from smart_hr.data import load_data as load


@st.cache
def load_data(data_dir):
    '''
    '''
    excel_filename = os.path.join(data_dir, "hr.xls")
    load(excel_filename)