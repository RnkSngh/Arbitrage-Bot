# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 22:33:42 2018

@author: rauna
"""

'''
Uses Market_Tree.py and KuCoin_Trade_Functions.py to find and execute arbitrage opportunities on Kucoin.com. 
'''

##############################################
#IMPORTING THE DRIVERS AND LIBRARIES
##############################################
import Market_Tree
import KuCoin_Trade_Functions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from time import time
import datetime
from datetime import datetime
from urllib2 import *
import urllib
from Market_Tree import *
import requests
import json
import httplib
import threading
from multiprocessing import Pool
from selenium.webdriver.support.ui import WebDriverWait
from kucoin.client import Client
##############################################



##############################################
#User defined variables 
##############################################
Username= '' #Kucoin Username & Password
Password= '' 
out_file_name= "trade_data_.csv" #Name of output file that keeps trading data
key = ''  #kucoin API key and secret key
secrt = ''
target_root = "BTC" #Name of starting and ending asset for the arbitrage path
trading_fee = .999 #amount retained after applying trading fees
##############################################


#Write header line of output file
ouptut_file= open(out_file_name, "a+")
ouptut_file.write("Time, Gain, valid,  Path, Trade Vol  \n")


##############################################
#Load and process data 
##############################################

while 1==1:
    try:
        start_time= time.time()

        url_base= [] #holds all of the market url extensions of traded currencies
        currencies=[] #holds all of the names of traded currencies 
        tree_list=[] #A Market_tree array

        #get most recent trading data
        request = requests.get('https://api.kucoin.com/v1/open/tick')
        request_data = json.loads(request.text)["data"]
        market_data = {}

        #loop through and input each coin into the structure
        for i in range(200):
            
            dataline = request_data[i]
            buy_price= dataline["buy"]
            sell_price= dataline["sell"]
            recent_vol = dataline["vol"]

            if recent_vol==0: #skip over loading assets not being traded
                continue
            
            crypto_pair = dataline["symbol"]
            url_base.append(crypto_pair)
            crypto_pair= crypto_pair.split("-") 
            quote_asset= crypto_pair[1] #Seperate base and quote assets
            base_asset = crypto_pair[0]
            
            #check if quote and base assets have been added in previous iterations; load them if they have not yet been added
            if quote_asset in currencies: 
                quote_asset_index= currencies.index(quote_asset)
            else:
                currencies.append(quote_asset)
                quote_index= len(currencies)-1
                tree_list.append(MarketTree(quote_asset))

            if base_asset in currencies:
                base_asset_index= currencies.index(base_asset)
            else:
                currencies.append(base_asset)
                base_asset_index= len(currencies)-1
                tree_list.append(MarketTree(base_asset))
            
            quote_asset_tree= tree_list[quote_asset_index]
            base_asset_tree= tree_list[base_asset_index]
            quote_asset_tree.add_branch(base_asset_tree, 1/sell_price) #the bi-directional differences represent the most competitive bid and ask prices
            base_asset_tree.add_branch(quote_asset_tree, buy_price)

        #find index of the root of starting and ending market
        for i in range(len(tree_list)):
            if tree_list[i].coin== target_root:
                target_tree = tree_list[i]
                break

        [distance, path]  = target_tree.get_max_branch(target_root, None, trading_fee)

        if distance > 1: #check if the best trading path would be profitable, excute if it would be
            [valid, starting_vol] = validate_opportunity(paths)
            if valid:
                place_order(paths, starting_vol)
        
        network_time= time.time()-start_time
        #write to output file 
        ouptut_file.write(str(network_time) + ", " + str(distance) + ", " + str(valid) + ", " + path + ", " + str(starting_vol) + " \n")



    except Exception as e: #print exception if error is encountered
        print(e)
        continue

