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

def analisar_tendencia(df):
    return None

def delta_days(start,end):
    # Data inicial
    d1 = datetime.strptime(start, '%Y-%m-%d')
    # Data final
    d2 = datetime.strptime(end, '%Y-%m-%d')
    return d1, d2, abs((d2 - d1).days)

class catalogador(IQ_Option):
    def __init__(self,email,password):
        # conectar com a corretora
        API = IQ_Option(email,password)
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
            if reason == "[Errno -2] Name or service not known":
                print("No Network")
            elif reason == error_password:
                print("Error Password")
                
        mode = 'PRACTICE'
        API.change_balance(mode)
        self.API = API
    
    def get_API(self):
        return self.API
    
    def to_df(self,velas):
        dic = {'id':[],'from':[],'at':[],'to':[],'open':[],'close':[],'min':[],'max':[],'volume':[]}
        for vela in velas:
            for item in vela:
                dic[item].append(vela[item])
        df = pd.DataFrame(dic)
        
        # convertendo timestamp para datetime
        date = pd.to_datetime(df['at']).dt.floor('1min')
        # filtrando dentro do intervalo start - end
        intervalo = date >= self.start
        df_filtrado = df[intervalo]
        date_filtrado = date[intervalo]
        df_size = len(date_filtrado)
        # criando multiindex
        df_filtrado.index = pd.MultiIndex.from_arrays([[self.par]*df_size, date_filtrado], names=('goal', 'date'))
        # deletando colunas redundantes
        df_filtrado = df.drop(columns=['id','from','at','to'])                    
    
        return df_filtrado
        
    def ler_candles(self,par,timeframe,start,end):
        start, end, days = delta_days(start,end)
        data = datetime.timestamp(end)
        qtd = {60*1:1440, 60*5:288, 60*15:96}
        total_candles = int(qtd[timeframe]*days)
        if total_candles < 1000:
            velas = self.API.get_candles(par, timeframe, total_candles, data)
        else:
            velas = []
            for pacote in range(1000,total_candles,1000):
                velas = self.API.get_candles(par, timeframe, pacote, data) + velas
                data = velas[0]['from']
            velas = self.API.get_candles(par, timeframe, int(total_candles%1000), data) + velas
            
        self.par = par
        self.start = start
        
        return self.to_df(velas)