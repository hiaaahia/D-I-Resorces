#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 21:22:22 2020

@author: houjiani
"""

import datetime as dt
import pandas as pd

df_empty=pd.DataFrame(columns=['Date', 'Temperature, *C, SEU ARCH', 'RH, %, SEU ARCH', 'Dew Point, *C, SEU ARCH','Rain, mm, SEU ARCH Rain','Solar Radiation, W/m^2, SEU ARCH solar radiation','Wind Speed, m/s, SEU ARCH Wind speed'])

def excelTodf(year):
    global df_empty
    i_data = '/Users/houjiani/Downloads/作业/srtp/东南大学微气候特征预测/东南大学微气候特征预测/data/Data backup/WW_SEU_Climate_'+str(year)+'.xlsx'
    df=pd.read_excel(i_data)

    df.dropna(how='any')  
#print(df.dropna(how='any'))
    df2 = df.drop(['Gust Speed, m/s, SEU ARCH', 'Pressure, mbar, SEU ARCH Air pressure','Wind Direction, *, SEU ARCH Wind direction',], axis=1)
    df2 = df.dropna(how='any') 

    df2['Date']=pd.to_datetime(df2['Date'],format='%y-%m-%d %H:%M:%S')

    for index, row in df2.iterrows():
        if row['Date'].minute==0:
            df_empty.loc[index]=df2.loc[index]
    df_empty.set_index(df_empty['Date'],inplace=True)



listYear = [2017,2018,2019,2020]
listMonth = [8,9,10,11,12]
df_sumMax = pd.DataFrame(columns=['Date', 'Temperature, *C, SEU ARCH', 'RH, %, SEU ARCH', 'Dew Point, *C, SEU ARCH','Wind Speed, m/s, SEU ARCH Wind speed'])
df_sumMin = pd.DataFrame(columns=['Date', 'Temperature, *C, SEU ARCH', 'RH, %, SEU ARCH', 'Dew Point, *C, SEU ARCH'])
df_sumSum = pd.DataFrame(columns=['Rain, mm, SEU ARCH Rain','Solar Radiation, W/m^2, SEU ARCH solar radiation'])

def getAday(year,i,j):
    global df_sumMax,df_empty
    global df_sumSum
    global df_sumMin
    
    if (i<10 and j<10):
        c=str(year)+'-0'+str(i)+'-0'+str(j)
    elif (i<10 and j>10):
        c=str(year)+'-0'+str(i)+'-'+str(j)
    elif (i>10 and j<10):
        c=str(year)+'-'+str(i)+'-0'+str(j)
    c=str(year)+'-'+str(i)+'-'+str(j)
    
    df_empty1 = pd.DataFrame(columns=['Date', 'Temperature, *C, SEU ARCH', 'RH, %, SEU ARCH', 'Dew Point, *C, SEU ARCH','Rain, mm, SEU ARCH Rain','Solar Radiation, W/m^2, SEU ARCH solar radiation','Wind Speed, m/s, SEU ARCH Wind speed'])
    df_empty1 = df_empty.loc[c:c]
    """
    df_max = df_empty1.max()
    df_max = pd.DataFrame(df_max)
    df_max = pd.DataFrame(df_max.values.T,index=df_max.columns, columns=df_max.index)
    df_max=df_max.drop(['Rain, mm, SEU ARCH Rain','Solar Radiation, W/m^2, SEU ARCH solar radiation'],axis=1)
    df_sumMax = pd.concat([df_sumMax, df_max])
    
    df_min = df_empty1.min()
    df_min = pd.DataFrame(df_min)
    df_min = pd.DataFrame(df_min.values.T,index=df_min.columns,columns=df_min.index)
    df_sumMin = pd.concat([df_sumMin,df_min])
    
    df_empty1 = df_empty1.drop(['Temperature, *C, SEU ARCH', 'RH, %, SEU ARCH', 'Dew Point, *C, SEU ARCH','Wind Speed, m/s, SEU ARCH Wind speed'],axis=1)
    df_sum = df_empty1.sum()
    df_sum = pd.DataFrame(df_sum)
    df_sum = pd.DataFrame(df_sum.values.T,index=df_sum.columns,columns=df_sum.index)
    df_sumSum = pd.concat([df_sumSum,df_sum],ignore_index=True)
    """
    df_empty1 = df_empty1.drop(['Temperature, *C, SEU ARCH', 'RH, %, SEU ARCH', 'Dew Point, *C, SEU ARCH','Wind Speed, m/s, SEU ARCH Wind speed'],axis=1)
    df_sum = df_empty1.max()
    df_sum = pd.DataFrame(df_sum)
    df_sum = pd.DataFrame(df_sum.values.T,index=df_sum.columns,columns=df_sum.index)
    df_sumSum = pd.concat([df_sumSum,df_sum],ignore_index=True)
    



def dayAndmonth(year):
    if (year==2016):
        for i in listMonth:
            if (i==8):
                for j in range(8,32):
                    getAday(year,i, j)
            elif (i==10):
                for j in range(1,32):
                    getAday(year,i, j)
            elif (i==11 or i==9):
                for j in range(1,31): 
                    getAday(year,i, j)
            elif (i==12):
                for j in range(1,12):
                    getAday(year,i, j)
    elif (year == 2017 or year == 2018 or year == 2019 ):
        for i in range(1,13):
            if (i==2):
                for j in range(1,29):
                    getAday(year,i, j)
            elif (i==8 or i==1 or i==3 or i==5 or i==7 or i==10 or i==12):
                for j in range(1,32):
                     getAday(year,i, j)
            elif (i==4 or i==6 or i==9 or i==11):
                for j in range(1,31):
                    getAday(year,i, j)
    elif (year == 2020):
        for i in range(1,6):
            if (i == 2):
                for j in range(1,30):
                    getAday(year,i, j)
            elif (i==1 or i==3 or i==5):
                for j in range(1,32):
                     getAday(year,i, j)
            elif (i==4):
                for j in range(1,31):
                    getAday(year,i, j)
            elif (i==5):
                for j in range(1,7):
                    getAday(year,i, j)
            
            
                    
for year in listYear:
    excelTodf(year)
    dayAndmonth(year)        
    
df_sumMax.set_index(df_sumMax['Date'],inplace=True)
df_sumMin.set_index(df_sumMin['Date'],inplace=True)

#df_sumMin.to_excel("min.xlsx",sheet_name='Sheet1')
df_sumSum.to_excel("solarmax.xlsx",sheet_name='Sheet1')
    
    