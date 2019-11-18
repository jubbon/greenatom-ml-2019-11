#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import streamlit as st

from smart_hr.data import load_data as load
from smart_hr.data.dismissal import load as load_dismissal


@st.cache
def load_data(data_dir):
    '''
    '''
    excel_filename = os.path.join(data_dir, "hr.xls")
    load(excel_filename)

    dismissal_filename = os.path.join(data_dir, "dismissal.csv")
    feature_importance_filename = os.path.join(data_dir, "feature_importance.csv")
    load_dismissal(dismissal_filename, feature_importance_filename)
