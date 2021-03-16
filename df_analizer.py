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

province = dict()
date = []

for arg in sys.argv[1:]:
    province[str(arg)] = []     #creating a dictionary with the arguments passed as keys


date = df.loc[df['denominazione_provincia'].str.contains('campobasso', flags = re.I, regex = True)]['data'].tolist()    #date list

for key, val in province.items():
    val = df.loc[df['denominazione_provincia'].str.contains(key, flags = re.I, regex = True)]['totale_casi'].tolist()   #positive list
    for i in range(1, len(val))[::-1]:
        val[i] -= val[i-1]
    province[key] = val
    plt.plot(date, val, label=df.loc[df['denominazione_provincia'].str.contains(key, flags = re.I, regex = True)]['denominazione_provincia'].tolist()[0])

# print(province)
plt.gcf().autofmt_xdate()

date_format = mpl_dates.DateFormatter('%d %b %Y')

plt.gca().xaxis.set_major_formatter(date_format)

plt.xlabel('Data')
plt.ylabel('Casi giornalieri')

plt.legend()

plt.show()