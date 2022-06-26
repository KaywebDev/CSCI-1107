
class Queue:

    def __init__(self):
        self.logical_size = 0
        self.first = None
        self.last = None

    def is_empty(self):
        return self.logical_size == 0

    def __len__(self):
        return self.logical_size

    def enqueue(self,value):
        new_node = Node(value)
        if self.logical_size == 0:
            self.first = new_node
        else:
            self.last.next = new_node
        self.last = new_node
        self.logical_size += 1

    def dequeue(self):
        if self.logical_size == 0:
            raise EmptyQueue("Can't dequeue from an empty queue.")
        elif self.logical_size == 1:
            self.last = None
        return_value = self.first.value
        self.first = self.first.next
        self.logical_size -= 1
        return return_value

    def __str__(self):
        output = "Queue->"
        next_node = self.first
        while next_node is not None:
            output += str(next_node.value)
            output += "->"
            next_node = next_node.next
        return output

class Node:

    def __init__(self,value):
        self.value = value
        self.next = None

class EmptyQueue(Exception):
    pass

if __name__ == "__main__":
    my_queue = Queue()
    for c in "ABCDEFG":
        my_queue.enqueue(c)
    for c in "HIJKLMN":
        print(my_queue.dequeue())
        print(len(my_queue))
        my_queue.enqueue(c)
    while True:
        print(my_queue.dequeue())
        print(len(my_queue))
