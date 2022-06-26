
import simple_array

MINIMUM_CAPACITY = 10

class List:
    
    # while we could rely on our _expand_if_necessary method here, measuring
    #   the initial required size ourselves means we don't have to create and
    #   immediately dispose of an internal array that's too small
    def __init__(self,*args):
        self.logical_size = len(args)
        initial_capacity = MINIMUM_CAPACITY
        while initial_capacity < len(args):
            initial_capacity *= 2
        self.array = simple_array.SimpleArray(initial_capacity)
        for i in range(len(args)):
            self.array[i] = args[i]

    def __len__(self):
        return self.logical_size
    
    # build the __repr__ string one value at a time, special-casing the first
    def __repr__(self):
        output = "List("
        if self.logical_size > 0:
            output += repr(self.array[0])
        for i in range(1,self.logical_size):
            output += ", "
            output += repr(self.array[i])
        output += ")"
        return output

    def append(self,value):
        # ensure we won't outgrow our internal array with this new value
        self._expand_if_necessary(self.logical_size+1)
        
        # place the new value at the previous logical_size before incrementing
        #   it
        self.array[self.logical_size] = value
        self.logical_size += 1
    
    # fairly straightforward, but remember that we must only count up to our
    #   logical size, not capacity, or we will include garbage in the count
    def count(self,value):
        output = 0
        for i in range(self.logical_size):
            if self.array == value:
                output += 1
        return output
    
    # leaves positive indexes alone while converting negative ones into
    #   positive ones, python-style
    # notably DOES NOT raise an exception if the index is too big OR TOO SMALL,
    #   that job is left to the caller
    def _adjust_index(self,index):
        if index >= 0:
            return index
        else:
            return len(self)+index
    
    # similar to count but we can return immediately on finding the first
    #   occurrence
    # still need to bound ourselves by logical size
    def __contains__(self,value):
        for i in range(self.logical_size):
            if self.array[i] == value:
                return True
        return False
    
    # similar to above, searching for match up to (not including) logical size
    # raises exception if value isn't present anywhere
    def index(self,value):
        for i in range(self.logical_size):
            if self.array[i] == value:
                return i
        raise ValueError(f"{repr(value)} is not in List")

    def __getitem__(self,index):
        # adjust the index first in case it's negative
        index = self._adjust_index(index)
        
        # if it's [still] out of bounds, raise an exception
        if index < 0 or index >= self.logical_size:
            raise IndexError()
        
        # otherwise we can just play middleman and grab it directly from the
        #   internal array
        return self.array[index]

    # exact same as __getitem__ but setting the value rather than returning it
    def __setitem__(self,index,value):
        index = self._adjust_index(index)
        if index < 0 or index >= self.logical_size:
            raise IndexError()
        self.array[index] = value
    
    # insertion is a problem point for an array-based list. we'll need to shift
    #   all the values at and beyond the insertion point over to the right.
    def insert(self,index,value):
        
        # first adjust/validate the index
        index = self._adjust_index(index)
        if index < 0 or index > self.logical_size:
            raise IndexError()
        
        # expand the inner array first if we're currently full
        self._expand_if_necessary(self.logical_size+1)
        
        # from the right-hand side (INCLUSIVE) DOWN to the insertion point
        #   (ALSO INCLUSIVE), shift every value one index to the right
        for i in range(self.logical_size+1,index,-1):
            self.array[i] = self.array[i-1]
        
        # finally, we can add the new value to the intended location and
        #   increment our logical size
        self.array[index] = value
        self.logical_size += 1
    
    # the key thing we want to avoid here is doing more copy operations than
    #   necessary
    def insert_all(self,index,iterable):
        
        # adjust and validate the index
        index = self._adjust_index(index)
        if index < 0 or index > self.logical_size:
            raise IndexError()
            
        # iterables aren't all required to have __len__, sooo....
        iter_len = 0
        for _ in iterable:
            iter_len += 1
        
        # might as well skip the rest of this if the iterable was empty
        if iter_len > 0:
            
            # expand as much as necessary - note that this could potentially
            #   require MULTIPLE doublings, and we are set up for that!
            self._expand_if_necessary(self.logical_size+iter_len)
            
            # begin the shifting process, like with the insert method, but this
            #   time we potentially need to shift everything *multiple* spaces
            #   over - however many values are in the iterable
            for i in range(self.logical_size+iter_len,
                           index+iter_len-1,
                           -1):
                self.array[i] = self.array[i-iter_len]
            
            # then we can loop through the iterable and copy the values into
            #   the array since those values have all been preserved
            i = index
            for value in iterable:
                self.array[i] = value
                i += 1
            
            # last, update the logical size
            self.logical_size += iter_len
    
    
    def remove_at(self,index):
    
        # first adjust and validate the index
        index = self._adjust_index(index)
        if index < 0 or index >= self.logical_size:
            raise IndexError()
        
        # grab the value for returning before we remove it
        return_value = self.array[index]
        
        # starting from the index, going UP, copy in values from the RIGHT
        for i in range(index,self.logical_size):
            self.array[i] = self.array[i+1]
        self.logical_size -= 1

        # check to see if we should shrink our internal array
        self._shrink_if_quarter()
        
        return return_value
    
    # extend is just a special case of insert_all, why not treat it as one?
    def extend(self,iterable):
        self.insert_all(self.logical_size,iterable)
    
    
    def __eq__(self,other):
        # shortcut: is other the same object as self?
        if self is other:
            return True
        # return False if other isn't a List
        elif type(self) != type(other):
            return False
        # if the lengths vary, the lists are unequal
        elif len(self) != len(other):
            return False
        else:
            # otherwise scan for positionally mismatched values
            for i in range(self.logical_size):
                if self.array[i] != other.array[i]:
                    return False
            return True

    def __lt__(self,other):
        # shortcut: no object is less than itself
        if self is other:
            return False
        # raise exception if "other" isn't a List
        elif type(self) != type(other):
            raise TypeError("List inequality only supported between Lists")
        else:
            # using this rather than a for loop since we might need to go one
            #   index beyond the end of either self or other
            i = 0
            while True:
                # true case 1: no mismatch is found but self runs out of nodes
                #   before other does
                if i == len(self) and i != len(other):
                    return True
                # false case 1: no mismatch is found but other runs out of
                #   nodes either before self or at the same time
                elif i == len(other):
                    return False
                # true case 2: self is less than other at this position
                elif self.array[i] < other.array[i]:
                    return True
                # false case 2: self is greater than other at this position
                elif self.array[i] > other.array[i]:
                    return False
                # iterative case: self and other are equal at this position
                else:
                    i += 1
    
    # defining >= in terms of <
    def __ge__(self,other):
        return not self < other
    
    # internal method responsible for upsizing the internal array when
    #   necessary
    # "capacity_required" is what the logical_size will be at the END of
    #   whatever operation is about to occur
    # multiple doublings are possible if necessary!
    def _expand_if_necessary(self,capacity_required):
        if capacity_required > len(self.array):
            new_capacity = len(self.array)
            while capacity_required > new_capacity:
                new_capacity *= 2
            new_array = simple_array.SimpleArray(new_capacity)
            for i in range(self.logical_size):
                new_array[i] = self.array[i]
            self.array = new_array
    
    # internal method responsible for downsizing the internal array when one
    #   quarter or less of it is in use
    # note that multiple halvings can be triggered by this method at once, even
    #   though we currently do not have any methods which would decrease our
    #   logical size by more than 1 at a time
    def _shrink_if_quarter(self):
        if len(self.array) > MINIMUM_CAPACITY and \
              self.logical_size <= len(self.array) // 4:
            new_capacity = len(self.array)
            while new_capacity > MINIMUM_CAPACITY and \
                  self.logical_size <= new_capacity // 4:
                new_capacity //= 2
            new_array = simple_array.SimpleArray(new_capacity)
            for i in range(self.logical_size):
                new_array[i] = self.array[i]
            self.array = new_array
                  

if __name__ == "__main__":
    my_list = List('a','b','b','a','b')
    print(my_list)