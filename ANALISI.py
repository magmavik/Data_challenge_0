#   Program for analizing COVID-19 dataframes from github.
#
#   Dev:    Luca Malucelli, Lorenzo Magnoni
#   Ctc:    luca.malucelli@studenti.unimi.it



import sys

import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from scipy.signal import argrelextrema


def ind_max ( l ,  a  ,  b):
    if ( a > b ):
        return 0
    m = a
    for x in range(a , b):
        if ( l[m] <= l[x] ):
            m = x
        if (x == len(l)-1): break
    return m 
            

df = pd.read_csv('output.csv')
df['data'] = pd.to_datetime(df['data']).dt.date
start_time =  pd.to_datetime('2021-1-8').date()

regioni = df['denominazione_regione'].tolist()
regioni = list(dict.fromkeys(regioni))

df = df[df['data'] > start_time ]  #restrain period 

date = df['data'].tolist() #date list
date = list(dict.fromkeys(date))

data_regioni = dict()
passings = dict() #passings from yellow to orange/red
peaks = dict()  # dictionary of peaks for each region
delta_time = dict()

for reg in regioni:
    val = df.loc[df['denominazione_regione'].str.contains(str(reg), flags = re.I, regex = True)]['totale_casi'].tolist()
    col = df.loc[df['denominazione_regione'].str.contains(str(reg), flags = re.I, regex = True)]['colore'].tolist()

    for i in range(1, len(val))[::-1]: # convert cumulative cases in daily cases
        val[i] -= val[i-1]

    for i in range(1, len(val)-2, 3): #mean over three days for reducing fluctuantion 
        trio = np.array([val[i], val[i+1], val[i+2]])
        m = np.mean(trio)
        val[i] = m
        val[i+1] = m
        val[i+2] = m
    
    #creating a data frame for each region with
    df_merge = pd.DataFrame (list(zip(date, val,col)), columns=['date','dati_giornalieri','colore']) 
    data_regioni[reg] = df_merge
    
    passings[reg] = []
    peaks[reg] = []
    delta_time[reg] = []
    
    
    for i in range(0, len(val)-1):
        if (col[i] == 'giallo') & ((col[i+1] == 'arancione') | (col[i+1] == 'rosso')):
            passings[reg].append(i) #date of switching colour
    
    cont = 0
    for pas in passings[reg]:
        for i in range(0, len(val) - 1):
            if i == pas: 
                peaks[reg].append(date[ind_max(val, pas, pas + 15)])
                #print('data switch: ', date[pas], ' data picco: ', peaks[reg][0]  )
                delta_time[reg].append( peaks[reg][cont] - date[pas] )
                cont += 1
    
print( peaks)
print( delta_time)      
                
                
            
