# Arbitrage-Bot
A bot which downloads, analyzes, and executes arbitrage opportunities

A MarketTree is a bi-directional graph where each node represents an asset, and bi-directional links between nodes represent the bid and ask price at the time of the latest data retrieval. Thus, the product of links along a path between nodes represents the quantity of the end asset obtained after following a path connecting the beginning and end asset.

For example, take A, B and C as different assets (each represented as a node in the graph) which are traded at a bid and ask price (each represented as a directional link connecting two nodes) per each pair. Trading 1 unit of A for B at an ask price of x would yield x units of B. Trading x units of B for C at the ask price of y would yield x*y units of C. Thus, the quantity of the end asset obtained is the distance (i.e. the product of the links) along the path from asset A to asset C.

 Consequently, any cyclical path (i.e. starting and ending at the same node) with a distance greater than 1 represents an arbitrage opportunity - a series of trades which would yield a greater quantity of the starting asset after execution. 
 
Market_Tree.py contains the implementation of this data structure, and a function called get_max_path which finds the longest path which starts and ends at the root of a specified target node. To avoid infinite cycling, each link between nodes can only be used once in a path. 

Arbitrage_tester.py contains a basic set of unittests to test the Market_Tree implmenetaiton. 
 
Kucoin_Arbitrage_ETL.py is a script that extracts, transforms, and loads Kucoin trading data into the Market_Tree structure. The script then executes the greatest arbitrage opportunity using KuCoin_Trade_Functions.py if it would profitable.
