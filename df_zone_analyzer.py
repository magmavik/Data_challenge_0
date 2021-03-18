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

regioni = df['denominazione_regione'].tolist()
regioni = list(dict.fromkeys(regioni))
regione = regioni[1]

df = df[df['data'] > pd.to_datetime('2020-12-15').date() ]

date = df['data'].tolist() #date list
date = list(dict.fromkeys(date))


val = df.loc[df['denominazione_regione'].str.contains(regione, flags = re.I, regex = True)]['totale_casi'].tolist()   #positive list

for i in range(1, len(val))[::-1]:
    val[i] -= val[i-1]
for i in range(1, len(val)-2, 3):
    trio = np.array([val[i], val[i+1], val[i+2]])
    m = np.mean(trio)
    val[i] = m
    val[i+1] = m
    val[i+2] = m
    
date.pop(0) #removing first problematic value
val.pop(0)
regione_plot = plt.bar(date, val)

for i in range(1, len(val)):
    control = df.loc[df['denominazione_regione'].str.contains(regione, flags = re.I, regex = True)]['colore'].tolist()[i]
    if control == "giallo":
        regione_plot[i].set_facecolor('yellow')
    elif control == "arancione":
        regione_plot[i].set_facecolor('orange')
    elif control == "rosso":
        regione_plot[i].set_facecolor('red')

# print(province)

plt.gcf().autofmt_xdate()

date_format = mpl_dates.DateFormatter('%d %b %Y')

plt.gca().xaxis.set_major_formatter(date_format)

plt.xlabel('Data')
plt.ylabel('Casi giornalieri')

plt.legend()

plt.title(df.loc[df['denominazione_regione'].str.contains(regione, flags = re.I, regex = True)]['denominazione_regione'].tolist()[0])

plt.show()
