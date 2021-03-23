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


giorni_gialli = 10
giorni_aranc = 15
regione = 'Liguria' #seleziode della regione interessata





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
        for x in range(int(d), len(in_list) - int(d)):
            j[x] =  mean_over_list_range(in_list, int(x-d), int(x+d))
    #else #per completezza sarebbe da fare, ma lo sbatti è poco
        #d =  
    return j

def verify_conditions( col , i):
    if ((i - giorni_gialli < 0) or (i + giorni_aranc > len(col) -1)) : return False
    
    else:
        for x in range( i - giorni_gialli, i + giorni_aranc ):
            if ( x <= i ): 
                if (col[x] != 'giallo') :return False
            else:
                if( col[x] == ' giallo') : return False
            
    return True
    
def max_in_range( val , a, b):
    ind_max = a
    if ( a > b or b > len(val) ) :
        print( 'ERROR: wrong input in __function__ ') # non ho idea se funzioni il __function__
        return 0
    
    else:
        max = val[a]
        for x in range(a,b):
            
            if( max <= val[x]):
                
                ind_max = x
                max = val[x]
    
    return ind_max
    
    
    
    
################################
#   lettura e pulitura dati    #
################################

df = pd.read_csv('output.csv')
df['data'] = pd.to_datetime(df['data']).dt.date # rimozione dell'ora dalla data

regioni = df['denominazione_regione'].tolist()
regioni = list(dict.fromkeys(regioni))
 

df = df[df['data'] > pd.to_datetime('2021-01-01').date()] # rimozione dei dati più vecchi di ..



date = df['data'].tolist() #date list
date = list(dict.fromkeys(date)) # rimozione duplicati

# lista dei valori comulativi dei casi
val = df.loc[df['denominazione_regione'].str.contains(regione, flags = re.I, regex = True)]['totale_casi'].tolist()   #positive list
col = df.loc[df['denominazione_regione'].str.contains(regione, flags = re.I, regex = True)]['colore'].tolist()

################################
#         analisi dati         #
################################


for i in range(1, len(val))[::-1]: #conversione da cumulativi a giornalieri
    val[i] -= val[i-1]
    
    
date.pop(0) #removing first problematic value
val.pop(0)
col.pop(0)


picchi = list()
# normalizziamo i dati sull'andamento ciclico settimanale 
s_dec = adjust_series(val,7)  
regione_plot_norm = plt.bar(date, s_dec)

# set dei colori 
for i in range(1, len(s_dec)):
    
    if col[i] == "giallo":
        regione_plot_norm[i].set_facecolor('yellow')
    elif col[i] == "arancione":
        regione_plot_norm[i].set_facecolor('orange')
    elif col[i] == "rosso":
        regione_plot_norm[i].set_facecolor('red')
    #ricerca picchi
    if col[i] == "giallo" and col[i + 1] == "arancione":
        if verify_conditions(col , i) :
            picchi.append( max_in_range( s_dec , i , i + 15))
            regione_plot_norm[max_in_range( s_dec , i , i + 15) ].set_hatch('////')
        
        
print(picchi)
print(len(val))
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


