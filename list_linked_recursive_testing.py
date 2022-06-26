
from list_linked_recursive import List
import unittest

class TestInit(unittest.TestCase):
    
    def test_init_empty(self):
        the_list = List()
        self.assertEqual(the_list.first,None)
    
    def test_init_single(self):
        the_list = List(5)
        self.assertEqual(the_list.first.value,5)
        self.assertEqual(the_list.first.next,None)
    
    def test_init_multi(self):
        the_list = List('a','b','c')
        self.assertEqual(the_list.first.value,'a')
        self.assertEqual(the_list.first.next.value,'b')
        self.assertEqual(the_list.first.next.next.value,'c')
        self.assertEqual(the_list.first.next.next.next,None)

class TestLen(unittest.TestCase):
    
    def test_len_empty(self):
        the_list = List()
        self.assertEqual(len(the_list),0)
    
    def test_init_single(self):
        the_list = List('a')
        self.assertEqual(len(the_list),1)
        self.assertEqual(len(the_list.first),1)
    
    def test_init_multi(self):
        the_list = List('a','b','c')
        self.assertEqual(len(the_list),3)
        self.assertEqual(len(the_list.first),3)
        self.assertEqual(len(the_list.first.next),2)
        self.assertEqual(len(the_list.first.next.next),1)

class TestAppend(unittest.TestCase):

    def test_append_empty(self):
        the_list = List()
        the_list.append('a')
        self.assertEqual(the_list.first.value,'a')
        self.assertEqual(the_list.first.next,None)
    
    def test_append_normal(self):
        the_list = List('a','b','c')
        the_list.append('d')
        self.assertEqual(the_list.first.next.next.next.value,'d')
        self.assertEqual(the_list.first.next.next.next.next,None)

class TestCount(unittest.TestCase):
    
    def test_count_empty(self):
        the_list = List()
        self.assertEqual(the_list.count('x'),0)
        self.assertEqual(the_list.count(''),0)
        self.assertEqual(the_list.count(0),0)
        self.assertEqual(the_list.count(None),0)
    
    def test_count_abbabca(self):
    
        test_values = 'abbabca'
        
        the_list = List(*test_values)
        for unique_value in set(test_values):
            self.assertEqual(the_list.count(unique_value),test_values.count(unique_value))
        
        probe = the_list.first
        remaining_values = test_values
        while remaining_values != "":
            for unique_value in set(remaining_values):
                self.assertEqual(probe.count(unique_value),remaining_values.count(unique_value))
            probe = probe.next
            remaining_values = remaining_values[1:]
        
    
class TestExtend(unittest.TestCase):
    
    def test_extend_empty_to_empty(self):
        the_list = List()
        the_iterable = iter("")
        the_list.extend(the_iterable)
        self.assertEqual(the_list.first,None)
    
    def test_extend_empty_to_normal(self):
        the_list = List('a','b')
        the_iterable = iter("")
        the_list.extend(the_iterable)
        self.assertEqual(the_list.first.value,'a')
        self.assertEqual(the_list.first.next.value,'b')
        self.assertEqual(the_list.first.next.next,None)
    
    def test_extend_normal_to_empty(self):
        the_list = List()
        the_iterable = iter("xy")
        the_list.extend(the_iterable)
        self.assertEqual(the_list.first.value,'x')
        self.assertEqual(the_list.first.next.value,'y')
        self.assertEqual(the_list.first.next.next,None)
    
    def test_extend_normal_to_normal(self):
        the_list = List('a','b')
        the_iterable = iter("xy")
        the_list.extend(the_iterable)
        self.assertEqual(the_list.first.value,'a')
        self.assertEqual(the_list.first.next.value,'b')
        self.assertEqual(the_list.first.next.next.value,'x')
        self.assertEqual(the_list.first.next.next.next.value,'y')
        self.assertEqual(the_list.first.next.next.next.next,None)

