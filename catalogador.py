# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 18:20:14 2020

@author: Anon
"""

# importando bibliotecas
import time
import pandas as pd
import os
# enter the API directory:
os.chdir("iqoptionapi")
from iqoptionapi.stable_api import IQ_Option

# lendo informações de login
config = open('config.txt')
email = config.readline().strip('\n')   
password = config.readline().strip('\n')

# variaveis
mode = 'PRACTICE'
days = int(input("Insira quantos dias: "))
timeframe = int(input("Insira o timeframe em minutos: "))*60
par = input("Insira o ativo: ")
print()

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
API.change_balance(mode)

# lendo candles
qtd = {60*1:1440, 60*5:288, 60*15:96}
total_candles = int(qtd[timeframe]*days)
if total_candles < 1000:
    velas = API.get_candles(par, timeframe, total_candles, time.time())
else:
    velas = []
    data = time.time()
    for pacote in range(1000,total_candles,1000):
        velas = API.get_candles(par, timeframe, pacote, data) + velas
        intervalo = int(velas[0]['from'])-1
        data = velas[0]['from']
    velas = API.get_candles(par, timeframe, int(total_candles%1000), data) + velas
            
# convertendo para dataframe
dic = {'id':[],'from':[],'at':[],'to':[],'open':[],'close':[],'min':[],'max':[],'volume':[]}
for vela in velas:
    for item in vela:
        dic[item].append(vela[item])
df = pd.DataFrame(dic)

# convertendo timestamp para datetime
date = pd.to_datetime(df['at']).dt.floor('1min')
# criando multiindex
df.index = pd.MultiIndex.from_arrays([[par]*total_candles, date], names=('goal', 'date'))
# deletando colunas redundantes
df = df.drop(columns=['id','from','at','to'])

# salvando
caminho = par+'.csv'
df.to_csv(caminho)
print("Salvo em",caminho)

print(df.head())