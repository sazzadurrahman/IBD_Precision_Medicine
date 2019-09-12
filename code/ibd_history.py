# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 10:54:38 2019

@author: srahman
"""

import dash
import pandas as pd

##from app import app

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

ibd_csv="J:/Experimental data/2.0 CURRENT STUDIES/CCR001/Data uploaded to AnalytixAgility/ibd_donors_history.csv"
#ibd_csv="C:/Reprocell/data/ibd_donors_history.csv"
#ibd_csv=r'C:\Reprocell\ibd_donors_history.csv'
ibd_df = pd.read_csv(ibd_csv)
ibd_df['Ethnicity']=ibd_df['Ethnicity'].str.capitalize()
ibd_df['Disease'] = ibd_df['Tissue_Type'].str.split().str[0]
ibd_df=ibd_df.dropna(axis='columns')
col_options = [dict(label=x, value=x) for x in ibd_df.columns]
dimensions = ["x", "y", "color", "graph column","graph row"]

