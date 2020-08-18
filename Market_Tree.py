
'''
A market tree is a bi-directional graph that represents a network for a particular exchange. The market tree is recursively defined (i.e. all assets in an exchange represent the market tree themsevlves

Self.branches points to an array of Market Trees  - similar to most default implementations of a tree, all of the branches poit to trees themselves
'''

class MarketTree():
    num_calls = 0 #keeps track of number of recursive calls to a function; used for getting an idea of complexity
    def __init__(self, asset:str, branches=None): #asset is a string, branches is an array of other MarketTrees; null is a tree
        self.asset = asset
        if branches==None:
            self.branches = [] #branches is an array of [distance, MarketTree]
        self.num_branches = len(self.branches) 

    """ 
    Prints the first-layer of connections to the tree_root
    """
    def __repr__(self) -> str: #
        print_string=self.asset + ": "
        for branch in self.branches:
            print_string+= str(branch[0])+ "-" + str(branch[1].asset)+ ", "
        return print_string
        
       """
       Adds a market instance, represented by a bidirectional connection between nodes, between self and sub_tree. Each each direction represents the bid and ask price, between two assents. 

       This class is used when parsing in data into a netork for a particular exchange. Due to the bi-directional nature, the branch pointer existsb both from this market and from the added market- t hus the added pinter must be added from both the market tree. Thus, this method is typically added in bid/ask pairs. 

       Parameters
       ----------
       sub_tree : MarketTree
           Market_Tree that represents the asset of each 
       distance : float
           The price to convert between self and sub_tree. 

    """
    def add_branch(self, sub_tree:'MarketTree', distance:float) -> None: #adds a MarketTree onto one of the branches
        self.branches.append([float(distance), sub_tree])
        self.num_branches+=1
        return
       
       """
       Returns the distance between self and the MarketTree at a given index within self's branches

       This class is used from the get_max_branch function.
       Parameters
       ----------
       index : int
           The index of the branch to return the distance from self at
        
    """
    def get_distance(self, index:int): #returns the dstance to the branch at index
        if index>=self.num_branches: #index is out of range
            return None
        else:
            return self.branches[index][0]
         
         
      """
      Similar to get_distance, but returns the branch itself instead of the distance to the branch
      This class is used from the get_max_branch function.
      Parameters
      ----------
      index : int
          The index of the branch that will be returned

    """
    def get_branch(self, index:int): #returns the branch at index
        if index>=self.num_branches: #index is out of range
            return None
        else:
            return self.branches[index][1]

          """
      Similar to get_distance, but takes the name of the market_tree instead of the index of the market_tree. 
      Parameters
      ----------
      target_asset : str
          The name of the branch to find the distance
    """"
     
    def find_distance(self, target_asset:str): #given the name of an asset, finds the distance to the asset
        for branch in self.branches:
            sub_tree = branch[1] 
            if sub_tree.asset==target_asset:
                target_distance = branch[0]
                return target_distance
        return None #the target_asset is not found

      """
      Finds a cyclical path that starts and ends at the tree deliniated by the name target_asset Returns a string corresponding to the path that the max_path takes through the network, and the quantity of the start asset that is returned after trading along the returned path. 
      Parameters
      ----------
      target_asset : str
          The name of the MarketTree that is being found for teh cyclical path. This is used to keep track between recursive calls that aren't called at the root of the initial method call.       
          searched_nodes : array
          An array of all paths which have been searched in finding the maximum path. This is used only in recursive calls, and can thus be specified as an empty array when being called as a user. This argument is used to ensure that all returned subpaths are not repeated.
          trading_fee : float
          A float representing the amount of an asset retained after trading. This method assumes that a normalized trading fee (i.e. one that scales with the amount of asset that is traded) is applied - to specify a fixed trading fee that is independent of the amount that is traded, it can be done outside of this method and added to the ratio of the start asset that this function returns. 
          
          
    """"
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

