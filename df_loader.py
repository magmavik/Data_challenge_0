#   Program for loading COVID-19 dataframes from github.
#
#   Dev:    Luca Malucelli
#   Ctc:    luca.malucelli@studenti.unimi.it


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import glob
from datetime import date, timedelta

sdate = date(2020,2,24) #start date
edate = date.today() + timedelta(days=1) #end date
# edate = date(2020,2, 27)

path = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-'

datelist = []
for time in pd.date_range(sdate, edate-timedelta(days = 1), freq = 'd'):
    datelist.append(time.strftime("%Y%m%d"))

data_frames = []

for i in datelist:
    filename = path + i + '.csv'
    df = pd.read_csv(filename)
    data_frames.append(df)

#frame = pd.concat(li, axis = 0, ignore_index = True)