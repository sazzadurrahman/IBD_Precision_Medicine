# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:24:08 2019

@author: srahman
"""
import allel
import csv
import pandas as pd
from functools import reduce
import os
import sys
import numpy as np
import scipy
import dash
import pandas as pd
import numpy as np
import dash_html_components as html
import ibd_history as ibd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', -1)

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)


#Read all VCF files from source, and read each file as dataframe
import glob
vcf_path="J:/Experimental data/2.0 CURRENT STUDIES/CCR001/Data uploaded to AnalytixAgility/IBD Donors whole exome vcfs/"
#vcf_path="C:/Reprocell/IBD Donors whole exome vcfs/"
filenames=glob.glob(vcf_path+'*.vcf.gz')

#TNF IBD
tnf_csv1="J:/Experimental data/2.0 CURRENT STUDIES/CCR001/Data uploaded to AnalytixAgility/TNFa levels pgml_IBD_25 donors.csv"
#tnf_csv1="C:/Reprocell/data/TNFa levels pgml_IBD_25 donors.csv"
tnf_df = pd.read_csv(tnf_csv1)
tnf_df.columns = tnf_df.columns.str.strip().str.replace(' ', '_')

#Get from 4th columns to exclude Media only columns
donor_slice = np.r_[0, 3:17]
#Inlcude Donor_ID column 
tnf_dfs=tnf_df.iloc[:,donor_slice]

#Calculate mean between 2s' columns
s1=tnf_dfs[['SEB', 'SEB.1']].mean(axis=1)
s2=tnf_dfs[['SEB_5ASA', 'SEB_5ASA.1']].mean(axis=1)
s3=tnf_dfs[['SEB_DMSO', 'SEB_DMSO.1']].mean(axis=1)
s4=tnf_dfs[['SEB_Pred_1uM','SEB_Pred_1uM.1']].mean(axis=1)
s5=tnf_dfs[['SEB_Pred_100nM','SEB_Pred_100nM.1']].mean(axis=1)
s6=tnf_dfs[['SEB_BIRB796_100nM', 'SEB_BIRB796_100nM.1']].mean(axis=1)
s7=tnf_dfs[['SEB_BIRB796_10nM', 'SEB_BIRB796_10nM.1']].mean(axis=1)

tnf_dfs_mean = tnf_dfs[['Donor_ID']].assign(SEB_mean=s1, SEB5ASA_mean=s2, SEBDMSO_mean=s3, SEBPred1uM_mean=s4,SEBPred100nM_mean=s5, SEBBirb796100nM=s6, SEBBirb79610nM=s7)


#col_options = [dict(label=x, value=x) for x in tnf_dfs_mean.columns]


dimensions = ["X", "Y", "Colour"]



#Compare each mean column against the control column
t1=tnf_dfs_mean['SEB5ASA_mean']/tnf_dfs_mean['SEB_mean']*100
t2=tnf_dfs_mean['SEBPred1uM_mean']/tnf_dfs_mean['SEBDMSO_mean']*100
t3=tnf_dfs_mean['SEBPred100nM_mean']/tnf_dfs_mean['SEBDMSO_mean']*100
t4=tnf_dfs_mean['SEBBirb796100nM']/tnf_dfs_mean['SEBDMSO_mean']*100
t5=tnf_dfs_mean['SEBBirb79610nM']/tnf_dfs_mean['SEBDMSO_mean']*100
tnf_mean_compare = round(tnf_dfs_mean[['Donor_ID']].assign(SEB5ASA_SEB=t1, SEBPred1uM_SEBDMSO=t2, SEBPred100nM_SEBDMSO=t3, SEBBirb796100nM_SEBDMSO=t4,SEBBirb79610nM_SEBDMSO=t5),3)

#Set index to apply substraction on the whole datafraame 
tnf_mean_compare_i=tnf_mean_compare.set_index('Donor_ID')

#Difference from 100
tnf_mean_compare_i_r=tnf_mean_compare_i.sub(100)

#Reset index
tnf_mean_compare_i_r.reset_index(level =['Donor_ID'], inplace = True) 
col_options = [dict(label=x, value=x) for x in tnf_mean_compare_i_r.columns]

#col_options_cat = [dict("name"=x, "id"=x) for x in tnf_mean_compare_i_r.columns[1:]]
col_options_cat = [{"label":x, "value":x} for x in tnf_mean_compare_i_r.columns[1:]]

#format_mapping={'SEB5ASA_SEB': '{:,.3f}', 'SEBPred1uM_SEBDMSO': '{:,.3f}', 'SEBPred100nM_SEBDMSO': '{:.3f}','SEBBirb796100nM_SEBDMSO': '{:.3f}','SEBBirb79610nM_SEBDMSO': '{:.3f}'}
#for key, value in format_mapping.items():
 #   tnf_mean_compare_i_r[key] = tnf_mean_compare_i_r[key].apply(value.format)

tnf_i=tnf_mean_compare_i_r
tnf_ir=tnf_mean_compare_i_r

#Merge TNF control and TNF compared data
#1. Get the two control vaaiables and Donor_ID
tnf_control=tnf_dfs_mean[['Donor_ID','SEB_mean','SEBDMSO_mean']]
#2 Merge tnf_control and tnf_mean_compare_i_r 
tnf_compare=tnf_mean_compare_i_r.merge(tnf_control, left_on='Donor_ID', right_on='Donor_ID', how='outer')

#Format tnf_mean_compare_i_r data frame columns for data dictionary


#combine IBD history and TNF mean compare data set , tnf_mean_compare_i_r
tnf_ibd=tnf_mean_compare_i_r.merge(ibd.ibd_df, left_on='Donor_ID', right_on='Donor_ID', how='outer')
tnf_ibd_col_options = [dict(label=x, value=x) for x in tnf_ibd.columns]

def get_drugs(drug):
    #dr=tnf_mean_compare_i_r[tnf_mean_compare_i_r[drug]<0][['Donor_ID',drug]]
    dr=tnf_mean_compare_i_r[tnf_mean_compare_i_r[drug]][['Donor_ID',drug]]
    #dr[[drug]]=abs(dr[[drug]]) #Get absolute value of the selected column
    dr[[drug]]=dr[[drug]]
    dr_abs=dr[['Donor_ID',drug]]  
    cr=dr_abs.columns[1]+'_range'
    dr_abs[cr]=pd.cut(x=dr_abs[dr_abs.columns[1]], bins=range(0,100+25,25), right=False)
    rt=dr_abs[[dr_abs.columns[2],dr_abs.columns[1],dr_abs.columns[0]]]
    return rt

def generate_table(dataframe, max_rows=10):
    
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    ) 

#Create Bin range and labels and return data
def get_data(binr):
    binrange=[]
    bincount=int(100/binr)
    binvalue=0
    for x in range(0,bincount+1):
        binrange.insert(x,binvalue)
        binvalue=binvalue+binr
    
    binlabel=[]
    start=0
    end=binr
    for i in range(bincount):
        r=str(start)+'-'+str(end)
        binlabel.insert(i, r)
        start=start+binr
        end=end+binr    

#Create dataframes based on variables/columns 
    cols=tnf_i.columns[1:]
    range_df=[]
    for c in cols:
        dr=tnf_i[tnf_i[c] <0][['Donor_ID',c]]
        dr[[c]]=abs(dr[[c]]) #Get absolute value of the selected column
        dr_abs=dr[['Donor_ID',c]] 
        cr=c[0:c.index('_')]+'_Range'
        dr_abs[cr]=pd.cut(x=dr_abs[dr_abs.columns[1]], bins=binrange, labels=binlabel, right=False)
        rt=dr_abs[['Donor_ID',cr,c]]
        range_df.append(rt)
    range_dfs=reduce(my_merge, range_df)
    return range_dfs

def my_merge(df1, df2):
    return pd.merge(df1, df2, left_on='Donor_ID', right_on='Donor_ID',how='outer')

range_dfs=get_data(25)
#range_dfs=reduce(my_merge, range_df)

format_mapping={'SEB5ASA_SEB': '{:,.3f}', 'SEBPred1uM_SEBDMSO': '{:,.3f}', 'SEBPred100nM_SEBDMSO': '{:.3f}','SEBBirb796100nM_SEBDMSO': '{:.3f}','SEBBirb79610nM_SEBDMSO': '{:.3f}'}
for key, value in format_mapping.items():
    range_dfs[key] = range_dfs[key].apply(value.format)
    tnf_ir[key] = tnf_ir[key].apply(value.format)

