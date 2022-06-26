
class SimpleArray:

    def __init__(self,capacity,fill_value=None):
        self._elements = list()
        for i in range(capacity):
            self._elements.append(fill_value)

    def __len__(self):
        return len(self._elements)

    def __str__(self):
        return str(self._elements)

    def __iter__(self):
        return iter(self._elements)

    def __getitem__(self,index):
        return self._elements[index]

    def __setitem__(self,index,new_value):
        self._elements[index] = new_value

if __name__ == "__main__":

    my_array = SimpleArray(5)
    my_array[0] = 'a'
    my_array[1] = 'b'
    my_array[2] = 'c'

    print("Hi there")

    for val in my_array:
        print(val)
    for val in my_array:
        print(val)
