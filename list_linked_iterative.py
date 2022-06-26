
class List:

    # constructor can take any number of initial values in *args, uses the
    #   append method to add each of them rather than doing it manually
    def __init__(self,*args):
        self.size = 0
        self.first = None
        self.last = None
        for arg in args:
            self.append(arg)

    def __len__(self):
        return self.size

    # __repr__ builds the output string one value at a time, with "List(...)"
    #   as the underlying "shell" that will always be returned
    def __repr__(self):
        output = "List("
        if self.size > 0:
            output += repr(self.first.value)
            probe = self.first.next
            # values after the first one must be handled separately to ensure
            #   that commas are added where appropriate
            while probe is not None:
                output += ", "
                output += repr(probe.value)
                probe = probe.next
        output += ")"
        return output

    
    def append(self,value):
        # always begin by wrapping the new value into a Node
        new_node = Node(value)
        
        # special case: empty list, new node becomes both first and last
        if self.last is None:
            self.first = new_node
            self.last = new_node
        # usual case: new node is the old last's next, and becomes the new last
        else:
            self.last.next = new_node
            self.last = new_node
        # in either case, size is increased by 1
        self.size += 1
    
    def count(self,value):
        output = 0
        probe = self.first
        # no need for special case here, whether self.first is None or not we
        #   want to search until probe hits a None
        while probe is not None:
            if probe.value == value:
                # add one "tally" each time we find a node with a value
                #   matching the one we're searching for
                output += 1
            probe = probe.next
        return output
    
    # leaves positive indexes alone while converting negative ones into
    #   positive ones, python-style
    # notably DOES NOT raise an exception if the index is too big OR TOO SMALL,
    #   that job is left to the caller
    def _adjust_index(self,index):
        if index >= 0:
            return index
        else:
            return len(self) + index
    
    def __contains__(self,value):
        probe = self.first
        # as with count, no need to special case the empty List
        while probe is not None:
            if probe.value == value:
                # as soon as a single match is found, we can return True
                return True
            probe = probe.next
        # if we reach a None without a match found, return False
        return False
    
    # because we're able to perform append in constant time thanks to our last
    #   pointer, we can implement "extend" by just repeatedly calling append
    #   without loss of (much) efficiency
    def extend(self,iterable):
        for value in iterable:
            self.append(value)
    
    def index(self,value):
        # this method operates similar to count and __contains__, but rather
        #   than returning bool we must return an index int. thus we must keep
        #   track of our position as an int as we search this time
        i = 0
        probe = self.first
        while probe is not None:
            # if a match is found at this position, return it
            if probe.value == value:
                return i
            # otherwise increase our index count *and* move the probe to the
            #   next node
            i += 1
            probe = probe.next
        # if we reach the end with no matches, we raise ValueError
        raise ValueError(f"{repr(value)} is not in List")

    
    def __getitem__(self,index):
        # use _adjust_index to convert pythonic negative indexes to positive
        index = self._adjust_index(index)
        
        # raise IndexError if provided index was too far positive *or too far
        #   negative*
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        
        # because this is the first of several methods that will need to access
        #   a node by index, we rely on helper method _get_node to do the core
        #   work here
        node = self._get_node(index)
        return node.value

    # operates identically to __getitem__ but sets the selected node's value
    #   to the provided one rather than returning it
    def __setitem__(self,index,value):
        index = self._adjust_index(index)
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        
        node = self._get_node(index)
        node.value = value

    # because insert can change the first node of the list, we need to handle
    #   that as a special case. it can *also* change the last node of the list,
    #   but we can piggyback on our append method for that
    def insert(self,index,value):
        index = self._adjust_index(index)
        
        # note that unlike above, we are allowing for indexes that are exactly
        #   equal to self.size on purpose
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")

        new_node = Node(value)
        # check if we're "inserting" at the end first, in part because our
        #   append method already has handling for the empty-list situation
        if index == self.size:
            self.append(value)
        # check also for the special case where we are inserting at the very
        #   beginning
        elif index == 0:
            new_node.next = self.first
            self.first = new_node
            self.size += 1
        # otherwise it's an internal insert, which (because this is a singly-
        #   linked list) we'll need to perform starting from the node *prior*
        #   (thus the index-1)
        else:
            prev_node = self._get_node(index-1)
            new_node.next = prev_node.next
            prev_node.next = new_node
            self.size += 1
        # looks a little strange to have manual increment of self.size in the
        #   latter two cases but not the first, but it's necessary because
        #   append already performs the size increment

    # this would be a really simple method if we didn't care about efficiency!
    #   we could just make repeated calls to our insert method. however, that
    #   would take O(n*m) time, and we can do it in O(n+m) - we only want to
    #   seek to the correct location once
    def insert_all(self,index,iterable):
    
        # begin by adjusting and validating the index, allowing for indexes
        #   that are exactly equal to our list's size
        index = self._adjust_index(index)
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")
        
        # assemble the iterable into its own set of singly-linked nodes, from
        #   first_new to last_new. not every iterable has a __len__ and an
        #   iterable may be empty, so we have to be careful about both of those
        #   possibilities as well.
        iter_len = 0
        for val in iterable:
            # first value in the iterable becomes both first and last in the
            #   temp chain
            if iter_len == 0:
                first_new = Node(val)
                last_new = first_new
            # every subsequent value gets tacked onto the end, and we keep
            #   track of this new end
            else:
                last_new.next = Node(val)
                last_new = last_new.next
            
            # measure how many nodes we are adding in all
            iter_len += 1
        
        # if there was at least one value in the iterable, begin insert proper
        if iter_len > 0:
            # if insertion is happening at the beginning of the list...
            if index == 0:
                last_new.next = self.first
                self.first = first_new
            # if insertion is happening at the end, even simpler...
            elif index == self.size:
                self.last.next = first_new
            # as with vanilla insert, internal inserts are more complicated. we
            #   need to locate the node prior to where the insertion should
            #   occur so that we can rewire the necessary next pointers
            else:
                pre_insert_node = self._get_node(index-1)
                post_insert_node = pre_insert_node.next
                last_new.next = post_insert_node
                pre_insert_node.next = first_new
        
        # increase our size by however many nodes were in the iterable,
        #   (potentially 0)
        self.size += iter_len
                
    # remove_at works very similar to insert, but the edge cases are a bit more
    #   complicated
    def remove_at(self,index):
        
        # adjust and validate index
        index = self._adjust_index(index)
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        
        # if we're removing the first node...
        if index == 0:
            # grab the value to return
            return_value = self.first.value
            # check if we're in the extra-special case of this being the only
            #   node and handle that
            if self.size == 1:
                self.first = None
                self.last = None
            # otherwise it's just the first node that needs updating
            else:
                self.first = self.first.next
        # if we're removing the last node...
        elif index == self.size - 1:
            # grab the value to return
            return_value = self.last.value
            
            # unfortunately since we're singly-linked we have no way of getting
            #   to this in constant time, we'll have to traverse the list with
            #   _get_node
            penultimate_node = self._get_node(self.size-2)
            # detach the last node from the penultimate and mark the
            #   penultimate as the new last
            penultimate_node.next = None
            self.last = penultimate_node
        # otherwise we're removing an internal node, which works almost
        #   identically to inserting an internal node
        else:
            prev_node = self._get_node(index-1)
            selected_node = prev_node.next
            return_value = selected_node.value
            prev_node.next = selected_node.next
        
        # no matter what, a successful removal means decrementing size and
        #   returning the value
        self.size -= 1
        return return_value

    
    def __eq__(self,other):
        # shortcut: check to see if self and other are the same actual object
        if self is other:
            return True
        # we're not equal if we're not both Lists
        elif type(self) != type(other):
            return False
        # we're not equal if we have different lengths
        elif len(self) != len(other):
            return False
        # otherwise it comes down to having the same values in the same order
        else:
            # track through each list with a probe in parallel
            self_probe = self.first
            other_probe = other.first
            # until we hit the end of both lists...
            while self_probe is not None:
                # any value mismatch means the lists are unequal
                if self_probe.value != other_probe.value:
                    return False
                self_probe = self_probe.next
                other_probe = other_probe.next
            # if we hit the end without a value mismatch, lists are equal
            return True

    def __lt__(self,other):
        # shortcut: an object is never less than itself
        if self is other:
            return False
        # raise exception if we're trying to compare a List to a non-List
        elif type(self) != type(other):
            raise TypeError("List inequality only supported between Lists")
        else:
            # track through each list with a probe in parallel
            self_probe = self.first
            other_probe = other.first
            # while true loop since we WILL hit one of these conditions while
            #   tracking
            while True:
                # true case 1: no mismatch is found but self runs out of nodes
                #   before other does
                if self_probe is None and other_probe is not None:
                    return True
                # false case 1: no mismatch is found but other runs out of
                #   nodes either before self or at the same time
                elif other_probe is None:
                    return False
                # true case 2: self is less than other at this position
                elif self_probe.value < other_probe.value:
                    return True
                # false case 2: self is greater than other at this position
                elif self_probe.value > other_probe.value:
                    return False
                # iterative case: self and other are equal at this position
                else:
                    self_probe = self_probe.next
                    other_probe = other_probe.next

    # defining >= in terms of <
    def __ge__(self,other):
        return not self < other

    # helper method used for fetching a reference to a particular Node, rather
    #   than just its value
    # note that this method DOES NOT adjust/validate the index, as any such
    #   adjustment should have already been performed by the caller
    def _get_node(self,index):

        # special case first node
        if index == 0:
            return self.first
        # special case last node
        elif index == self.size - 1:
            return self.last
        # for normal cases, have to probe in a linear fashion 
        else:
            probe = self.first
            for i in range(index):
                probe = probe.next
            return probe
        
# "dumb" Node class, only has a constructor in iterative approach
class Node:

    def __init__(self,value):
        self.value = value
        self.next = None


if __name__ == "__main__":
    num = List(1, 2, 3, 4)
    num2 = List(1, 2, 4, 4)
    print(num < num2)