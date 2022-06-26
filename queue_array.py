
from simple_array import SimpleArray

MINIMUM_CAPACITY = 10

class Queue:

    def __init__(self):
        self.array = SimpleArray(MINIMUM_CAPACITY)
        self.logical_size = 0
        self.start_index = 0
        self.end_index = 0

    def enqueue(self,value):
        self._grow_if_necessary(self.logical_size+1)
        self.array[self.end_index] = value
        self.end_index += 1
        self.end_index %= self._capacity()
        self.logical_size += 1

    def dequeue(self):
        if self.logical_size == 0:
            raise EmptyQueue("Can't dequeue from an empty queue.")
        return_value = self.array[self.start_index]
        self.start_index += 1
        self.start_index %= self._capacity()
        self.logical_size -= 1
        self._shrink_if_quarter(self.logical_size)
        return return_value

    def front(self):
        if self.logical_size == 0:
            raise EmptyQueue("Can't dequeue from an empty queue.")
        return self.array[self.start_index]

    def __len__(self):
        return self.logical_size

    def is_empty(self):
        return self.logical_size == 0

    def __str__(self):
        output = "Queue->"
        for i in range(self.logical_size):
            output += str(self.array[(self.start_index+i)%self._capacity()])
            output += "->"
        return output

    def _capacity(self):
        return len(self.array)

    def _grow_if_necessary(self,new_size):
        if new_size > self._capacity():
            new_array = SimpleArray(self._capacity()*2)
            for i in range(self.logical_size):
                new_array[i] = self.array[(self.start_index+i)%self._capacity()]
            self.array = new_array
            self.start_index = 0
            self.end_index = self.logical_size

    def _shrink_if_quarter(self,new_size):
        if self._capacity() > MINIMUM_CAPACITY and new_size <= self._capacity()//4:
            new_array = SimpleArray(self._capacity()//2)
            for i in range(self.logical_size):
                new_array[i] = self.array[(self.start_index+i)%self._capacity()]
            self.array = new_array
            self.start_index = 0
            self.end_index = self.logical_size
            
            

class EmptyQueue(Exception):
    pass

if __name__ == "__main__":
    x = Queue()
    for i in range(10):
        x.enqueue(i)
    for i in range(5):
        x.dequeue()
    for i in range(10,15):
        x.enqueue(i)
    print(x.array)
    x.enqueue(15)
    print(x.array)
    for i in range(16,25):
        x.enqueue(i)
    print(x.array)
    for i in range(14):
        x.dequeue()
    print(x.array)
    x.dequeue()
    print(x.array)
