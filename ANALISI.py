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

df = pd.read_csv('output.csv')
df['data'] = pd.to_datetime(df['data']).dt.date
start_time =  pd.to_datetime('2020-12-13').date()

regioni = df['denominazione_regione'].tolist()
regioni = list(dict.fromkeys(regioni))

df = df[df['data'] > start_time ]  #restrain period 

date = df['data'].tolist() #date list
date = list(dict.fromkeys(date))

data_regioni = dict()
passings = dict() #passings from yellow to orange/red
peaks = dict()  # dictionary of peaks for each region

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

    passings[reg] = []
    peaks[reg] = []
    for i in range(0, len(val)-1):
        if (col[i] == 'giallo') & ((col[i+1] == 'arancione') | (col[i+1] == 'rosso')):
            passings[reg].append(i) #date of switching colour
    
    #creating a data frame for each region with
    df_merge = pd.DataFrame (list(zip(date, val,col)), columns=['date','dati_giornalieri','colore']) 
    data_regioni[reg] = df_merge

    n = 5 # io non capire
    # peaks[reg] = df_merge.loc[argrelextrema(df_merge['dati_giornalieri'].values, np.greater_equal, order=n)[0]].index.tolist[]
    # print(df_merge['max'].tolist())
    peaks[reg] = argrelextrema(df_merge['dati_giornalieri'].values, np.greater_equal, order=n)[0].tolist()

cazzo = data_regioni['Lombardia']
cazzo = cazzo['dati_giornalieri'].tolist()
date.pop(0) #removing first problematic value
cazzo.pop(0)
regione_plot = plt.bar(date, cazzo)

for i in range(0, len(cazzo)):
    if i+1 in peaks['Lombardia']:
        regione_plot[i].set_facecolor('red')

plt.gcf().autofmt_xdate()

date_format = mpl_dates.DateFormatter('%d %b %Y')

plt.gca().xaxis.set_major_formatter(date_format)

plt.xlabel('Data')
plt.ylabel('Casi giornalieri')

plt.title('Lombardia')

plt.show()
# prova = data_regioni['Lombardia']
# prova = prova['dati_giornalieri'].tolist()
# date.pop(0) #removing first problematic value
# cazzo.pop(0)
# regione_plot = plt.bar(date, prova)

# plt.gcf().autofmt_xdate()

# date_format = mpl_dates.DateFormatter('%d %b %Y')

# plt.gca().xaxis.set_major_formatter(date_format)

# plt.xlabel('Data')
# plt.ylabel('Casi giornalieri')

# plt.title('Lombardia')

# plt.show()
