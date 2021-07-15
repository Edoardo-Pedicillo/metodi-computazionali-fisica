import unittest

import crossover

class test_crossover (unittest.TestCase):

    def test_based_ordered_1 (self):
        p1=[1,2,3,4,5]
        p2=[3,1,4,2,5]
        selected_cities=[2,4]
        son = crossover.based_ordered_crossover(p1,p2,2,selected_cities)
        result1=[3,1,2,4,5]
        self.assertEqual(result1,son)
        self.assertEqual([1,4,3,2,5],crossover.based_ordered_crossover(p2,p1,2,selected_cities))# Scambio p1 -> p2

    def test_based_ordered_2 (self):
        p1=[2,7,6,3,1,5,4,8]
        p2=[4,5,6,2,8,7,3,1]
        selected_cities=[2,6,3,8]
        result=[4,5,2,6,3,7,8,1]
        son= crossover.based_ordered_crossover(p1,p2,2,selected_cities)
        self.assertEqual(result,son)
        
    def test_modified_ordered_crossover_1 (self):
         p1=[1,2,3,4,6,9,8,5,7]
         p2=[2,1,9,8,5,6,3,7,4]
         son=crossover.modified_ordered_crossover(p1,p2,4)
         result=[2,1,6,9,8,5,3,7,4]
         self.assertEqual(result,son)

    def test_modified_ordered_crossover_2 (self):
         p1=[1,2,3,4,6,9,8,5,7]
         p2=[2,1,9,8,5,6,3,7,4]
         son=crossover.modified_ordered_crossover(p2,p1,4)
         result=[1,2,5,6,3,9,8,7,4]
         self.assertEqual(result,son)

    def test_partially_mapped_crossover1(self):
        p1=[5,2,6,0,3,4,1]
        p2=[6,5,1,2,4,3,0]
        son=crossover.partially_mapped_crossover(p1,p2,2,6)
        result=[5,0,1,2,4,3,6]
        self.assertEqual(result,son)

    def test_partially_mapped_crossover2(self):
        p1=[5,2,6,0,3,4,1]
        p2=[6,5,1,2,4,3,0]
        son=crossover.partially_mapped_crossover(p2,p1,2,6)
        result=[1,5,6,0,3,4,2]
        self.assertEqual(result,son)
    
    def test_cycle_crossover1(self):
        
        p1=[5,2,6,0,3,4,1]
        p2=[6,5,1,2,4,3,0]
        son=crossover.cycle_crossover(p1,p2,1,verbose=False)
        
        self.assertEqual([6, 5, 1, 2, 4, 3, 0],son)

    def test_cycle_crossover2(self):
        
        p1=[5,2,6,0,3,4,1]
        p2=[6,5,1,2,4,3,0]
        son=crossover.cycle_crossover(p1,p2,0,verbose=False)
        
        self.assertEqual([5,2,6,0,3,4,1],son)



if __name__ == '__main__': 
    unittest.main()