# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 18:20:14 2020

@author: Anon
"""

# API
from functions import catalogador
from pyfiglet import Figlet

# cabecalho
f = Figlet(font='standard')
print(f.renderText('CATALOGUER'))
print("By Gustavo Souza")
print("Repository: https://github.com/gdssouza/po_bot_with_telegram")
print()

# lendo informações de login
config = open('config.txt')
email = config.readline().strip('\n')   
password = config.readline().strip('\n')

# variaveis
mode = 'PRACTICE'
start = '2020/12/01'
end = '2020/12/18'
timeframe = 60*15
par = 'EURUSD'

#start = input("Insira a data de início YYYY/MM/DD")
#start = input("Insira a data de término YYYY/MM/DD")
#timeframe = int(input("Insira o timeframe em minutos: "))*60
#par = input("Insira o ativo: ")
#print()

api = catalogador(email,password)
df = api.ler_candles(par, timeframe, start, end)

# salvando
caminho = par+'.csv'
df.to_csv(caminho)
print("Salvo em",caminho)

print(df.head())