class TestGetItem(unittest.TestCase):

    def test_get_from_empty(self):
        with self.assertRaises(IndexError):
            List()[0]
        with self.assertRaises(IndexError):
            List()[1]
        with self.assertRaises(IndexError):
            List()[-1]
    
    def test_get_normal(self):
        the_list = List('a','b','c')
        self.assertEqual(the_list[0],'a')
        self.assertEqual(the_list.first[0],'a')
        self.assertEqual(the_list[1],'b')
        self.assertEqual(the_list.first[1],'b')
        self.assertEqual(the_list.first.next[0],'b')
        self.assertEqual(the_list[2],'c')
        self.assertEqual(the_list.first[2],'c')
        self.assertEqual(the_list.first.next[1],'c')
        self.assertEqual(the_list.first.next.next[0],'c')
    
    def test_get_too_large(self):
        the_list = List('a','b','c')
        with self.assertRaises(IndexError):
            the_list[3]
        with self.assertRaises(IndexError):
            the_list.first[3]
        with self.assertRaises(IndexError):
            the_list.first.next[2]
        with self.assertRaises(IndexError):
            the_list.first.next.next[1]
    
    def test_get_negative(self):
        the_list = List('a','b','c')
        self.assertEqual(the_list[-3],'a')
        self.assertEqual(the_list[-2],'b')
        self.assertEqual(the_list[-1],'c')
    
    def test_get_too_small(self):
        the_list = List('a','b','c')
        with self.assertRaises(IndexError):
            the_list[-4]

class TestSetItem(unittest.TestCase):

    def test_set_from_empty(self):
        the_list = List()
        with self.assertRaises(IndexError):
            the_list[0] = 'a'
        with self.assertRaises(IndexError):
            the_list[1] = 'a'
        with self.assertRaises(IndexError):
            the_list[-1] = 'a'
    
    def test_set_normal(self):
        the_list = List('a','b','c')
        the_list[0] = 'x'
        self.assertEqual(the_list.first.value,'x')
        the_list[1] = 'y'
        self.assertEqual(the_list.first.next.value,'y')
        the_list[2] = 'z'
        self.assertEqual(the_list.first.next.next.value,'z')
    
    def test_set_too_large(self):
        the_list = List('a','b','c')
        with self.assertRaises(IndexError):
            the_list[3] = 'd'
    
    def test_set_negative(self):
        the_list = List('a','b','c')
        the_list[-1] = 'x'
        self.assertEqual(the_list.first.next.next.value,'x')
        the_list[-2] = 'y'
        self.assertEqual(the_list.first.next.value,'y')
        the_list[-3] = 'z'
        self.assertEqual(the_list.first.value,'z')
    
    def test_get_too_small(self):
        the_list = List('a','b','c')
        with self.assertRaises(IndexError):
            the_list[-4] = 'd'

class TestContains(unittest.TestCase):
    
    def test_contains_empty(self):
        self.assertFalse('x' in List())
        self.assertFalse(None in List())
    
    def test_contains_normal(self):
        the_list = List('a','b','c')
        
        self.assertTrue('a' in the_list)
        self.assertTrue('a' in the_list.first)
        self.assertFalse('a' in the_list.first.next)
        self.assertFalse('a' in the_list.first.next.next)
        
        self.assertTrue('b' in the_list)
        self.assertTrue('b' in the_list.first)
        self.assertTrue('b' in the_list.first.next)
        self.assertFalse('b' in the_list.first.next.next)
        
        self.assertTrue('c' in the_list)
        self.assertTrue('c' in the_list.first)
        self.assertTrue('c' in the_list.first.next)
        self.assertTrue('c' in the_list.first.next.next)
        
        self.assertFalse('d' in the_list)
        self.assertFalse('d' in the_list.first)
        self.assertFalse('d' in the_list.first.next)
        self.assertFalse('d' in the_list.first.next.next)

