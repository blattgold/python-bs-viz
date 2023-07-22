import unittest
import bs

class TestSearchStep(unittest.TestCase):
    def runTest(self):
        b = bs.Bs()
        b.to_sort = []
        self.assertEqual(b.search_step(), 
                         None)
        
        b = bs.Bs()
        b.to_sort = [0]
        self.assertEqual(b.search_step(),
                         None)

        b = bs.Bs()
        b.to_sort = [0, 0.1]
        self.assertEqual(b.search_step(),
                          None)

        b = bs.Bs()
        b.to_sort = [0.1, 0]
        self.assertEqual(b.search_step(),
                          1)

        b = bs.Bs()
        b.to_sort = [1, 2, 1]
        self.assertEqual(b.search_step(),
                          None)
        self.assertEqual(b.search_step(),
                          2)

class TestIsSorted(unittest.TestCase):
    def runTest(self):
        b = bs.Bs()
        self.assertEqual(b.is_sorted([]),
                         True)
        self.assertEqual(b.is_sorted([0]),
                         True)
        self.assertEqual(b.is_sorted([0,1]),
                         True)
        self.assertEqual(b.is_sorted([1,0]),
                         False)
        self.assertEqual(b.is_sorted([0,1,2,3,2]),
                         False)
        self.assertEqual(b.is_sorted([0,1,2,3,4,5]),
                         True)

class TestSortStep(unittest.TestCase):
    def runTest(self):
        b = bs.Bs()
        self.assertEqual(b.sort_step([0,1,2], 2),
                         [0,2,1])

unittest.main()
