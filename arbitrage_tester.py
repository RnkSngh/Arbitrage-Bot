''' For testing the Market Tree class to ensure outputs and future changes do not affect past tests

'''
from Market_Tree import *
import unittest


class TestMarket_Tree(unittest.TestCase):

    def test_simple_functions(self): #test init, add_branch, and find_distance functions
        tree_a= MarketTree("A")
        tree_b= MarketTree("B")
        tree_c=MarketTree("C")
        tree_a.add_branch(tree_b, 4)
        tree_d=a.get_branch(0)
        dist_to_b = tree_a.find_distance("B")
        self.assertEqual(tree_a.asset, 'A')
        self.assertEqual(tree_a.get_distance(0), 4)
        self.assertEqual(str(tree_b), str(MarketTree("B")))
        self.assertEqual(dist_to_b, 4)

    def test_get_max_branch(self):
        tree_a= MarketTree("A")
        tree_b= MarketTree("B")
        tree_a.add_branch(tree_b, 4)
        self.assertEqual(tree_a.get_max_branch("A"), [0, "A"])
        tree_b.add_branch(tree_a, 5)
        self.assertEqual(tree_a.get_max_branch("A"), [20, "ABA"])
    
        tree_c=MarketTree("C")
        tree_b.add_branch(tree_c, 5)
        tree_a.add_branch(tree_c, 3)
        tree_c.add_branch(tree_a, 2)
        self.assertEqual(tree_a.get_max_branch("A"), [120, "ABACA"])
        tree_d=MarketTree("D")
        tree_b.add_branch(tree_d, 2)
        tree_d.add_branch(tree_b, 4)
        self.assertEqual(tree_a.get_max_branch("A"), [960, "ABDBACA"])

    def test_float_get_max_branch(self): #test float values
        tree_a= MarketTree("A")
        tree_b= MarketTree("B")
        tree_a.add_branch(tree_b, 1.4)    
        tree_b.add_branch(tree_a, 1.5)
        self.assertEqual(tree_a.get_max_branch("A"), [2.1, "ABA"])
    
        tree_c=MarketTree("C")
        tree_b.add_branch(tree_c, 1.5)
        tree_a.add_branch(tree_c, 1.2)
        tree_c.add_branch(tree_a, 1.3)
        self.assertEqual(tree_a.get_max_branch("A"), [3.276, "ABACA"])
        tree_d=MarketTree("D")
        tree_b.add_branch(tree_d,1.2)
        tree_d.add_branch(tree_b, 1.4)
        self.assertEqual(tree_a.get_max_branch("A"), [5.50368, "ABDBACA"])

        

if __name__ == '__main__':
    unittest.main()
