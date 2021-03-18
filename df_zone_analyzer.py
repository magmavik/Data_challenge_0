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

# regioni = dict()
date = []

# for arg in sys.argv[1:]:
#     regioni[str(arg)] = []     #creating a dictionary with the arguments passed as keys

regione = sys.argv[1]


date = df.loc[df['denominazione_regione'].str.contains(regione, flags = re.I, regex = True)]['data'].tolist()    #date list

val = df.loc[df['denominazione_regione'].str.contains(regione, flags = re.I, regex = True)]['totale_casi'].tolist()   #positive list
for i in range(1, len(val))[::-1]:
    val[i] -= val[i-1]
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