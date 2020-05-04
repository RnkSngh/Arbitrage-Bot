# -*- coding: utf-8 -*-
"""
Created on Sun May  3 20:54:28 2020

@author: User
"""

"""
Useful function wrappers for interfacing between the Kucoin API and Market_Tree data structure
"""


#validate arbitrage opportunity will be profitable after trading
def validate_opportunity(path):

    path_urls = market.split("-")

    trade_length = len(max_urls) - 1 #number of trades that are needed in the arbitrage opportunity
    min_starting_volume = 1 #keeps track of the volume needed to start the arbitrage
    verified_return = 1 #verified return if the arbitrage along the path is executed
    
    
    # build switched and url_pairs
    for path_url in range(trade_length):
        first = path_urls[path_url]
        second = path_urls[path_url + 1]
        end_url = first + "-" + second

        if not end_url in url_base: #means the end_url should be switched
            end_url = second + "-" + first
            verified_return = verified_return * (1 / sell_price)
            min_starting_volume = min_starting_volume / sell_price
            
        else:
            verified_return = verified_return * buy_price
            min_starting_volume =  min_starting_volume * buy_price

                
    verified_return = verified_return * (trading_fee ** trade_length) #apply trading fee to the number of trades

    #set valid to 1 if verified return is profitable
    if verified_return>1:
        valid = True
    else:
        valid =  False
        
    return [valid, min_starting_vol]


#executes an arbitrage opportunity based on the given path and starting volume
def place_order(path, starting_vol):
    

    path_urls = path.split('-')
    trade_length = len(path_urls)
    current_vol = starting_vol 
    
    for u in range(trade_length): #iterate through each list
        first = path_urls[path_url]
        second = path_urls[path_url + 1]
        end_url = first + "-" + second
        
        
        if end_url in url_base: #determine if we need to switch the order of assets in the url or not
            URL = max_urls[u] + "-" + max_urls[u+1]
            [buy_price, buy_vol, sell_price, sell_vol] = market_data[URL]

            amount = current_vol*trading_fee
            current_vol = current_vol*buy_price
            price = buy_price
            formatted_amount = '{0:.7f}'.format(amount)
            formatted_price = '{0:.8f}'.format(price)
            client.create_sell_order(URL, formatted_price, formatted_amount)
            

        else:    #means we have to switch, should switch url order 
            URL = max_urls[u+1] + "-" + max_urls[u]
            [buy_price, buy_vol, sell_price, sell_vol] = market_data[URL]

            price = sell_price
            current_vol = trading_fee*current_vol/sell_price
            formatted_current_vol = '{0:.7f}'.format(current_vol)
            formatted_price = '{:1.8f}'.format(price)
            client.create_buy_order(URL, formatted_price, formatted_current_vol)

        time.sleep(0.5) #pause for half a second for network stability
        



        