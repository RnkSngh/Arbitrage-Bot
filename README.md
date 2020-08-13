# Overview
This repo contains a tool for downloading and analyzing arbitrage opportunities by solving the longest path problem for a network of assets. 

# MarketTrees
A MarketTree is a bi-directed graph where each node represents an asset, and bi-directed links between nodes represent the bid and ask price at the time of the latest data retrieval. Thus, the product of links along a path between nodes represents the quantity of the end asset obtained after following a path connecting the beginning and end asset.

## Longest Path Example
[](./ExampleArbitrageOpportunity.png)
For example, take A, B and C separate assets, each represented as a node in the graph, which are traded among each other at independent bid and ask prices (each represented as a directional link connecting two nodes). Trading 1 unit of A for B at an ask price of 0.25 would yield 0.25 units of B. Trading 0.25 units of B for C at the ask price of 2 would yield 0.5 units of C. This example should illustrate that the quantity of the end asset obtained is the distance (i.e. the product of the links) along the path from asset A to asset C.

Executing one last trade to exchange 0.5 units of C for A at an ask price of 2 yields 1.5 units of A (which is more than we started with!). Thus, any cyclical path (i.e. starting and ending at the same node) with a distance greater than 1 represents an arbitrage opportunity - a series of trades which would yield a greater quantity of the starting asset after execution. 

# Repo Structure
Market_Tree.py contains the implementation of this data structure, and a function called get_max_path which finds the longest path that starts and ends at the root of a specified target node. To avoid infinite cycling, each link between nodes is used only once in a path. 

Arbitrage_tester.py contains a basic set of unittests to test the Market_Tree implmenetaiton. 
 
Kucoin_Arbitrage_ETL.py is a script that loads the latest Kucoin trading data into the Market_Tree structure. The script then finds and executes the greatest arbitrage opportunity, if one exists, using functions from KuCoin_Trade_Functions.py.
