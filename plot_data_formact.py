# author: magmar68


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

df = pd. #insert your merge input file

provincia = 'Teramo'

df = df[['data','denominazione_regione','denominazione_provincia','totale_casi']]
df['data'] = pd.to_datetime(df['data']).dt.date
df = df.drop(df[df['denominazione_provincia'] != provincia].index)
df

#plot

fig, ax = plt.subplots(1) #plot only a pair of columns
ax.plot(df['data'],df['totale_casi']) #choose wich columns

fig.autofmt_xdate()

ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')





