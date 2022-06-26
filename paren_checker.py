
from stack_array import Stack

symbols = {"(",")","[","]","{","}"}
matched_symbols = {"(":")",
                   "[":"]",
                   "{":"}"}

def is_balanced(the_string,v=0):

    symbol_stack = Stack()

    for c in the_string:
        if c in symbols:
            # if opening symbol
            if c in matched_symbols:
                if v >= 1:
                    print(f"Pushed {c} onto stack.")
                symbol_stack.push(c)
            # if closing symbol
            else:
                if symbol_stack.is_empty():
                    if v >= 1:
                        print(f"Found {c}, but stack empty, returning False.")
                    return False
                last_open = symbol_stack.pop()
                if c != matched_symbols[last_open]:
                    if v >= 1:
                        print(f"Found {c}, but top element of stack is {last_open}, returning False.")
                    return False
                else:
                    if v >= 1:
                        print(f"Found {c}, popped {last_open} from stack.")
        else:
            if v >= 2:
                print(f"Found {c}, ignoring.")

    if v >= 1:
            print(f"String processed, {len(symbol_stack)} symbols remain in stack.")
    return symbol_stack.is_empty()
                
    

if __name__ == "__main__":
    print(is_balanced(")([[{qrtq{567u}}]asffd]((()wre)))",v=1))
