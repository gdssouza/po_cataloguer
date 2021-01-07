# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 18:20:14 2020

@author: Anon
"""

# API
from functions import cataloguer
from pyfiglet import Figlet
from time import time

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

# API DA IQ
api = cataloguer(email,password)
api.connect()

# coletando parametros
start = input("Insert start date YYYY/MM/DD :/> ")
end = input("Insert end date YYYY/MM/DD :/> ")
timeframe = int(input("Insert timeframe in minutes :/> "))*60
goal = input("Insert the goal :/> ")

# lendo candles
ti = time()
df = api.read_candles(goal, timeframe, start, end)
tf = time()
# imprimindo infos
print('%i candles read in %.2f seconds'%(len(df.index),tf-ti))

# salvando
local = goal+'.csv'
df.to_csv(local)
print("Saved in",local)

print(df.head())