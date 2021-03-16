import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates

df = pd.read_csv('output.csv')
df['data'] = pd.to_datetime(df['data']).dt.date

province = dict()
province['milano'] = []
province['campobasso'] = []
province['alessandria'] = []
province['pavia'] = []
# campobasso = []
# milano = []
date = []

# campobasso = df.loc[df['denominazione_provincia'].str.contains('campobasso', flags = re.I, regex = True)]['totale_casi'].tolist()
date = df.loc[df['denominazione_provincia'].str.contains('campobasso', flags = re.I, regex = True)]['data'].tolist()

for key, val in province.items():
    val = df.loc[df['denominazione_provincia'].str.contains(key, flags = re.I, regex = True)]['totale_casi'].tolist()
    for i in range(1, len(val))[::-1]:
        val[i] -= val[i-1]
    province[key] = val
    plt.plot(date, val, label=key)

print(province)
plt.gcf().autofmt_xdate()

date_format = mpl_dates.DateFormatter('%d %b %Y')

plt.gca().xaxis.set_major_formatter(date_format)

plt.xlabel('Data')
plt.ylabel('Casi giornalieri')

plt.legend()

plt.show()