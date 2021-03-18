#   Program for loading COVID-19 dataframes from github.
#
#   Dev:    Luca Malucelli, Lorenzo Magnoni
#   Ctc:    luca.malucelli@studenti.unimi.it


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import glob
from datetime import date, timedelta

sdate = date(2020,2,24) #start date
edate = date.today() - timedelta(days=1) #end date
# edate = date(2020,2, 27)

path = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-'

datelist = []
for time in pd.date_range(sdate, edate, freq = 'd'):
    datelist.append(time.strftime("%Y%m%d"))

data_frames = []

for i in datelist:
    filename = path + i + '.csv'
    df = pd.read_csv(filename)
    data_frames.append(df)

frame = pd.concat(data_frames, axis = 0, ignore_index = True)

frame.sort_values(['data', 'denominazione_regione'], ascending = True)
#frame = frame.drop(columns=['codice_provincia', 'lat', 'long', 'note'])
frame['data'] = pd.to_datetime(frame['data']).dt.date
# frame['colore_zona'] = ''

df = pd.read_csv('https://raw.githubusercontent.com/imcatta/restrizioni_regionali_covid/main/dataset.csv')
df['data'] = pd.to_datetime(df['data']).dt.date
df.loc[df['denominazione_regione'] == 'Provincia autonoma Bolzano', 'denominazione_regione'] = 'P.A. Bolzano'
df.loc[df['denominazione_regione'] == 'Provincia autonoma Trento', 'denominazione_regione'] = 'P.A. Trento'

# for regione in frame:
#     for colore in df:
#         if (regione['data'] == colore['data'] & regione['denominazione_regione'] == colore['denominazione_regione']):
#             regione['colore_zona'] = colore['colore'] 


# frame.loc[(frame['data'] == ) & (), ]

frame = pd.merge(frame, df, how="left", on=["data", "denominazione_regione"])

frame.to_csv('output.csv')