class TestInsert(unittest.TestCase):
    
    def setUp(self):
        self.the_list = List('a','b')
    
    def test_insert_beginning(self):
        self.the_list.insert(0,'x')
        self.assertEqual(self.the_list.first.value,'x')
        self.assertEqual(self.the_list.first.next.value,'a')
        self.assertEqual(self.the_list.first.next.next.value,'b')
        self.assertEqual(self.the_list.first.next.next.next,None)
        self.the_list.insert(0,'y')
        self.assertEqual(self.the_list.first.value,'y')
        self.assertEqual(self.the_list.first.next.value,'x')
        self.assertEqual(self.the_list.first.next.next.value,'a')
        self.assertEqual(self.the_list.first.next.next.next.value,'b')
        self.assertEqual(self.the_list.first.next.next.next.next,None)
        
    def test_insert_middle(self):
        self.the_list.insert(1,'x')
        self.assertEqual(self.the_list.first.value,'a')
        self.assertEqual(self.the_list.first.next.value,'x')
        self.assertEqual(self.the_list.first.next.next.value,'b')
        self.assertEqual(self.the_list.first.next.next.next,None)
        self.the_list.insert(1,'y')
        self.assertEqual(self.the_list.first.value,'a')
        self.assertEqual(self.the_list.first.next.value,'y')
        self.assertEqual(self.the_list.first.next.next.value,'x')
        self.assertEqual(self.the_list.first.next.next.next.value,'b')
        self.assertEqual(self.the_list.first.next.next.next.next,None)
    
    def test_insert_end(self):
        self.the_list.insert(2,'x')
        self.assertEqual(self.the_list.first.value,'a')
        self.assertEqual(self.the_list.first.next.value,'b')
        self.assertEqual(self.the_list.first.next.next.value,'x')
        self.assertEqual(self.the_list.first.next.next.next,None)
        self.the_list.insert(3,'y')
        self.assertEqual(self.the_list.first.value,'a')
        self.assertEqual(self.the_list.first.next.value,'b')
        self.assertEqual(self.the_list.first.next.next.value,'x')
        self.assertEqual(self.the_list.first.next.next.next.value,'y')
        self.assertEqual(self.the_list.first.next.next.next.next,None)
    
    def test_insert_negative(self):
        self.the_list.insert(-1,'x')
        self.assertEqual(self.the_list.first.value,'a')
        self.assertEqual(self.the_list.first.next.value,'x')
        self.assertEqual(self.the_list.first.next.next.value,'b')
        self.assertEqual(self.the_list.first.next.next.next,None)
        self.the_list.insert(-3,'y')
        self.assertEqual(self.the_list.first.value,'y')
        self.assertEqual(self.the_list.first.next.value,'a')
        self.assertEqual(self.the_list.first.next.next.value,'x')
        self.assertEqual(self.the_list.first.next.next.next.value,'b')
        self.assertEqual(self.the_list.first.next.next.next.next,None)
    
    def test_insert_manual(self):
        self.the_list.first.insert(1,'x')
        self.assertEqual(self.the_list.first.value,'a')
        self.assertEqual(self.the_list.first.next.value,'x')
        self.assertEqual(self.the_list.first.next.next.value,'b')
        self.assertEqual(self.the_list.first.next.next.next,None)
    
    def test_insert_too_big(self):
        with self.assertRaises(IndexError):
            self.the_list.insert(3,'x')
    
    def test_insert_too_small(self):
        with self.assertRaises(IndexError):
            self.the_list.insert(-3,'x')

class TestIndex(unittest.TestCase):
    
    def test_index_empty(self):
        the_list = List()
        for value in ['x','',0,None]:
            with self.assertRaises(ValueError):
                the_list.index(value)
    
    def test_index_abcde(self):
        test_values = "abcde"
        absent_values = [None,0,'ab']
        the_list = List(*test_values)
        
        for value in test_values:
            self.assertEqual(test_values.index(value),the_list.index(value))
        for value in absent_values:
            with self.assertRaises(ValueError):
                the_list.index(value)
    
    def test_index_mixed(self):
        test_values = [None,True,0,9.5,'yes','testing',True,False,0]
        absent_values = ['a','b','c','d','e','x',9,-1,1]
        the_list = List(*test_values)
        
        for value in test_values:
            self.assertEqual(test_values.index(value),the_list.index(value))
        for value in ['a','b','c','d','e','x',9,-1]:
            with self.assertRaises(ValueError):
                the_list.index(value)

