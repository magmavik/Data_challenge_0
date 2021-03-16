import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt

df = pd.read_csv('output.csv')

province = dict()
province['milano'] = []
province['campobasso'] = []
province['alessandria'] = []
# campobasso = []
# milano = []
date = []

# campobasso = df.loc[df['denominazione_provincia'].str.contains('campobasso', flags = re.I, regex = True)]['totale_casi'].tolist()
date = df.loc[df['denominazione_provincia'].str.contains('campobasso', flags = re.I, regex = True)]['data'].tolist()

for key in province:
    key = df.loc[df['denominazione_provincia'].str.contains(key, flags = re.I, regex = True)]['totale_casi'].tolist()
    for i in range(1, len(key))[::-1]:
        key[i] -= key[i-1]
    plt.plot(date, key)


plt.show()