
import simple_array

INITIAL_STACK_CAPACITY = 10

class Stack:

    def __init__(self):
        self.values = simple_array.SimpleArray(INITIAL_STACK_CAPACITY)
        self.logical_size = 0

    def push(self,value):
        self._grow_if_necessary(self.logical_size+1)
        self.values[self.logical_size] = value
        self.logical_size += 1

    def pop(self):
        if self.logical_size == 0:
            raise EmptyStack("Can't pop empty stack.")
        self.logical_size -= 1
        return_value = self.values[self.logical_size]
        self._shrink_if_quarter()
        return return_value

    def peek(self):
        if self.logical_size == 0:
            raise EmptyStack("Can't peek empty stack.")
        return self.values[self.logical_size-1]

    def is_empty(self):
        return self.logical_size == 0

    def _capacity(self):
        return len(self.values)

    def _grow_if_necessary(self,new_size):
        if new_size > self._capacity():
            new_values = simple_array.SimpleArray(self._capacity()*2)
            for i in range(self.logical_size):
                new_values[i] = self.values[i]
            self.values = new_values

    def _shrink_if_quarter(self):
        if self._capacity() > INITIAL_STACK_CAPACITY and \
           self.logical_size <= self._capacity() // 4:
            new_values = simple_array.SimpleArray(self._capacity()//2)
            for i in range(self.logical_size):
                new_values[i] = self.values[i]
            self.values = new_values

    def __len__(self):
        return self.logical_size


class EmptyStack(Exception):
    pass
        

if __name__ == "__main__":
    my_stack = Stack()
    for i in range(100):
        my_stack.push(i)
    while not my_stack.is_empty():
        print(my_stack.pop())
