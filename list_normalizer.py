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
from matplotlib.pyplot import figure
figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

def odd( num): # semplice funzione che verifica se il numero è pari
    if num % 2 == 0: return False
    else: return True

def mean_over_list_range( l, a, b): # fa la media degli elementi nella lista dall'indice a all'indice b
    if(a > b or a > len(l) -1 ):
        return 0
    sum = 0
    for x in range(a,b):
        if( x == len(l ) - 2):
            return sum/(x -a)
        sum += l[x-1]
    return sum/(b-a)

def adjust_series( in_list , step ): # ogni elemento della serie è la media mobile sui 7 giorni
    j = in_list.copy()
    if(odd(step) and step > 0 and step < len(in_list)): # notare che perdiamo i primi 3 e gli ultimi 3 della serie
        d = (step - 1)/2
        print(d)
        for x in range(int(d), len(in_list) - int(d)-1):
            j[x] =  mean_over_list_range(in_list, int(x-d), int(x+d))
    #else #per completezza sarebbe da fare, ma lo sbatti è poco
        #d =  
    return j


################################
#   lettura e pulitura dati    #
################################

df = pd.read_csv('output.csv')
df['data'] = pd.to_datetime(df['data']).dt.date # rimozione dell'ora dalla data

regioni = df['denominazione_regione'].tolist()
regioni = list(dict.fromkeys(regioni))
regione = 'Lombardia' #seleziode della regione interessata 

df = df[df['data'] > pd.to_datetime('2021-01-01').date()] # rimozione dei dati più vecchi di ..



date = df['data'].tolist() #date list
date = list(dict.fromkeys(date)) # rimozione duplicati

# lista dei valori comulativi dei casi
val = df.loc[df['denominazione_regione'].str.contains(regione, flags = re.I, regex = True)]['totale_casi'].tolist()   #positive list

################################
#         analisi dati         #
################################


for i in range(1, len(val))[::-1]: #conversione da cumulativi a giornalieri
    val[i] -= val[i-1]
    
    
date.pop(0) #removing first problematic value
val.pop(0)

# normalizziamo i dati sull'andamento ciclico settimanale 
s_dec = adjust_series(val,7)  
regione_plot_norm = plt.bar(date, s_dec )

# set dei colori 
for i in range(1, len(s_dec)):
    control = df.loc[df['denominazione_regione'].str.contains(regione, flags = re.I, regex = True)]['colore'].tolist()[i]
    if control == "giallo":
        regione_plot_norm[i].set_facecolor('yellow')
    elif control == "arancione":
        regione_plot_norm[i].set_facecolor('orange')
    elif control == "rosso":
        regione_plot_norm[i].set_facecolor('red')

################################
#             plot             #
################################

plt.gcf().autofmt_xdate()
date_format = mpl_dates.DateFormatter('%d %b %Y')
plt.gca().xaxis.set_major_formatter(date_format)
plt.xlabel('Data')
plt.ylabel('Casi giornalieri')
plt.title(df.loc[df['denominazione_regione'].str.contains(regione, flags = re.I, regex = True)]['denominazione_regione'].tolist()[0])
plt.show() #notare che i primi 3 e gli ultimi 3 non sono normalizzati