class TestRemoveAt(unittest.TestCase):
    
    def setUp(self):
        self.the_list = List('a','b','c','d','e')
    
    def test_remove_beginning(self):
        python_list = ['a','b','c','d','e']
        
        while len(python_list) > 0:
            self.assertEqual(python_list.pop(0),self.the_list.remove_at(0))
            probe = self.the_list.first
            for value in python_list:
                self.assertEqual(value,probe.value)
                probe = probe.next
        
    def test_remove_end(self):
        python_list = ['a','b','c','d','e']
        
        while len(python_list) > 0:
            self.assertEqual(python_list.pop(-1),self.the_list.remove_at(-1))
            probe = self.the_list.first
            for value in python_list:
                self.assertEqual(value,probe.value)
                probe = probe.next
    
    def test_remove_middle(self):
        python_list = ['a','b','c','d','e']
        
        while len(python_list) > 0:
            mid_index = len(python_list)//2
            self.assertEqual(python_list.pop(mid_index),self.the_list.remove_at(mid_index))
            probe = self.the_list.first
            for value in python_list:
                self.assertEqual(value,probe.value)
                probe = probe.next
    
    def test_remove_too_big(self):
        with self.assertRaises(IndexError):
            self.the_list.remove_at(5)
    
    def test_remove_too_small(self):
        with self.assertRaises(IndexError):
            self.the_list.remove_at(-6)

class TestEquality(unittest.TestCase):
    
    def test_empties_equal(self):
        self.assertEqual(List(),List())
    
    def test_abc_equal(self):
        self.assertEqual(List(*"abc"),List(*"abc"))
    
    def test_abc_abcd_unequal(self):
        self.assertFalse(List(*"abc")==List(*"abcd"))
    
    def test_empty_none_unequal(self):
        self.assertFalse(List()==List(None))
    
    def test_str_unequal(self):
        self.assertFalse(List(*"abc")=="str")
    
    def test_reallist_unequal(self):
        self.assertFalse(List(*"abc")==['a','b','c'])
    
class TestInequality(unittest.TestCase):
    
    def test_empties(self):
        self.assertFalse(List()<List())
        self.assertTrue(List()<=List())
        self.assertTrue(List()>=List())
        self.assertFalse(List()>List())
    
    def test_abc(self):
        self.assertFalse(List(*"abc")<List(*"abc"))
        self.assertTrue(List(*"abc")<=List(*"abc"))
        self.assertTrue(List(*"abc")>=List(*"abc"))
        self.assertFalse(List(*"abc")>List(*"abc"))
    
    def test_aaaaa_aabaa(self):
        self.assertTrue(List(*"aaaaa")<List(*"aabaa"))
        self.assertTrue(List(*"aaaaa")<=List(*"aabaa"))
        self.assertFalse(List(*"aaaaa")>=List(*"aabaa"))
        self.assertFalse(List(*"aaaaa")>List(*"aabaa"))
    
    def test_abc_abcd(self):
        self.assertTrue(List(*"abc")<List(*"abcd"))
        self.assertTrue(List(*"abc")<=List(*"abcd"))
        self.assertFalse(List(*"abc")>=List(*"abcd"))
        self.assertFalse(List(*"abc")>List(*"abcd"))
    
    def test_abc_ab(self):
        self.assertFalse(List(*"abc")<List(*"ab"))
        self.assertFalse(List(*"abc")<=List(*"ab"))
        self.assertTrue(List(*"abc")>=List(*"ab"))
        self.assertTrue(List(*"abc")>List(*"ab"))
    
    def test_incomparable_str(self):
        with self.assertRaises(TypeError):
            List(*"abc") < "abc"
        with self.assertRaises(TypeError):
            List(*"abc") <= "abc"
        with self.assertRaises(TypeError):
            List(*"abc") >= "abc"
        with self.assertRaises(TypeError):
            List(*"abc") > "abc"
        
    def test_incomparable_reallist(self):
        with self.assertRaises(TypeError):
            List(*"abc") < ['a','b','c']
        with self.assertRaises(TypeError):
            List(*"abc") <= ['a','b','c']
        with self.assertRaises(TypeError):
            List(*"abc") >= ['a','b','c']
        with self.assertRaises(TypeError):
            List(*"abc") > ['a','b','c']

if __name__ == "__main__":
    unittest.main(verbosity=2)