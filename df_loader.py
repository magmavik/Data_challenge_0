#   Program for loading COVID-19 dataframes from github.
#
#   Dev:    Luca Malucelli  Lorenzo Magnoni
#   Ctc:    luca.malucelli@studenti.unimi.it


import numpy as np
import pandas as pd
import os.path


import glob
from datetime import date, timedelta

# path to "protezione civile italiana" github repository
path = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-'
dropped_columns = ['codice_provincia', 'lat', 'long', 'note']
file_OUT = 'merge.csv'
COLOR = True


sdate = date(2020,2,24) #start date
edate = date.today() - timedelta(days=1) #end date

#======================================================================================

#================function==============================================================
def create_date_list( _sdate, _edate):
    _list = []
    if (_sdate > _edate):
        print('ERROR: unexpected input in __function__')
        return 
    # create a list of date from start date to end date
    for time in pd.date_range(sdate, edate, freq = 'd'):
        _list.append(time.strftime("%Y%m%d"))
    return _list

def create_merge_data_frame(_datelist):
    _data_frames = []
    for i in datelist:
        filename = path + i + '.csv'
        df = pd.read_csv(filename)
        _data_frames.append(df)
    return _data_frames

def merge_data_frame(_data_frames, _datelist):
    for i in _datelist:
        filename = path + i + '.csv'
        df = pd.read_csv(filename)
        _data_frames.append(df)
    return _data_frames

#=====================================================================================
datelist = []
df = []

new_file = True

if(os.path.exists(file_OUT)):
    df = pd.read_csv(file_OUT)
    print( ' updating file ', file_OUT,' ....')
    sdate = pd.to_datetime( df['data'].max())
    print(type(sdate))
    print(type(edate))
    if sdate == edate:
        print('file', file_OUT,'already updated')
        new_file = False
    else: 
        datelist = create_date_list(sdate,edate)
        df = merge_data_frame(df, datelist)
        print( file, ' file_OUT ' , 'updated')
else:
    print(' file', file_OUT,'doesn\'t already exist. Creating one.... it will take a while')
    datelist = create_date_list(sdate,edate)
    df = create_merge_data_frame(datelist)
    print(df)

#=====================================================================================

if new_file:
    frame = df
    frame['data'] = pd.to_datetime(frame['data']).dt.date
    frame.sort_values(['data', 'denominazione_regione', 'denominazione_provincia'], ascending = True)
    frame = frame.drop(columns = dropped_columns)

    if COLOR:
        color_frame = pd.read_csv('https://raw.githubusercontent.com/imcatta/restrizioni_regionali_covid/main/dataset.csv')
        color_frame['data'] = pd.to_datetime(df['data']).dt.date
        color_frame.loc[df['denominazione_regione'] == 'Provincia autonoma Bolzano', 'denominazione_regione'] = 'P.A. Bolzano'
        color_frame.loc[df['denominazione_regione'] == 'Provincia autonoma Trento', 'denominazione_regione'] = 'P.A. Trento'

        frame = pd.merge(frame, df, how="left", on=["data", "denominazione_regione"])

    print(frame.head)
    frame.to_csv(file_OUT)
