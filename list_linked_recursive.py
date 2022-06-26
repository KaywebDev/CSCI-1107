
class List:

    def __init__(self, *args):
        if len(args) == 0:
            self.first = None
        else:
            self.first = Node(*args)

    def __len__(self):
        if self.first is None:
            return 0
        else:
            return len(self.first)
    
    def __repr__(self):
        output = "List("
        if self.first is not None:
            output += self.first.repr_helper()
        output += ")"
        return output

    def append(self, value):
        if self.first is None:
            self.first = Node(value)
        else:
            self.first.append(value)
    
    def count(self, value):
        if self.first is None:
            return 0
        else:
            return self.first.count(value)
    
    def _adjust_index(self, index):
        if index >= 0:
            return index
        else:
            return len(self) + index
    
    def __contains__(self, value):
        if not self.first:
            return False
        else:
            return value in self.first
    
    def index(self, value):
        if not self.first:
            raise ValueError(f"{value} not in the list")
        else:
            return self.first.index(value)

    def __getitem__(self, index):
        if not self.first:
            raise IndexError("Index out of range")
        index = self._adjust_index(index)
        return self.first[index]

    def __setitem__(self, index, value):
        if not self.first:
            raise IndexError("Index out of range")
        index = self._adjust_index(index)
        self.first[index] = value

    def insert(self, index, value):
        if not self.first:
            raise IndexError("Index out of range")
        index = self._adjust_index(index)
        if index == 0:
            new_node = Node(value)
            new_node.next = self.first
            self.first = new_node
        else:
            self.first.insert(index, value)

    def remove_at(self, index):
        if not self.first:
            raise IndexError("Index out of range")
        index = self._adjust_index(index)
        if index == 0:
            value = self.first.value
            self.first = self.first.next
            return value
        else:
            return self.first.remove_at(index)
    
    def extend(self, iterable):
        if not self.first:
            try:
                self.first = Node(*iterable)
            except TypeError:
                pass
        else:
            return self.first.extend(iterable)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        elif (not self.first) and (not other.first):
            return True
        elif not self.first:
            return False
        elif not other.first:
            return False
        else:
            return self.first == other.first

    def __lt__(self, other):
        if type(other) != type(self):
            raise TypeError("List inequality only supported between Lists")
        if self.first and other.first:
            return self.first < other.first
        elif other.first:
            return True
        else:
            return False

    def __ge__(self, other):
        return not self < other


class Node:

    def __init__(self, value, *args):
        self.value = value
        if len(args) == 0:
            self.next = None
        else:
            self.next = Node(*args)

    def __len__(self):
        if self.next is None:
            return 1
        else:
            return 1 + len(self.next)
    
    def repr_helper(self):
        output = repr(self.value)
        if self.next is not None:
            output += ", "
            output += self.next.repr_helper()
        return output

    def append(self, value):
        if self.next is None:
            self.next = Node(value)
        else:
            self.next.append(value)
    
    def count(self, value):
        the_count = 0
        if self.value == value:
            the_count += 1
        if self.next is not None:
            the_count += self.next.count(value)
        return the_count
    
    def __contains__(self, value):
        if self.value == value:
            return True
        elif self.next:
            return value in self.next
        else:
            return False
    
    def index(self, value):
        if self.value != value:
            if self.next:
                return 1 + self.next.index(value)
            else:
                raise ValueError(f"{value} not in the list")
        else:
            return 0
    
    def __getitem__(self, index):
        if index == 0:
            return self.value
        if not self.next:
            raise IndexError("Index out of range")
        else:
            return self.next[index-1]

    def __setitem__(self, index, value):
        if index == 0:
            self.value = value
            return
        if not self.next:
            raise IndexError("Index out of range")
        else:
            self.next[index-1] = value
    
    def insert(self, index, value):
        if index == 1:
            new_node = Node(value)
            new_node.next = self.next
            self.next = new_node
        else:
            try:
                self.next.insert(index-1, value)
            except AttributeError:
                raise IndexError("Index out of range")
    
    def remove_at(self, index):
        if index == 1:
            value = self.next.value
            self.next = self.next.next
            return value
        else:
            try:
                return self.next.remove_at(index-1)
            except AttributeError:
                raise IndexError("Index out of range")
    
    def extend(self, iterable):
        if not self.next:
            try:
                self.next = Node(*iterable)
            except TypeError:
                pass
        else:
            return self.next.extend(iterable)
    
    def __eq__(self, other):
        if type(other) != type(self):
            return False
        if self.next and other.next:
            if self.value == other.value:
                return self.next == other.next
            else:
                return False
        elif (not self.next) and (not other.next):
            return self.value == other.value
        else:
            return False

    def __lt__(self, other):
        if type(other) != type(self):
            return False
        if (not self.next) and other.next:
            return True
        elif not other.next:
            return False
        elif self.value < other.value:
            return True
        elif self.value > other.value:
            return False
        else:
            return self.next < other.next

    def __ge__(self, other):
        return not self < other


if __name__ == "__main__":
    List()
