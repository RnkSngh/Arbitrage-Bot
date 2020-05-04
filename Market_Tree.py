# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 22:33:42 2018

@author: raunak
"""

'''
A MarketTree is a bi-directional graph where each node represents an asset, and bi-directional links between nodes represent the bid and ask price at the time of the latest data retrieval. Thus, the product of links represents the quantity of the end asset obtained after following a path connecting the beginning and end asset.

For example, take A, B and C as different assets (each represented as a node in the graph) which are traded at a bid and ask price (each represented as a directional link connecting two nodes) per each pair. Trading 1 unit of A for B at an ask price of x would yield x units of B. Trading x units of B for C at the ask price of y would yield x*y units of C. Thus, the quantity of the end asset obtained is the distance (i.e. the product of the links) along the path from asset A to asset C.

 Consequently, any cyclical path with a distance greater than 1 represents an arbitrage opportunity - a series of trades which would yield a greater quantity of the starting asset after execution. 

'''

class MarketTree():
    num_calls = 0 #keeps track of number of recursive calls to a function; used for getting an idea of complexity
    def __init__(self, asset:str, branches=None): #asset is a string, branches is an array of other MarketTrees; null is a tree
        self.asset = asset
        if branches==None:
            self.branches = [] #branches is an array of [distance, MarketTree]
        self.num_branches = len(self.branches) 

    def __repr__(self) -> str: #prints the first-layer of connections to the tree_root
        print_string=self.asset + ": "
        for branch in self.branches:
            print_string+= str(branch[0])+ "-" + str(branch[1].asset)+ ", "
        return print_string
        
    def add_branch(self, sub_tree:'MarketTree', distance:float) -> None: #adds a MarketTree onto one of the branches
        self.branches.append([float(distance), sub_tree])
        self.num_branches+=1
        return

    def get_distance(self, index:int): #returns the dstance to the branch at index
        if index>=self.num_branches: #index is out of range
            return None
        else:
            return self.branches[index][0]

    def get_branch(self, index:int): #returns the branch at index
        if index>=self.num_branches: #index is out of range
            return None
        else:
            return self.branches[index][1]

    def find_distance(self, target_asset:str): #given the name of an asset, finds the distance to the asset
        for branch in self.branches:
            sub_tree = branch[1] 
            if sub_tree.asset==target_asset:
                target_distance = branch[0]
                return target_distance
        return None #the target_asset is not found


    def get_max_branch(self, target_asset:str, searched_nodes = None, trading_fee:float = 1 ): #searches through all possible combinations through a tree and gets the longest path leading back to the target_asset without repeating links
        MarketTree.num_calls+=1
        
        if searched_nodes == None: #convert default argument to be immutable
            searched_nodes= ''
        
        if self.num_branches == 0: #will return 0 if there are no breanches to follow in a path 
            return [[0] , ['']]
    

        searched_nodes +=self.asset #searched nodes keeps track of visited nodes to avoid infinite cycling
        
        paths=[]
        distances=[]


        for branch_index in range(self.num_branches): 

            sub_branch= self.get_branch(branch_index)
            sub_name= sub_branch.asset
            
            if self.asset + sub_name not in searched_nodes: #if the asset has not been visited yet, add potential sub paths to paths
                [sub_distances, sub_paths]= sub_branch.get_max_branch(target_asset, searched_nodes, trading_fee)
                for sub_path_index in range(len(sub_distances)):
                    sub_distances[sub_path_index]= sub_distances[sub_path_index]*self.get_distance(branch_index)*trading_fee
                    sub_paths[sub_path_index]= self.asset + sub_paths[sub_path_index]
                
                distances= distances + sub_distances
                paths = paths + sub_paths
            else: #if the tree has already been visited
                distances.append(trading_fee)
                paths.append(self.asset)
                
        if self.asset==target_asset and searched_nodes == self.asset: #this only triggers for the initial function call; this prunes the return paths to only get the highest path
            
            zipped_distances = list(zip(distances, paths))
            distances = [distance for distance, path in zipped_distances if path[-1]==target_asset] #only get the paths which end at the target_asset
            paths  = [path for distance, path in zipped_distances if path[-1]==target_asset]
            max_index= distances.index(max(distances))
            formatted_distance = float(format(distances[max_index], ".8f")) #format to get right decimal accuracy
            return [formatted_distance, paths[max_index]]
        
        return [distances , paths]  #this return is used for recursive calls

