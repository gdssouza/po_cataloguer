# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 10:09:19 2020

@author: Anon
"""

# importando bibliotecas
import pandas as pd
import os
from datetime import datetime
# enter the API directory:
os.chdir("iqoptionapi")
# API
from iqoptionapi.stable_api import IQ_Option
os.chdir('../') # back

def analyze_trend(df, periodo):
    # recebe um dataframe com os candles
    # retorna um dataframe com a tendencia dos candles para um período
    return None

def delta_days(start,end):
    # Data inicial
    d1 = datetime.strptime(start, '%Y/%m/%d')
    # Data final
    d2 = datetime.strptime(end, '%Y/%m/%d')
    return d1, d2, abs((d2 - d1).days)

class cataloguer(IQ_Option):
    def __init__(self,email,password):
        '''
        

        Parameters
        ----------
        email : string
        password : string

        Returns
        -------
        None.

        '''
        self.email = email
        self.password = password
        self.API = False

    def connect(self):
        '''
        

        Returns
        -------
        API : iqoptionapi.stable_api.IQ_Option(email,password)

        '''
        # conectar com a corretora
        API = IQ_Option(self.email,self.password)
        error_password ="""{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
        check,reason = API.connect()
        if check:
            print("Start your robot")
            #if see this you can close network for test
            if API.check_connect() == False:#detect the websocket is close
                print("Try reconnect")
                check,reason = API.connect()         
                if check:
                    print("Reconnect successfully")
                else:
                    if reason == error_password:
                        print("Error Password")
                    else:
                        print("No Network")
            else:
                mode = 'PRACTICE'
                API.change_balance(mode)
        else:
            if reason == "[Errno -2] Name or service not known":
                print("No Network")
            elif reason == error_password:
                print("Error Password")
        self.API = API
        return self.API
           
    def to_df(self,candles):
        '''
        

        Parameters
        ----------
        candles : dic

        Returns
        -------
        df_filtered : pandas DataFrame

        '''
        dic = {'id':[],'from':[],'at':[],'to':[],'open':[],'close':[],'min':[],'max':[],'volume':[]}
        for candle in candles:
            for item in candle:
                dic[item].append(candle[item])
        df = pd.DataFrame(dic)
        
        # convertendo timestamp para datetime
        date = pd.to_datetime(df['at']).dt.floor('1min')
        
        # filtrando dentro do interval start - end
        interval = date >= self.start
        df_filtered = df[interval]
        date_filtered = date[interval]
                
        # criando multiindex
        df_size = len(date_filtered)
        df_filtered.index = pd.MultiIndex.from_arrays([[self.goal]*df_size, date_filtered], names=('goal', 'date'))
        # deletando colunas redundantes
        df_filtered = df_filtered.drop(columns=['id','from','at','to'])
        
        return df_filtered
        
    def read_candles(self,goal,timeframe,start,end):
        '''
        

        Parameters
        ----------
        goal : string
        timeframe : int
        start : pandas datetime
        end : pandas datetime

        Returns
        -------
        df : pandas DataFrame

        '''
        start, end, days = delta_days(start,end)
        date = datetime.timestamp(end)
        amount = {60*1:1440, 60*5:288, 60*15:96}
        len_candles = int(amount[timeframe]*days)
        if len_candles < 1000:
            candles = self.API.get_candles(goal, timeframe, len_candles, date)
        else:
            candles = []
            for pacote in range(1000,len_candles,1000):
                candles = self.API.get_candles(goal, timeframe, pacote, date) + candles
                date = candles[0]['from']
            candles = self.API.get_candles(goal, timeframe, int(len_candles%1000), date) + candles
            
        self.goal = goal
        self.start = start
        
        return self.to_df(candles)