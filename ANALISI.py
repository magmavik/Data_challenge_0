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
import matplotlib
from scipy.signal import argrelextrema

def odd( num): # semplice funzione che verifica se il numero è pari
    if num % 2 == 0: return False
    else: return True

def mean_over_list_range( l, a, b): # fa la media degli elementi nella lista dall'indice a all'indice b
    if(a > b or a > len(l) -1 ):
        return 0
    sum = 0
    for x in range(a,b):
        if( x == len(l ) - 1):
            return sum/(x -a)
        sum += l[x-1]
    return sum/(b-a)

def adjust_series( in_list , step ): # ogni elemento della serie è la media mobile sui 7 giorni
    j = in_list.copy()
    if(odd(step) and step > 0 and step < len(in_list)): # notare che perdiamo i primi 3 e gli ultimi 3 della serie
        d = (step - 1)/2
        for x in range(int(d), len(in_list) - int(d)):
            j[x] =  mean_over_list_range(in_list, int(x-d), int(x+d))
    #else #per completezza sarebbe da fare, ma lo sbatti è poco
        #d =  
    return j

################################
#   lettura e pulitura dati    #
################################


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams.update({'font.size': 18})

df = pd.read_csv('output.csv')
df['data'] = pd.to_datetime(df['data']).dt.date
start_time =  pd.to_datetime('2021-01-05').date()

regioni = df['denominazione_regione'].tolist()
regioni = list(dict.fromkeys(regioni))

df = df[df['data'] > start_time ]  #restrain period

date = df['data'].tolist() #date list
date = list(dict.fromkeys(date))

data_regioni = dict()
passings = dict() #passings from yellow to orange/red
peaks = dict()  # dictionary of peaks for each region
dist = dict()

for reg in regioni:
    
    # +++++ CREATING CORRECT REGION DATAFRAME +++++
    
    val = df.loc[df['denominazione_regione'].str.contains(str(reg), flags = re.I, regex = True)]['totale_casi'].tolist()
    col = df.loc[df['denominazione_regione'].str.contains(str(reg), flags = re.I, regex = True)]['colore'].tolist()

    for i in range(1, len(val))[::-1]: # convert cumulative cases in daily cases
        val[i] -= val[i-1]

    norm = adjust_series(val, 7)

    # creating a data frame for each region with
    df_merge = pd.DataFrame (list(zip(date, val, norm, col)), columns=['date','dati_giornalieri', 'dati_giornalieri_mediati', 'colore'])
    # removing first 5 rows (3 not normalized, 1 bad peak... why 5 and not 4? fucking domanda) and last 3 (not normalized)
    df_merge = df_merge.iloc[5:]
    df_merge = df_merge.iloc[:-3]
    data_regioni[reg] = df_merge



    # +++++ ANALYZING DATA +++++

    passings[reg] = []
    peaks[reg] = []
    dist[reg] = []

    # searching peaks in normalized data
    n = 15
    peaks[reg] = argrelextrema(df_merge['dati_giornalieri_mediati'].values, np.greater_equal, order=n)[0].tolist()

    # searching passings giallo-arancione or giallo-rosso
    for i in range(0, len(df_merge['colore'].tolist())):
        if (col[i] == 'giallo') & ((col[i+1] == 'arancione') | (col[i+1] == 'rosso')):
            passings[reg].append(i) #last yellow index

    # calculating distance with proper bounds
    print(passings[reg])
    for passing in passings[reg]:
        print(passing)
        for i in range(passing-15, passing):
            if (i < 0) | (i > len(col)) : exit
            elif col[i] != "giallo":
                passings[reg].remove(passing)
                exit

    for passing in passings[reg]:
        for i in range(passing, passing + 20):
            if (i < 0) | (i > len(col)): exit
            elif col[i] == "giallo":
                passings[reg].remove(passing)
                exit
    print(passings[reg])







# +++++ PLOTTING +++++

for i in range(1, len(sys.argv)):
    regione = sys.argv[i]

    dati = data_regioni[regione]
    x1 = dati['date'].tolist()
    y1 = dati['dati_giornalieri'].tolist()
    col1 = dati['colore'].tolist()

    fig, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
    ax1.set_title('a')
    ax2.set_title('b')
    ax1 = ax1.bar(x1, y1)
    for i in range(0, len(x1)):
        if col1[i] == 'giallo':
            ax1[i].set_facecolor('#fff000')
        if col1[i] == 'arancione':
            ax1[i].set_facecolor('orange')
        if col1[i] == 'rosso':
            ax1[i].set_facecolor('red')
        if i+1 in peaks[regione]:
            ax1[i].set_hatch('////')

    x2 = dati['date'].tolist()
    y2 = dati['dati_giornalieri_mediati'].tolist()
    col2 = dati['colore'].tolist()


    ax2 = ax2.bar(x2, y2)

    for i in range(0, len(x2)):
        if col1[i] == 'giallo':
            ax2[i].set_facecolor('#fff000')
        if col1[i] == 'arancione':
            ax2[i].set_facecolor('orange')
        if col1[i] == 'rosso':
            ax2[i].set_facecolor('red')
        if i+1 in peaks[regione]:
            ax2[i].set_hatch('////')

    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 22,
        }
    font1 = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 40,
        }
    plt.gcf().autofmt_xdate()

    date_format = mpl_dates.DateFormatter('%d %b %Y')

    plt.gca().xaxis.set_major_formatter(date_format)



    plt.xlabel('Data', fontdict=font)
    fig.text(0.02, 0.5, 'Casi giornalieri', va='center', rotation='vertical', fontdict=font)

plt.show()
   
