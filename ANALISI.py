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

df = pd.read_csv('output.csv')
df['data'] = pd.to_datetime(df['data']).dt.date
start_time =  pd.to_datetime('2020-12-13').date()

regioni = df['denominazione_regione'].tolist()
regioni = list(dict.fromkeys(regioni))
regione = regioni[1]

df = df[df['data'] > start_time ]

date = df['data'].tolist() #date list
date = list(dict.fromkeys(date))

data_regioni = dict()

passings = dict() #passings from yellow to orange/red

for reg in regioni:
    val = df.loc[df['denominazione_regione'].str.contains(str(reg), flags = re.I, regex = True)]['totale_casi'].tolist()
    col = df.loc[df['denominazione_regione'].str.contains(str(reg), flags = re.I, regex = True)]['colore'].tolist()

    for i in range(1, len(val))[::-1]:
        val[i] -= val[i-1]
    for i in range(1, len(val)-2, 3):
        trio = np.array([val[i], val[i+1], val[i+2]])
        m = np.mean(trio)
        val[i] = m
        val[i+1] = m
        val[i+2] = m

    
    df_merge = pd.DataFrame (list(zip(date, val,col)) ,columns=['date','dati_gionalieri','colore'])
    data_regioni[reg] = df_merge

    #passings[reg] = []
    for i in range(0, len(val)-1):
        if (col[i] == 'giallo') & ((col[i+1] == 'arancione') | (col[i+1] == 'rosso')):
            passings[reg].append(i)

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
