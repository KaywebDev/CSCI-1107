
class Stack:

    def __init__(self):
        self.top = None
        self.size = 0

    def push(self,value):
        self.size += 1
        new_top = Node(value)
        new_top.set_next(self.top)
        self.top = new_top

    def pop(self):
        if self.is_empty():
            raise EmptyStack("Can't pop empty stack.")
        self.size -= 1
        return_value = self.top.get_value()
        self.top = self.top.get_next()
        return return_value

    def peek(self):
        if self.is_empty():
            raise EmptyStack("Can't peek empty stack.")
        return self.top.get_value()

    def is_empty(self):
        return self.top is None

    def __len__(self):
        return self.size

class Node:

    def __init__(self,value):
        self.value = value
        self.next = None

    def get_value(self):
        return self.value

    def set_value(self,value):
        self.value = value

    def get_next(self):
        return self.next

    def set_next(self,new_next):
        self.next = new_next

class EmptyStack(Exception):
    pass

if __name__ == "__main__":
    my_stack = Stack()
    for code_point in range(ord('a'),ord('z')+1):
        my_stack.push(chr(code_point))
    while not my_stack.is_empty():
        print(len(my_stack))
        print(my_stack.pop())
        print(len(my_stack))
        print()
