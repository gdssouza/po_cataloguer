# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 18:20:14 2020

@author: Anon
"""

import time
# hight level api ,This api is write base on ""iqoptionapi.api" for more easy
from iqoptionapi.stable_api import IQ_Option

config = open('config.txt')
email = config.readline().strip('\n')   
password = config.readline().strip('\n')
mode = 'PRACTICE'
days = 7
timeframe = 60

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
velas = API.get_candles('EURUSD',timeframe,days,time.time())
print(velas)